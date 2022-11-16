import functions as fn
import music as ms
import arrhythima as ar
import VoiceChanger as vc
import IPython.display as ipd
import librosa.display
import librosa
import plotly.tools
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
from multiprocessing import Process
from streamlit_option_menu import option_menu
import altair as alt
from scipy import signal


st.set_page_config(layout="wide", page_title="Equalizer")
st.markdown("""
        <style>
                .css-18e3th9{
                    margin-top: -60px;
                
                    }

                .css-1qaq3qt{
                    width:100%;
                    align-items: center;
                    justify-content: center;
                }
               
               .css-1vq4p4l{
                margin-top: -79px;
                
                margin-left: -10px;
                margin-right: -10px;
               }
               .css-163ttbj{
                width:18% !important;
               }
               .css-1cc1g65{
                gap:0px;
               }
               ..css-f6bu01{
                gap:-1rem;
               }
               .css-ocqkz7{
                gap:0px;
                margin-top: 10px;
               }
               
               .css-1g7xoqr{
                
                    margin-block-start: -1.4%;
               }
                .css-1a32fsj{
                    margin-block-start: -1.4%;
                    margin-bottom: -38px;
                }
                .css-1gugvky{
                    margin-inline: -3%;
               }
               .css-ocqkz-e1tzin5v4{
                margin-inline-start: 35%;
                margin-block-end: -2.7%;
            margin-block-start: -4.5%;
            
                }
                .css-pmxsec.exg6vvm0{
                    margin-top:-10px;
                }
                .css-zakn0l{
                      margin-top: -2px;
                }
                .css-u5r6vw{
                    padding-top: 1.5rem;
                   
                    margin-top: -10px;
                }
                
                .css-u5r6vw.e16nr0p34 #$0{
                    margin-top:10px;
                }
                .stAudio{
                    margin-top:-18px;
                    margin-bottom: -20px;
                }
                .row-widget.stCheckbox{
                    margin-top:10px;
                }
                canvas.marks {
    max-width: 100%!important;
    height: auto!important;
}
                
        </style>
        """, unsafe_allow_html=True)
st.set_option('deprecation.showPyplotGlobalUse', False)

st.sidebar.title("Equalizer Controls")
options = st.sidebar.selectbox(
    'Mode', ('Audio', 'Music', 'Vowels', 'Arrhythmia', 'Voice Changer'))


controls_column, main_column=st.columns([1,2])


if options == 'Audio':
    # ----------------------------------------------- importing sound
    Sound = fn.Uploader()
    spectrogram_checkbox=st.sidebar.checkbox('Spectrogram')
    if Sound:
        if 'triangles' not in st.session_state:
            st.session_state.triangles=[0] *10
        fn.Audio_player(Sound)
        audio_duration = fn.get_audio_duration(Sound)
        loaded_sound_file, sampling_rate = fn.Sound_loading(Sound, 1)
        # make an array for time with the same length as the sampled audio file
        original_time_axis = np.linspace(
            0, audio_duration, len(loaded_sound_file))
        # plot original audio in time domain (dynamic)

        amplitude, phase, rfrequency = fn.Fourier_operations(
            loaded_sound_file, sampling_rate)
        # rfrequency,amplitude= fn.magnitude_spectrum_ (amplitude,sampling_rate, 1 )
        #ax = plt.figure(figsize=(10, 8))
        List_freq_axis, List_amplitude_axis, bin_max_frequency_value = fn.bins_separation(
            rfrequency, amplitude)
        window=fn.Triangle(bin_max_frequency_value)
       
        mod_List_amplitude_axis, empty = fn.sound_modification(
            st.session_state.triangles, List_amplitude_axis)
        modified_time_axis = np.linspace(
            0, audio_duration, len(mod_List_amplitude_axis))
        phase = phase[:len(mod_List_amplitude_axis):1]
        # fn.dynamic_plot(original_time_axis.tolist(),loaded_sound_file.tolist(),"original")
        # fn.dynamic_plot(modified_time_axis.tolist(),mod_List_amplitude_axis,"modified")
        # generate = st.button('Generate')
        ifft_file = fn.inverse_fourier(mod_List_amplitude_axis, phase)
        # generate=st.button('Generate')
        # if generate:
        song = ipd.Audio(ifft_file, rate=sampling_rate)
        empty.write(song)
        rfrequency = rfrequency[:len(mod_List_amplitude_axis):1]
        loaded_sound_file = loaded_sound_file[:len(ifft_file)]
        mod_List_amplitude_axis = mod_List_amplitude_axis[:len(ifft_file)]
        original_time_axis = original_time_axis[:len(ifft_file)]
        # st.write("ifft", ifft_file)
        # ax = plt.figure(figsize=(10, 8))

        # plt.plot(rfrequency, mod_List_amplitude_axis, color='black')
        # st.plotly_chart(ax)
        # Altair starts here
        # original_df = pd.DataFrame({'time': original_time_axis[::500], 'amplitude': loaded_sound_file[:: 500], 'modified_amplitude': ifft_file[::500]}, columns=[
        #     'time', 'amplitude', 'modified_amplitude'])

        # lines = fn.altair_plot(original_df)
        # line_plot = st.altair_chart(lines)
        # start_btn = st.button('Start')
        # ax = plt.figure(figsize=(10, 8))
        # amplitude = amplitude[:len(rfrequency)]
        # plt.plot(rfrequency, amplitude, color='black')

        # st.plotly_chart(ax)
        
        loaded_sound_file = loaded_sound_file[:len(ifft_file)]
        mod_List_amplitude_axis = mod_List_amplitude_axis[:len(ifft_file)]
        original_time_axis = original_time_axis[:len(ifft_file)]

        # Altair starts here
        resulting_df = pd.DataFrame({'time': original_time_axis[::500], 'amplitude': loaded_sound_file[:: 500], 'modified_amplitude': ifft_file[::500]}, columns=[
            'time', 'amplitude', 'modified_amplitude'])
        
        if(not spectrogram_checkbox):
            lines = fn.altair_plot(resulting_df)
            line_plot = st.altair_chart(lines)
            fn.dynamic_plot(line_plot, resulting_df)
        else:
            fn.plot_spectro(loaded_sound_file, ifft_file)
        if 'triangles' in st.session_state:
            st.session_state.triangles = fn.Sliders_generation(bin_max_frequency_value,window)
            
        # #ax = plt.figure(figsize=(10, 8))
        # amplitude = amplitude[:len(rfrequency)]
        # #plt.plot(rfrequency, amplitude, color='black')
        # #st.plotly_chart(ax)


