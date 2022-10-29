import IPython.display as ipd
import librosa.display
import librosa
from time import time
from typing import List
import numpy as np
from requests import delete
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import soundfile as sf
import scipy as sc


st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)

# ----------------------------------------------- importing sound

Sound = st.sidebar.file_uploader(label="Upload your sound")

st.audio(Sound, format="audio/wav", start_time=0)

# --------------------------------------------- Simply sampling my sound_file

sound_file, sr = librosa.load(Sound)

# --------------------------------------------- Appling fourier Transform

sound_file_fft = np.fft.fft(sound_file)

magnitude_sound_file_fft = sound_file_fft.astype(float)

sound_file_ifft=np.fft.ifft(sound_file_fft)

magnitude_sound_ifft=np.fft.ifft(magnitude_sound_file_fft)

# ---------------------------------------------

global empty
empty = st.empty()

def magnitude_spectrum_(signal, sr, f_ratio):
    ft = np.fft.fft(signal)
    magnitude_spectrum = np.abs(ft)
    frequency = np.linspace(0, sr, len(magnitude_spectrum))
    number_frequency_bins = int(len(frequency) * f_ratio)
    frequency = frequency[:number_frequency_bins]
    magnitude_spectrum = magnitude_spectrum[:number_frequency_bins]
    return frequency, magnitude_spectrum

def bins_separation(frequency, magnitude_spectrum):
    List_freq_axis = []
    List_amplitude_axis = []
    bin_max_frequency_value = int(len(frequency)/10)
    i = 0
    while(i < 10):
        List_freq_axis.append(
            frequency[i*bin_max_frequency_value: (i+1)*bin_max_frequency_value])
        List_amplitude_axis.append(
            magnitude_spectrum[i*bin_max_frequency_value:(i+1)*bin_max_frequency_value])
        i = i+1
    return List_freq_axis, List_amplitude_axis


def bins_modification(empty,List_freq_axis, List_amplitude_axis):
    empty.empty()
    mod_List_amplitude_axis = []
    i = 0
    while(i < 10):
        Amplitude = slider(i)
        mod_List_amplitude_axis.append(List_amplitude_axis[i]*Amplitude)
        i = i+1
    return mod_List_amplitude_axis


def slider(i):
    x = st.slider(min_value=0, max_value=20, key=i, label='saba7o', value=1)
    return x

#-----------------------------------------------------------------------------

frequency, magnitude_spectrum = magnitude_spectrum_(sound_file, sr, 1)

List_freq_axis, List_amplitude_axis = bins_separation(frequency, magnitude_spectrum)

mod_List_amplitude_axis = bins_modification(empty,List_freq_axis, List_amplitude_axis)

mod_List_amplitude_axis = list(itertools.chain.from_iterable(mod_List_amplitude_axis))

mod_List_amplitude_axis_time = sc.fft.ifft(mod_List_amplitude_axis)

# ----------------------------------------------------------------------------

x=sound_file_ifft.astype(float)
y=magnitude_sound_ifft.astype(float)
song = ipd.Audio(y, rate=sr)

st.write(x)
st.write(y)
st.write(mod_List_amplitude_axis_time[1])
st.write(sound_file)

generate=st.button('Generate')
delete=st.button('delete')

if generate:
    empty.write(song)