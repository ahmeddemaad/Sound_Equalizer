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

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Audio", "Music", "Vowels", "Arrhythima", "Audio conversion"])
with tab1:

    # ----------------------------------------------- importing sound

    Sound = fn.Uploader()
    if Sound:
        fn.Audio_player(Sound)
        loaded_sound_file, sampling_rate = fn.Sound_loading(Sound)
        amplitude,phase,rfrequency=fn.Fourier_operations(loaded_sound_file,sampling_rate)
        # rfrequency,amplitude= fn.magnitude_spectrum_ (amplitude,sampling_rate, 1 )
        ax = plt.figure(figsize=(10, 8))
        List_freq_axis, List_amplitude_axis,bin_max_frequency_value=fn.bins_separation(rfrequency, amplitude)
        sliders_date=fn.Sliders_generation(bin_max_frequency_value)
        mod_List_amplitude_axis,empty=fn.sound_modification(sliders_date,List_amplitude_axis)
        phase=phase[:len(mod_List_amplitude_axis):1]
        ifft_file=fn.inverse_fourier(mod_List_amplitude_axis,phase)    # generate = st.button('Generate')
        # generate=st.button('Generate')
        # if generate:
        song=ipd.Audio(ifft_file,rate=sampling_rate/2)
        empty.write(song)
        rfrequency=rfrequency[:len(mod_List_amplitude_axis):1]
        # plt.plot(rfrequency, mod_List_amplitude_axis, color='black')
        # st.plotly_chart(ax)
