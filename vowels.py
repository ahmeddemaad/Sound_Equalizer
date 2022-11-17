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


def sliders_generation(main_column):
    columns = main_column.columns(5)
    sliders_data = []
    vowels=[" ' SH ' sound","  ' O ' sound","  ' A ' sound","  ' R ' sound","  ' B ' sound"]
    for i in range(0, 5):
        with columns[i]:

            value = svs.vertical_slider(
                key=i, default_value=1, step=1, min_value=0, max_value=20, slider_color= '#3182ce',thumb_color = 'black')
            if value == None:
                value = 1
            sliders_data.append(value)
            st.write(vowels[i])
    return sliders_data



def Vowels_modification(frequency, amplitude, sliders_data,main_column,controls_column):
    controls_column.write("Modified Audio")
    empty = controls_column.empty()
    empty.empty()

    index_sh = np.where((frequency >= 800) & (frequency <= 5000))
    for i in index_sh:
        amplitude[i] = amplitude[i]*sliders_data[0]
    index_guitar = np.where((frequency >= 500) & (frequency <= 2000))
    for i in index_guitar:
        amplitude[i] = amplitude[i]*sliders_data[1]
    index_flute = np.where((frequency >= 500) & (frequency <= 1200))
    for i in index_flute:
        amplitude[i] = amplitude[i]*sliders_data[2]
    index_hoba = np.where((frequency >= 900) & (frequency <= 5000))
    for i in index_hoba:
        amplitude[i] = amplitude[i]*sliders_data[3]
    index_b = np.where((frequency >= 1200) & (frequency <= 5000))
    for i in index_b:
        amplitude[i] = amplitude[i]*sliders_data[4]

    return amplitude, empty