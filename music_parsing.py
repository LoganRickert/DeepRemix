from __future__ import print_function
import os

from scipy.io import wavfile
import numpy as np
import librosa


def directory_to_array(filepath="./data/input_wavs", n_mfcc=40):
    '''
    Parses all wav files into Mel-Frequency Cepstrum Coefficients
    Arguments:
        filepath - Path to directory containing .wav files
        n_mfcc   - Number of Ceptrsum Coefficients to use.
    '''

    song_mfcc_repr = {}
    try:
        filenames = os.listdir(filepath)
    except OSError:
        print("No such directory. Please Enter a valid directory.")
    for fname in filenames:
        if fname[-4:] == ".wav":
            try:
                y_data, sample_rate = librosa.load(fname)
            except:
                print("Could not load file. Moving to next file.")
                continue
            #  will need to experiment with different values for n_mfcc
            song_mfcc_repr[fname] = librosa.feature.mfcc(y=y_data,
                                                         sr=sample_rate,
                                                         n_mfcc=n_mfcc)
    return song_mfcc_repr


def array_to_wav(filename, time_series_data, sample_rate):
    '''
    Converts an output array of time series data to a wav file
    Arguments:
        filename         - what to name the output file
        time_series_data - Numpy array with music data in a time series format.
        sample_rate      - The sample rate used for the music.
    '''

    filepath = "./data/output_wavs"
    filepath = os.path.join(filepath, filename)
    try:
        # This should work? maybe?
        librosa.output.write_wav(filepath, time_series_data, sample_rate)
    except:
        print("Could not write data to {0}.".format(filepath))
