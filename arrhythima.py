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

def arrhythima():
    ecg = electrocardiogram()

    fs = 360
    time = np.arange(ecg.size) / fs

    fourier_x_axis = sc.fft.rfftfreq(len(ecg), (time[1]-time[0]))
    fourier_y_axis = sc.fft.rfft(ecg)

    points_per_freq = len(fourier_x_axis) / (fourier_x_axis[-1])

    value = st.slider(label="Arrhythimia" ,min_value=0 ,max_value=10 ,value=1 ,key=12)

    fourier_y_axis[int(points_per_freq*1)   :int(points_per_freq* 5)] *= value

    modified_signal         = sc.fft.irfft(fourier_y_axis) 

    fig, axs = plt.subplots()
    fig.set_size_inches(14,5)

    plt.plot(time, (modified_signal))
    plt.xlabel("Time in s")
    plt.ylabel("ECG in mV")
    plt.xlim(45, 51)

    st.plotly_chart(fig)