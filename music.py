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
    instruments=["Drum","Guitar","Flute"]
    columns = main_column.columns(3)
    sliders_data = []
    for i in range(0, 3):
        with columns[i]:
            value = svs.vertical_slider(
                key=i, default_value=1, step=1, min_value=0, max_value=20, slider_color= '#3182ce',thumb_color = 'black')
            if value == None:
                value = 1
            sliders_data.append(value)
            st.write(instruments[i])
    return sliders_data


def music_modification(frequency, amplitude, sliders_data,controls_column):
    controls_column.write("Modified Audio")
    empty = controls_column.empty()
    empty.empty()
    index_drums = np.where((frequency >= 0) & (frequency < 1000))

    for i in index_drums:
        amplitude[i] = amplitude[i]*sliders_data[0]

    index_guitar = np.where((frequency >= 1000) & (frequency < 2700))
    for i in index_guitar:
        amplitude[i] = amplitude[i]*sliders_data[1]
    index_flute = np.where((frequency >= 2700) & (frequency < 25000))
    for i in index_flute:
        amplitude[i] = amplitude[i]*sliders_data[2]
    return amplitude, empty,
