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
            #print("writing ",sample,' in file')
            wav_file.writeframes(struct.pack('h', int(sample * 32767.0)))

        wav_file.close()

        return





if __name__ == "__main__":

    from PIL import Image

    imgHeight = 150 #in px
    beepDuration= 50 #in ms

    img = Image.open('poulet.jpg')
    long, larg = img.size


    #resizes the picture for its height to be 500px
    newlarg = imgHeight
    newlong = imgHeight * long / larg

    newlong = int(newlong)
    newlarg = int(newlarg)

    result = Image.new('L', (int(newlong), int(newlarg)))
    img = img.resize((newlong, newlarg))

    blackValue = [[0 for x in range(newlong)] for y in range(newlarg)]

    for y in range(newlarg):
        for x in range(newlong):
            r, v, b = img.getpixel([x, y])
            blackValue[y][x] = ((r + v + b) / 3) / 255
            result.putpixel((x, y), int((r + v + b) / 3))

    # for y in range(newlarg):
    #  print(blackValue[y][200])

    #result.show()
    print(result.size)

    #result.show()

    bg = BeepGenerator()
    bg.append_silence(beepDuration*newlong)

    baseFrequency = 100.0


    print("Generating Tone")
    for i in range(newlarg):
        temporaryWave = BeepGenerator()
        for j in range(newlong):

            # we increment the frequency each time for each row of pixels to show as a new row in the spectrogram
            temporaryWave.append_sinewave(baseFrequency-i**2,duration_milliseconds=beepDuration,volume=blackValue[i][j]/250)

        bg.add_sinewaves(temporaryWave)

    #print(bg.audio)

    print("Generating wav file")
    bg.save_wav("output.wav")