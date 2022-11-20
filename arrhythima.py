import IPython.display as ipd
import librosa.display
import librosa
import time
from typing import List
import numpy as np
from requests import delete
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import soundfile as sf
import scipy as sc
from scipy.fftpack import fft
import streamlit_vertical_slider as svs
import cmath
import wave
import contextlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.misc import electrocardiogram
import functions as fn

# import streamlit_nested_layout


def arrhythima(main_column, controls_column):

    ecg = electrocardiogram()
    fs = 360
    time = np.arange(ecg.size) / fs
    amplitude, phase, rfrequency = fn.fourier_transform(ecg, fs)
    value = controls_column.slider(
        label="Arrhythmia", min_value=0, max_value=10, value=1, key=12)
    arythemia_freq = np.where((rfrequency >= 1) & (rfrequency < 5))
    for i in arythemia_freq:
        amplitude[i] = amplitude[i]*value
    modified_signal = fn.inverse_fourier(amplitude, phase)
    df = pd.DataFrame({'time': time, 'amplitude': ecg,
                      'modified_amplitude': modified_signal})
    rows_until_45sec = df.loc[df['time'] <= float(45)]
    rows_until_51sec = df.loc[df['time'] <= float(51)]
    df = df.loc[len(rows_until_45sec):len(rows_until_51sec)]
    for i in range(0, 4):
        main_column.empty().write("")

    return df, ecg, modified_signal,time
    # lines, width, height = fn.altair_plot(df, 500, 300)
    # line_plot = main_column.altair_chart(lines)
    # fn.dynamic_plot(line_plot, df, controls_column, main_column, width, height)
