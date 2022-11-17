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
import vowels as vl


st.set_page_config(layout="wide", page_title="Equalizer")
st.markdown("""
        <style>
                .css-18e3th9{
                    margin-top: -120px;
                    margin-left: 40px;
                    overflow-y:hidden;
                    overflow-x:hidden;
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
               .css-f6bu01{
                gap:-1rem;
               }
               .css-ocqkz7{
                gap:0px;
                margin-top: 10px;
                margin-left: 10px;
               }
               .css-12w0qpk{
                    margin-left: 16px;
               }

               .css-1g7xoqr{
                
                    margin-block-start: -1.4%;
               }
                .css-1a32fsj{
                    margin-block-start: -1.4%;
                    margin-bottom: -38px;
                }
                .css-1gugvky{
                    margin-inline: -4%;
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
                
                .css-u5r6vw.e16nr0p34 {
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
    #----------------------------------------------- importing sound-----------------------------------------------#
    audio = fn.uploader()
    spectrogram_checkbox=st.sidebar.checkbox('Spectrogram')
    if audio:
        
    
        fn.audio_player(audio)
        audio_duration = fn.get_audio_duration(audio)
        loaded_sound_file, sampling_rate = fn.sound_loading(audio, 1)
        original_time_axis = np.linspace(
            0, audio_duration, len(loaded_sound_file))
        amplitude, phase, rfrequency = fn.fourier_transform(
            loaded_sound_file, sampling_rate)
      
        frequency_axis_list, amplitude_axis_list, bin_max_frequency_value = fn.bins_separation(
            rfrequency, amplitude)
        window=fn.triangle(bin_max_frequency_value)
        
        if 'triangles' not in st.session_state:
            st.write("not in state")
            st.session_state.triangles=[]
        
        st.session_state.triangles = fn.sliders_generation(bin_max_frequency_value,window)
       
        
        modified_amplitude_axis_list, empty = fn.sound_modification(
            st.session_state.triangles, amplitude_axis_list)
        
        modified_time_axis = np.linspace(
            0, audio_duration, len(modified_amplitude_axis_list))
        phase = phase[:len(modified_amplitude_axis_list):1]

        ifft_file = fn.inverse_fourier(modified_amplitude_axis_list, phase)

        song = ipd.Audio(ifft_file, rate=sampling_rate)
        empty.write(song)
        rfrequency = rfrequency[:len(modified_amplitude_axis_list):1]
        loaded_sound_file = loaded_sound_file[:len(ifft_file)]
        modified_amplitude_axis_list = modified_amplitude_axis_list[:len(ifft_file)]
        original_time_axis = original_time_axis[:len(ifft_file)]
        loaded_sound_file = loaded_sound_file[:len(ifft_file)]
        modified_amplitude_axis_list = modified_amplitude_axis_list[:len(ifft_file)]
        original_time_axis = original_time_axis[:len(ifft_file)]

        resulting_df = pd.DataFrame({'time': original_time_axis[::500], 'amplitude': loaded_sound_file[:: 500], 'modified_amplitude': ifft_file[::500]}, columns=[
            'time', 'amplitude', 'modified_amplitude'])
        
        if(not spectrogram_checkbox):
            lines = fn.altair_plot(resulting_df)
            line_plot = st.altair_chart(lines)
            fn.dynamic_plot(line_plot, resulting_df)
        else:
            fn.plot_spectrogram(loaded_sound_file, ifft_file)

        

if options == 'Music':
    Music = fn.uploader()
    spectrogram_checkbox=st.sidebar.checkbox('Spectrogram')
    if Music:
        if 'music_sliders_data' not in st.session_state:
            st.session_state.music_sliders_data=[]
        st.session_state.music_sliders_data = ms.sliders_generation()
            
        fn.audio_player(Music)
        loaded_sound_file, sampling_rate = fn.sound_loading(Music, 1)
        audio_duration = fn.get_audio_duration(Music)
        original_time_axis = np.linspace(
            0, audio_duration, len(loaded_sound_file))
        amplitude, phase, rfrequency = fn.fourier_transform(
            loaded_sound_file, sampling_rate)
        
        modified_amplitude, empty = ms.music_modification(
            rfrequency, amplitude, st.session_state.music_sliders_data)
        modified_time_axis = np.linspace(
            0, audio_duration, len(modified_amplitude))
        ifft_file = fn.inverse_fourier(modified_amplitude, phase)
        
        song = ipd.Audio(ifft_file, rate=sampling_rate)
        
        empty.write(song)
        ax = plt.figure(figsize=(10, 8))

        loaded_sound_file = loaded_sound_file[:len(ifft_file)]
        modified_amplitude_axis_list = modified_amplitude[:len(ifft_file)]
        original_time_axis = original_time_axis[:len(ifft_file)]

        # Altair starts here
        resulting_df = pd.DataFrame({'time': original_time_axis[::500], 'amplitude': loaded_sound_file[:: 500], 'modified_amplitude': ifft_file[::500]}, columns=[
            'time', 'amplitude', 'modified_amplitude'])
        
        if(not spectrogram_checkbox):
            lines = fn.altair_plot(resulting_df)
            line_plot = st.altair_chart(lines)
            fn.dynamic_plot(line_plot, resulting_df)
        else:
            fn.plot_spectrogram(loaded_sound_file, ifft_file) 
        
    else:
        pass
if options == 'Arrhythmia':
    ar.arrhythima()
if options == 'Voice Changer':
    Sound = fn.uploader()
    #spectrogram_checkbox=st.sidebar.checkbox('Spectrogram')
    if Sound:
        st.write(
            '<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        voice = st.radio(
            'Voice', options=["Low Pitch", "High Pitch"])
        fn.audio_player(Sound)
        speed_rate = 1.4
        sampling_rate_factor = 1.4
        st.write("Modified Audio")
        empty = st.empty()
        if voice == "Low Pitch":
            empty.empty()
            speed_rate = 1.4
            sampling_rate_factor = 1.4
        else:

            empty.empty()
            speed_rate = 0.5
            sampling_rate_factor = 0.5

        loaded_sound_file, sampling_rate = vc.voice_changer(Sound, speed_rate)
        song = ipd.Audio(loaded_sound_file, rate=sampling_rate /
                         sampling_rate_factor)
        empty.write(song)

if options == 'Vowels':
    Vowels = fn.uploader()
    if Vowels:
        fn.audio_player(Vowels)
        audio_duration=fn.get_audio_duration(Vowels)
        loaded_sound_file, sampling_rate = fn.sound_loading(Vowels, 1)
        original_time_axis = np.linspace(
            0, audio_duration, len(loaded_sound_file)) 
        

        time_df=pd.DataFrame({'time': original_time_axis[::100],'amplitude': loaded_sound_file[::100]})
        certain_time_df=time_df[time_df['time']<=0.5]
        st.write(certain_time_df)
        amplitude, phase, rfrequency = fn.fourier_transform(
            loaded_sound_file, sampling_rate)
        df=pd.DataFrame({'frequency':rfrequency, 'amplitude':amplitude})
       
        
        certain_frequencies_df= df[df['frequency']>=10000]
      
        sliders_data = vl.sliders_generation()
        modified_amplitude, empty = vl.vowel_modifier(
            rfrequency, amplitude, sliders_data)
        
        ifft_file = fn.inverse_fourier(modified_amplitude, phase)
        song = ipd.Audio(ifft_file, rate=sampling_rate)
        empty.write(song)
        ax = plt.figure(figsize=(10, 8))
        plt.plot(rfrequency, modified_amplitude, color='black')
        st.plotly_chart(ax)
    else:
        pass