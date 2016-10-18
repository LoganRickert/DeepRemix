import numpy as np
import os
import sys
from nose.tools import assert_equal
import pytest


# Still need to test directory_to_wav
def test_music_parsing_with_good_input():
    fname1 = "./data/input_wavs/got_s1e1_bastard.wav"
    fname2 = "output.wav"
    n_mfcc = 400
    # need to figure out if it's possible to go from mfcc -> wav
    # so that we can test turning it back into the original piece

    # create a temporary directory to make sure there is actually output.
    os.mkdir("./data/temp_output")
    assert len(os.listdir("./data/temp_output")) == 0

    # check that data is the right shape
    data, sample_rate = parse_wav(fname1, n_mfcc)
    assert np.shape(data) == (n_mfcc, 999)
    assert sample_rate > 0

    # write garbage wav to temp output_directory, ./data/ temp_output
    fname2 = os.path.join("./data/temp_output", fname2)
    array_to_wav(fname2, data, sample_rate)
    assert len(os.listdir("./data/temp_output")) != 0

    # delete temp directory
    shutil.rmtree("./data/temp_output", ignore_errors=False, onerror=None)
    # os.rmdir("./data/temp_output")


def test_music_parsing_no_input():
    # testing parse_wav
    with pytest.raises(SystemExit) as e_info:
        data, sr = parse_wav("fname.wav")

    data2, sr2 = parse_wav("totally_a_wav.jpg")

    assert data2 == np.array([])
    assert sr2 < 0

    with pytest.raises(SystemExit) as e_info:
        directory_to_array("./totally_a_directory.jpg")

    # need to test dir->array with no input at all, with wrong types,
    # an empty directory, a directory with no wav files,
    #  a directory with all wav files,

    # need to test array -> wav with no input, with a bad filename,
    #  with bad data, with a bad sample rate, with a bad filepath,

    # there's probably more test cases to consider later...
