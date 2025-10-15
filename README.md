# Image to Spectrogram

By Rémy Caruhel

## Description 

This project aims to take an image, and to transcribe into an audio wav file.

The available image formats are : 
.jpg
.png
.jpeg

## How to run it

py Tone.py "YourRimage.png" "WavFileName"

## How it works

### Step 1 : Image resizing

The image is resized into a 150px high black and white image
An array of the black and while values

### Step 2 : Building the audio file

#### Building one line

For the first row of the resized image, a sine wave is first created at the highest frequency (around 20kHz) 
The value of the frequency used for each line of the image is : (previousFrequency-rowNumber)^2
Every 5 miliseconds, the intensity of this sine wave is changed accordingly to the value of each pixel.


#### Building other lines

To build the other lines of the image, all the sine waves are added.

Then the wav file is build with the previously sine wave.
