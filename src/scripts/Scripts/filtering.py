import numpy as np
import os
import pandas as pd
from scipy.signal import butter, filtfilt
from scipy.signal import find_peaks
import sys


def filtering(x):
    # Define filter parameters
    filtCutOff = 1
    sample = 30

    # Design a Butterworth low-pass filter
    b, a = butter(3, (2 * filtCutOff) / sample, "low")

    # Apply the filter to the input signal x using filtfilt
    media = filtfilt(b, a, x)

    return media
