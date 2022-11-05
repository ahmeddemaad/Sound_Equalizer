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

#-------------------------------------------------------------------player for audio-------------------------------------------------------------------#


def Audio_player(file):
    st.audio(file, format="audio/wav", start_time=0)

    #-------------------------------------------------------------------Uploaderr-------------------------------------------------------------------#


def get_audio_duration(file):
    with contextlib.closing(wave.open(file.name, 'r')) as file:
        frames = file.getnframes()
        rate = file.getframerate()
        duration = frames / float(rate)
        return duration


def Uploader():
    file = st.file_uploader(label="Upload your sound")
    return file

    #-------------------------------------------------------------------reading Audio -------------------------------------------------------------------#


def Sound_loading(file,speed_rate):
    loaded_sound_file, sampling_rate = librosa.load(file, sr=None)
    # speed_rate=st.slider(label="speed Rate",min_value= 0.1 , max_value=2.0 ,value=1.0)
    loaded_sound_file = librosa.effects.time_stretch(loaded_sound_file, rate=speed_rate)
    return loaded_sound_file, sampling_rate

    #-------------------------------------------------------------------processing-------------------------------------------------------------------#


def make_chart(df, y_col, ymin, ymax):
    fig = make_subplots(
    rows=2, cols=1,
    subplot_titles=("Original Audio","Modified Audio"))

    fig.add_trace(go.Scatter(x=df['time'], y=df[y_col], mode='lines'),row=1,col=1)
    fig.update_layout(width=900, height=570, xaxis_title='time',yaxis_title=y_col)
    st.write(fig)


def dynamic_plot(x, y):
    plot_spot = st.empty()
    dataframe = {'time': x, 'amplitude': y}
    df = pd.DataFrame(dataframe)

    length = len(df)
    ymax = max(df['amplitude'])
    ymin = min(df['amplitude'])

    rows_until_1sec = df['time'].loc[df['time'] <= float(1)]
    for i in range(0, length-1, 500):
        df_tmp = df.iloc[i:i+len(rows_until_1sec)]
        with plot_spot:
            make_chart(df_tmp, 'amplitude', ymin, ymax)
        time.sleep(0.001)


def Fourier_operations(loaded_sound_file, sampling_rate):

    fft_file = sc.fft.rfft(loaded_sound_file)
    amplitude = np.abs(fft_file)
    phase = np.angle(fft_file)
    frequency = sc.fft.rfftfreq(len(loaded_sound_file), 1/sampling_rate)
    return amplitude, phase, frequency

#-------------------------------------------------------------------bins_seperation-------------------------------------------------------------------#


def bins_separation(frequency, amplitude):
    List_freq_axis = []
    List_amplitude_axis = []
    bin_max_frequency_value = int(len(frequency)/10)
    i = 0
    while(i < 10):
        List_freq_axis.append(
            frequency[i*bin_max_frequency_value: (i+1)*bin_max_frequency_value])
        List_amplitude_axis.append(
            amplitude[i*bin_max_frequency_value:(i+1)*bin_max_frequency_value])
        i = i+1
    return List_freq_axis, List_amplitude_axis, bin_max_frequency_value
#-------------------------------------------------------------------sliders-generation-------------------------------------------------------------------#


def Sliders_generation(bin_max_frequency_value):
    columns = st.columns(10)
    sliders_data = []

    for i in range(0, 10):
        with columns[i]:
            e = (i+1)*bin_max_frequency_value
            value = svs.vertical_slider(
                key=i, default_value=1, step=1, min_value=-20, max_value=20)
            st.write(f" { e } HZ")
            if value == None:
                value = 1
            sliders_data.append(value)
    return sliders_data


def sound_modification(sliders_data, List_amplitude_axis):
    empty = st.empty()
    empty.empty()
    modified_bins = []
    for i in range(0, 10):
        modified_bins.append(sliders_data[i]* List_amplitude_axis[i])
    mod_List_amplitude_axis = list(itertools.chain.from_iterable(modified_bins))
    return mod_List_amplitude_axis, empty


def inverse_fourier(mod_List_amplitude_axis, phase):
    mod = np.multiply(mod_List_amplitude_axis, np.exp(1j*phase))
    ifft_file = sc.ifft(mod)
    return ifft_file