if options == 'Music':
    Music = fn.Uploader()
    spectrogram_checkbox=st.sidebar.checkbox('Spectrogram')
    if Music:
        if 'music_sliders_data' not in st.session_state:
            st.session_state.music_sliders_data=[1]*3
            
        fn.Audio_player(Music)
        loaded_sound_file, sampling_rate = fn.Sound_loading(Music, 1)
        audio_duration = fn.get_audio_duration(Music)
        original_time_axis = np.linspace(
            0, audio_duration, len(loaded_sound_file))
        amplitude, phase, rfrequency = fn.Fourier_operations(
            loaded_sound_file, sampling_rate)
        #sliders_data = ms.Sliders_generation()
        modified_amplitude, empty = ms.music_modification(
            rfrequency, amplitude, st.session_state.music_sliders_data)
        modified_time_axis = np.linspace(
            0, audio_duration, len(modified_amplitude))
        ifft_file = fn.inverse_fourier(modified_amplitude, phase)
        
        song = ipd.Audio(ifft_file, rate=sampling_rate)
        
        empty.write(song)
        ax = plt.figure(figsize=(10, 8))

        loaded_sound_file = loaded_sound_file[:len(ifft_file)]
        mod_List_amplitude_axis = modified_amplitude[:len(ifft_file)]
        original_time_axis = original_time_axis[:len(ifft_file)]

        # Altair starts here
        resulting_df = pd.DataFrame({'time': original_time_axis[::500], 'amplitude': loaded_sound_file[:: 500], 'modified_amplitude': ifft_file[::500]}, columns=[
            'time', 'amplitude', 'modified_amplitude'])
        
        if(not spectrogram_checkbox):
            lines = fn.altair_plot(resulting_df)
            line_plot = st.altair_chart(lines)
            fn.dynamic_plot(line_plot, resulting_df)
        else:
            fn.plot_spectro(loaded_sound_file, ifft_file) 
        if 'music_sliders_data' in st.session_state:
            st.session_state.music_sliders_data = ms.Sliders_generation()
       
        #fn.static_plot(original_time_axis.tolist(), loaded_sound_file.tolist(),"original")
        # fn.static_plot(modified_time_axis.tolist(),modified_amplitude,"modified")
        # fn.dynamic_plot(original_time_axis.tolist(),loaded_sound_file.tolist(),"original")
        # fn.dynamic_plot(modified_time_axis.tolist(),modified_amplitude,"modified")
        # plt.plot(rfrequency, modified_amplitude, color='black')
        # st.plotly_chart(ax)
    else:
        pass
if options == 'Arrhythmia':
    ar.arrhythima()
if options == 'Voice Changer':
    Sound = fn.Uploader()
    spectrogram_checkbox=st.sidebar.checkbox('Spectrogram')

    if Sound:
        st.write(
            '<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        voice = st.radio(
            'Voice', options=["Deep Voice", "Smooth Voice"])
        fn.Audio_player(Sound)
        speed_rate = 1.4
        sampling_rate_factor = 1.4
        if voice == "Deep Voice":
            empty = st.sidebar.empty()
            empty.empty()
            speed_rate = 1.4
            sampling_rate_factor = 1.4
        elif voice == "Smooth Voice":
            empty = st.sidebar.empty()
            empty.empty()
            speed_rate = 0.5
            sampling_rate_factor = 0.5

        loaded_sound_file, sampling_rate = vc.Voice_changer(Sound, speed_rate)
        song = ipd.Audio(loaded_sound_file, rate=sampling_rate /
                         sampling_rate_factor)
        empty.write(song)
