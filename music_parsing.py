from __future__ import print_function
import os

from scipy.io import wavfile
import numpy as np
import librosa
import sys


def parse_wav(filename, n_mfcc=40):
    '''
    Parses a single wav file into MFCC's and sample rate.

    Arguments:
        filename - Name of input wav file.
        n_mfcc   - Number of coefficients to use.

    Returns:
        A tuple with a numpy array with cepstrum coefficients, and sample rate.

    Raises:

    '''

    song_data = np.array([])
    sample_rate = -1
    if filename[-4:] == '.wav':
        try:
            y_data, sample_rate = librosa.load(filename)
            #  will need to experiment with different values for n_mfcc
            song_data = librosa.feature.mfcc(y=y_data,
                                             sr=sample_rate,
                                             n_mfcc=n_mfcc)
        except:
            sys.exit(1)

    return (song_data, sample_rate)


def directory_to_array(filepath="./data/input_wavs", n_mfcc=40):
    '''
    Parses all wav files into Mel-Frequency Cepstrum Coefficients.

    Arguments:
        filepath - Path to directory containing .wav files
        n_mfcc   - Number of coefficients to use.

    Returns:
        A dictionary with filenames as keys, and MFCC arrays as values.
    '''

    song_mfcc_repr = {}
    try:
        filenames = os.listdir(filepath)
    except OSError:
        print("No such directory. Please Enter a valid directory.")
        sys.exit(1)
    for fname in filenames:
        song_mfcc_repr[fname] = parse_wav(fname, n_mfcc)
    return song_mfcc_repr


def array_to_wav(filename, time_series_data, sample_rate, filepath=None):
    '''
    Converts an output array of time series data to a wav file.

    Arguments:
        filename         - what to name the output file
        time_series_data - Numpy array with music data in a time series format.
        sample_rate      - The sample rate used for the music.

    Returns:
        None. Also saves a file.
    '''
    # To test that it is outputting properly
    if filepath is None:
        filepath = "./data/output_wavs"

    try:
        # If the directory you want to put the file in doesn't exist, create it
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        filepath += filename
        # This should output a wav file correctly. maybe?
        librosa.output.write_wav(filepath, time_series_data, sample_rate)
    except:
        print("Could not write data to {0}".format(filepath))


if __name__ == "__main__":
    # For testing purposes
    # np.set_printoptions(precision=4,
    #                     linewidth=80,
    #                     threshold=np.inf,
    #                     suppress=True)
    # data, sample_rate = parse_wav(input_filename, 400)
    #
    # Sorta works, but you can't actually convert it back since
    #  we have mfcc and there's no way to get mfcc back to wav, directly.
    #
    # array_to_wav("output1.wav", data, sample_rate)
    print("Woo. I'm a file. You should uncomment stuff if you're testing...")
