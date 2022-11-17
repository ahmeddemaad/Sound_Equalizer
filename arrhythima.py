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
import streamlit_nested_layout


def arrhythima(main_column,controls_column):
    ''' if 'arrhythmia_slider' not in st.session_state:
        st.session_state.arrhythmia_slider=1 '''
    col1,col2=main_column.columns([1,.001])
    ecg = electrocardiogram()
    fs = 360
    time = np.arange(ecg.size) / fs

    fourier_x_axis = sc.fft.rfftfreq(len(ecg), (time[1]-time[0]))
    fourier_y_axis = sc.fft.rfft(ecg)
    
    value = controls_column.slider(label="Arrhythmia", min_value=0,max_value=10, value=1, key=12)
    points_per_freq = len(fourier_x_axis) / (fourier_x_axis[-1])
    
    fourier_y_axis[int(points_per_freq*1):int(points_per_freq * 5)] *= value
    modified_signal = sc.fft.irfft(fourier_y_axis)
    df=pd.DataFrame({'time':time, 'amplitude':modified_signal})
    with col1:
        lines = fn.altair_plot(df)
        line_plot = st.altair_chart(lines)
        fn.dynamic_plot(line_plot, df,controls_column)
   
  #'''   st.write( st.session_state.arrhythmia_slider) '''