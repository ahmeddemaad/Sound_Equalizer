import functions as fn
import music as ms
import arrhythima as ar
import VoiceChanger as vc
import IPython.display as ipd
import librosa.display
import librosa
import plotly.tools
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
from multiprocessing import Process

st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)

options = st.sidebar.radio('Tools', options=["Audio", "Music", "Vowels", "Arrhythima","Voice Changer"])

if options == 'Audio':
    # ----------------------------------------------- importing sound
    Sound = fn.Uploader()
    if Sound:
        # fn.Audio_player(Sound)
        audio_duration = fn.get_audio_duration(Sound)
        loaded_sound_file, sampling_rate = fn.Sound_loading(Sound,1)
        # make an array for time with the same length as the sampled audio file
        original_time_axis = np.linspace( 0, audio_duration, len(loaded_sound_file))
        # plot original audio in time domain (dynamic)

        amplitude, phase, rfrequency = fn.Fourier_operations(
            loaded_sound_file, sampling_rate)
        # rfrequency,amplitude= fn.magnitude_spectrum_ (amplitude,sampling_rate, 1 )
        #ax = plt.figure(figsize=(10, 8))
        List_freq_axis, List_amplitude_axis, bin_max_frequency_value = fn.bins_separation(
            rfrequency, amplitude)
        sliders_date = fn.Sliders_generation(bin_max_frequency_value)
        mod_List_amplitude_axis, empty = fn.sound_modification(
            sliders_date, List_amplitude_axis)
        modified_time_axis = np.linspace( 0, audio_duration, len(mod_List_amplitude_axis))
        phase = phase[:len(mod_List_amplitude_axis):1]
        # generate = st.button('Generate')
        ifft_file = fn.inverse_fourier(mod_List_amplitude_axis, phase)
        # generate=st.button('Generate')
        # if generate:
        song = ipd.Audio(ifft_file, rate=sampling_rate/2)
        empty.write(song)
        rfrequency = rfrequency[:len(mod_List_amplitude_axis):1]
        fn.dynamic_plot(original_time_axis.tolist(),loaded_sound_file.tolist())
        # fn.dynamic_plot(modified_time_axis.tolist(),mod_List_amplitude_axis)
        # plot original audio in time domain (static)

        # plot in frequency domain
        #plt.plot(rfrequency, mod_List_amplitude_axis, color='black')
        # st.plotly_chart(ax)
if options == 'Music':
    Music = ms.Uploader()
    if Music:
        fn.Audio_player(Music)
        loaded_sound_file, sampling_rate = fn.Sound_loading(Music,1)
        amplitude, phase, rfrequency = fn.Fourier_operations(
            loaded_sound_file, sampling_rate)
        sliders_data = ms.Sliders_generation()
        modified_amplitude, empty = ms.music_modification(
            rfrequency, amplitude, sliders_data)
        ifft_file = fn.inverse_fourier(modified_amplitude, phase)
        song = ipd.Audio(ifft_file, rate=sampling_rate/2)
        empty.write(song)
        ax = plt.figure(figsize=(10, 8))
        # plt.plot(rfrequency, modified_amplitude, color='black')
        # st.plotly_chart(ax)
    else:
        pass
if options == 'Arrhythima':
        ar.arrhythima()
if options == 'Voice Changer':
    Sound = fn.Uploader()
    if Sound:
        voice = st.sidebar.radio('Voice', options=["Deep Voice","Smooth Voice"])
        fn.Audio_player(Sound)
        if voice == "Deep Voice":
            empty = st.empty()
            empty.empty()
            speed_rate=1.4
            sampling_rate_factor = 1.4
        elif voice == "Smooth Voice":
            empty = st.empty()
            empty.empty()
            speed_rate=0.5
            sampling_rate_factor = 0.5
    loaded_sound_file, sampling_rate = vc.Voice_changer(Sound,speed_rate)
    song = ipd.Audio(loaded_sound_file, rate=sampling_rate/sampling_rate_factor)
    empty.write(song)



