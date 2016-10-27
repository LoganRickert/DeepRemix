# DeepRemix
## Remixing Music with Deep Learning

An interface in which you input a number of songs by one artist, and a song by another artist. Then a LSTM neural network in a GAN framework will output a remix of the song in the style of the first artist. Inputs are being parsed as Mel-Frequency Cepstrum Coefficients. Testing is done using PyTest and TravisCI.

For more information see [DeepRemix.com.](http://deepremix.com)

## Dependencies
* Python 2.7
* Keras
* Scipy
* Numpy
* librosa
* PyTest


## Usage

Clone the repository, copy the song you'd like to remix into `./data/to_remix` and run

 `python music_parsing.py`

 Once the song has been put in an appropriate representational state (MFCC), you can now run it through the neural network by running:

 `python scriptthatrunsnetworkgoeshere.py`

 This will save the output song into `./data/output_wavs`

# Travis CI
## To test a build, do the following:

* Commit and push something to the repository...
