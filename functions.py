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
import cmath
#-------------------------------------------------------------------player for audio-------------------------------------------------------------------#


def Audio_player(file):
    st.audio(file, format="audio/wav", start_time=0)

    #-------------------------------------------------------------------Uploaderr-------------------------------------------------------------------#


def Uploader():

    file = st.file_uploader(label="Upload your sound")
    return file

    #-------------------------------------------------------------------reading Audio -------------------------------------------------------------------#


def Sound_loading(file):
    loaded_sound_file, sampling_rate = librosa.load(file)
    return loaded_sound_file, sampling_rate

    #-------------------------------------------------------------------processing-------------------------------------------------------------------#


def Fourier_operations(loaded_sound_file):
    fft_file = np.fft.fft(loaded_sound_file)
    amplitude= np.abs(fft_file)
    phase =np.angle(fft_file)
    # frequency=fft.fftfreq()
    mod=np.multiply(amplitude,np.exp(1j*phase))
    ifft_file=sc.ifft(mod)
    return ifft_file,amplitude,phase

def magnitude_spectrum_(amplitude, sr, f_ratio):
    frequency = np.linspace(0, sr, len(amplitude))
    number_frequency_bins = int(len(frequency) * f_ratio)
    frequency = frequency[:number_frequency_bins]
    amplitude = amplitude[:number_frequency_bins]
    return frequency, amplitude


#-------------------------------------------------------------------bins_seperation-------------------------------------------------------------------#


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
#-------------------------------------------------------------------sliders-generation-------------------------------------------------------------------#


def Sliders_generation():
    columns = st.columns(10)
    sliders_data = []

    for i in range(0, 10):
        with columns[i]:
            value = svs.vertical_slider(
                key=i, default_value=0, step=1, min_value=-20, max_value=20)
            if value == None:
                value = 0
            sliders_data.append(value)
    return sliders_data
    #-------------------------------------------------------------------modification-------------------------------------------------------------------#

    #     global empty
    #     empty = st.empty()

    # def bins_modification(empty, List_freq_axis, List_amplitude_axis):
    #         empty.empty()
    #         mod_List_amplitude_axis = []
    #         i = 0
    #         while(i < 10):
    #             Amplitude = slider(i)
    #             mod_List_amplitude_axis.append(List_amplitude_axis[i]*Amplitude)
    #             i = i+1
    #         return mod_List_amplitude_axis
    #-------------------------------------------------------------------sliders-generate-------------------------------------------------------------------#

    # def slider(i):
    #     x = st.slider(min_value=0, max_value=20,
    #                     key=i, label='saba7o', value=1)
    #     return x

    #-------------------------------------------------------------------loading problem-------------------------------------------------------------------#

    # generate = st.button('Generate')

    # if generate:
    #     empty.write(song)
