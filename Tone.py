import math
import wave
import struct


class BeepGenerator:
    def __init__(self):
        # Audio will contain a long list of samples (i.e. floating point numbers describing the
        # waveform).  If you were working with a very long sound you'd want to stream this to
        # disk instead of buffering it all in memory list this.  But most sounds will fit in
        # memory.
        self.audio = []
        self.sample_rate = 44100.0

    def append_silence(self, duration_milliseconds=500):
        """
        Adding silence is easy - we add zeros to the end of our array
        """
        num_samples = duration_milliseconds * (self.sample_rate / 1000.0)

        for x in range(int(num_samples)):
            self.audio.append(0.0)

        return


    def add_sinewaves(self,ad):
        for x in range(len(ad.audio)):
            self.audio[x]+=ad.audio[x]

        return self.audio

    def append_sinewave(
            self,
            freq=440.0,
            duration_milliseconds=500,
            volume=1.0):
        """
        The sine wave generated here is the standard beep.  If you want something
        more aggresive you could try a square or saw tooth waveform.   Though there
        are some rather complicated issues with making high quality square and
        sawtooth waves... which we won't address here :)
        """

        num_samples = duration_milliseconds * (self.sample_rate / 1000.0)

        for x in range(int(num_samples)):
            self.audio.append(volume * math.sin(2 * math.pi * freq * (x / self.sample_rate)))

        return

    def save_wav(self, file_name):
        # Open up a wav file
        wav_file = wave.open(file_name, "w")

        # wav params
        nchannels = 1

        sampwidth = 2

        # 44100 is the industry standard sample rate - CD quality.  If you need to
        # save on file size you can adjust it downwards. The stanard for low quality
        # is 8000 or 8kHz.
        nframes = len(self.audio)
        comptype = "NONE"
        compname = "not compressed"
        wav_file.setparams((nchannels, sampwidth, self.sample_rate, nframes, comptype, compname))

        # WAV files here are using short, 16 bit, signed integers for the
        # sample size.  So we multiply the floating point data we have by 32767, the
        # maximum value for a short integer.  NOTE: It is theortically possible to
        # use the floating point -1.0 to 1.0 data directly in a WAV file but not
        # obvious how to do that using the wave module in python.
        for sample in self.audio:
            wav_file.writeframes(struct.pack('h', int(sample * 32767.0)))

        wav_file.close()

        return



class SpectrogramGenerator:
    def __init__(self,image_name):
        self.imageHeight = 150
        self.beepDuration = 50
        self.image = Image.open(image_name)
        self.outputImage = None
        self.outputValues = None
        self.newlong = None
        self.newlarg = None

    def generate_outputImage(self):
        long, larg = self.image.size
        self.newlarg = int(self.imageHeight)
        self.newlong = int(self.imageHeight * long / larg)

        self.outputImage = Image.new('L', (self.newlong, self.newlarg))
        img = self.image.resize((self.newlong, self.newlarg))

        self.outputValues = [[0 for _ in range(self.newlong)] for _ in range(self.newlarg)]

        for y in range(self.newlarg):
            for x in range(self.newlong):
                r, v, b = img.getpixel([x, y])
                self.outputValues[y][x] = ((r + v + b) / 3) / 255
                self.outputImage.putpixel((x, y), int((r + v + b) / 3))

        return self.outputImage



    def generateTone(self,filename):
        bg = BeepGenerator()
        bg.append_silence(self.beepDuration * self.newlong)

        baseFrequency = 100.0

        print("Generating Tone")
        for i in range(self.newlarg):
            temporaryWave = BeepGenerator()
            for j in range(self.newlong):
                # we increment the frequency each time for each row of pixels to show as a new row in the spectrogram
                temporaryWave.append_sinewave(baseFrequency + (self.newlarg - i - 1) ** 2,
                                              duration_milliseconds=self.beepDuration, volume=self.outputValues[i][j] / 250)

            bg.add_sinewaves(temporaryWave)

        # print(bg.audio)

        print("Generating wav file")
        bg.save_wav(filename)




if __name__ == "__main__":

    from PIL import Image
    import sys

    sg = SpectrogramGenerator(str(sys.argv[1]))
    sg.generate_outputImage()
    sg.generateTone(str(sys.argv[2]))