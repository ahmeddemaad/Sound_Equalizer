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
import simpleaudio as sa
import altair as alt
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
    file = st.file_uploader(label='Upload your sound', label_visibility='hidden')
    return file

    #-------------------------------------------------------------------reading Audio -------------------------------------------------------------------#


def Sound_loading(file,speed_rate):
    loaded_sound_file, sampling_rate = librosa.load(file, sr=None)
   
    # speed_rate=st.slider(label="speed Rate",min_value= 0.1 , max_value=2.0 ,value=1.0)
    loaded_sound_file = librosa.effects.time_stretch(loaded_sound_file, rate=speed_rate)
    return loaded_sound_file, sampling_rate

    #-------------------------------------------------------------------processing-------------------------------------------------------------------#
fig = make_subplots(
    rows=2, cols=1,shared_xaxes=True,
    subplot_titles=("Original Audio","Modified Audio"))
    
def make_chart(df, y_col, ymin, ymax,type):
    if type=="original": 
        row=1
    elif type=="modified":
        row=2
    fig.add_trace(go.Scatter(x=df['time'], y=df[y_col], mode='lines'),row=row,col=1)
    fig.update_layout(width=1200, height=500, xaxis_title='time',yaxis_title=y_col)
    fig.update_traces(line_color="#3182ce")
    st.write(fig)
    fig.data=[]
    fig.layout={}
    
def static_plot(x,y,type):
    plot_spot = st.empty()
    if type=="original": 
        row=1
    elif type=="modified":
        row=2
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines'), row=row,col=1)
    fig.update_layout(xaxis_title='time',yaxis_title='amplitude')
    fig.update_traces(line_color="#3182ce")
    st.write(fig)
# def dynamic_plot(original_x, original_y,type):
#     plot_spot = st.empty()
#     original_dataframe = {'time': original_x, 'amplitude': original_y}
#     original_df = pd.DataFrame(original_dataframe)
#     length = len(original_df)
#     original_ymax = max(original_df['amplitude'])
#     original_ymin = min(original_df['amplitude'])
#     rows_until_1sec = original_df['time'].loc[original_df['time'] <= float(1)]
#     for i in range(0, length-1, 1500):
#         original_df_tmp = original_df.iloc[i:i+len(rows_until_1sec)]
#         with plot_spot:
#             make_chart(original_df_tmp, 'amplitude', original_ymin, original_ymax,type)
#         time.sleep(0.001)
        

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
                key=i, default_value=0, step=1, min_value=-20, max_value=20,slider_color= '#3182ce',thumb_color = 'black')
            st.write(f" { e } HZ")
            if value == None:
                value = 1
            sliders_data.append(value)
    return sliders_data

def altair_plot(original_df):
    lines = alt.Chart(original_df).mark_line().encode(
            x=alt.X('0:T', axis=alt.Axis(title='Time')),
            y=alt.Y('1:Q', axis=alt.Axis(title='Amplitude'))
        ).properties(
            width=400,
            height=300
        ).interactive()
    return lines
def plot_animation(original_df):
        chart1 = alt.Chart(original_df).mark_line(color="#3182ce").encode(
            x=alt.X('time', axis=alt.Axis(title='Time')),
            # y=alt.Y('amplitude', axis=alt.Axis(title='Amplitude')),
        ).properties(
            width=500,
            height=300
        ).interactive()
        figure = chart1.encode(y=alt.Y('amplitude',axis=alt.Axis(title='Amplitude'))) | chart1.encode(y ='modified_amplitude')
        return figure


def dynamic_plot(line_plot,original_df):

    pause_btn = st.button('Pause')
    N = original_df.shape[0]  # number of elements in the dataframe
    st.write(N)
    burst = 1      # number of elements (months) to add to the plot
     # size of the current dataset
    for i in range(1, N):
                size = burst+ i    
                step_df = original_df.iloc[0:size]
                
                lines = plot_animation(step_df)
            
                line_plot = line_plot.altair_chart(lines)
                size = i + burst
                if size >= N:
                    size = N - 1
                if pause_btn:
                    size = 0
                time.sleep(.00000000001)

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
    ifft_file = sc.fft.irfft(mod)
    return ifft_file
