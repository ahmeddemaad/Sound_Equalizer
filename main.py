import functions as fn
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
from scipy.fftpack import fft
import streamlit_vertical_slider as svs


st.set_page_config(layout="wide")

st.set_option('deprecation.showPyplotGlobalUse', False)

<<<<<<< Updated upstream
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Audio", "Music", "Vowels", "Arrhythima", "Audio conversion"])
with tab1:

    # ----------------------------------------------- importing sound

    Sound = fn.Uploader()
    if Sound:
        fn.Audio_player(Sound)
        loaded_sound_file, sampling_rate = fn.Sound_loading(Sound)
        amplitude,phase=fn.Fourier_operations(loaded_sound_file)
        frequency,amplitude= fn.magnitude_spectrum_ (amplitude,sampling_rate, 1 )
        ax = plt.figure(figsize=(10, 8))
        List_freq_axis, List_amplitude_axis=fn.bins_separation(frequency, amplitude)
        sliders_date=fn.Sliders_generation()
        mod_List_amplitude_axis,empty=fn.sound_modification(sliders_date,List_amplitude_axis)
        st.write(mod_List_amplitude_axis[0])
        phase=phase[:len(mod_List_amplitude_axis):1]
        ifft_file=fn.inverse_fourier(mod_List_amplitude_axis,phase)    # generate = st.button('Generate')
        generate=st.button('Generate')
        if generate:
            song=ipd.Audio(ifft_file,rate=sampling_rate)
            empty.write(song)
        frequency=frequency[:len(mod_List_amplitude_axis):1]
        plt.plot(frequency, mod_List_amplitude_axis, color='black')
        st.plotly_chart(ax)
=======
# ----------------------------------------------- importing sound

Sound = st.sidebar.file_uploader(label="Upload your sound")

st.audio(Sound, format="audio/wav", start_time=0)

# --------------------------------------------- Simply sampling my sound_file

sound_file , sr = librosa.load(Sound)

# --------------------------------------------- Appling fourier Transform

sound_file_fft = np.fft.fft(sound_file)

magnitude_sound_file_fft = np.abs(sound_file_fft)

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
>>>>>>> Stashed changes
