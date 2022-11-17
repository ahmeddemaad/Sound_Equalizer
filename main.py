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
                .css-qri22k{
                    visibility:hidden;
                    padding:-17.5rem 1rem;   
                }
                .css-18e3th9{
                    margin-top: -100px;
                    margin-left: -187px;
                    overflow-y:hidden;
                    
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
                gap:15px;
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
                    margin-top:-16px;
                    margin-bottom:1px;
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
                .css-af4qln h1{
                    font-size:30px;
            }
                .css-af4qln h1{
                    margin-bottom: -10px;
                }
                .css-1p46ort{
                    margin-bottom: -0.5rem;
                }
                .css-1v5hvio{
                    padding:0.1em;
                }
                audio{
                    margin-top:-24px;
                    width:100%;
                }
                .css-1ywmfj8{
                    gap:2.1rem;
                }
                .css-fg4pbf{
                    margin-left:
                }
                .css-18e3th9{
                        margin-top: -100px;
    margin-left: -71px;
                }
        </style>
        """, unsafe_allow_html=True)
st.set_option('deprecation.showPyplotGlobalUse', False)
controls_column, main_column=st.columns([1,3])
controls_column.title("Equalizer Controls")
options = controls_column.selectbox(
    'Mode', ('Audio', 'Music', 'Vowels', 'Arrhythmia', 'Voice Changer'))




if options == 'Audio':
    audio = fn.uploader(controls_column)
    spectrogram_checkbox=controls_column.checkbox('Spectrogram')
    if audio:
        # ----------- importing audio
        fn.audio_player(audio,controls_column)
        audio_duration = fn.get_audio_duration(audio)
        loaded_sound_file, sampling_rate = fn.sound_loading(audio, 1)
        original_time_axis = np.linspace(0, audio_duration, len(loaded_sound_file))
        # ------------ processing
        amplitude, phase, rfrequency = fn.fourier_transform(loaded_sound_file, sampling_rate)
        frequency_axis_list, amplitude_axis_list, bin_max_frequency_value = fn.bins_separation(rfrequency, amplitude)
        sliders_data =fn.sliders_generation(frequency_axis_list[0][-1],main_column)
        modified_amplitude_axis_list, empty = fn.sound_modification(sliders_data, amplitude_axis_list,controls_column)
        modified_time_axis = np.linspace(0, audio_duration, len(modified_amplitude_axis_list))
        phase = phase[:len(modified_amplitude_axis_list):1]
        ifft_file = fn.inverse_fourier(modified_amplitude_axis_list, phase)
        # ------------ OutPut
        song = ipd.Audio(ifft_file, rate=sampling_rate) 
        empty.write(song)
        #-------------- Dynamic plotting
        rfrequency = rfrequency[:len(modified_amplitude_axis_list):1]
        loaded_sound_file = loaded_sound_file[:len(ifft_file)]
        modified_amplitude_axis_list = modified_amplitude_axis_list[:len(ifft_file)]
        original_time_axis = original_time_axis[:len(ifft_file)]
        resulting_df = pd.DataFrame({'time': original_time_axis[::500], 'amplitude': loaded_sound_file[:: 500], 'modified_amplitude': ifft_file[::500]}, columns=[
            'time', 'amplitude', 'modified_amplitude'])
        #-------------- Spectorgram Graph
        if(not spectrogram_checkbox):
            lines = fn.altair_plot(resulting_df)
            line_plot =main_column.altair_chart(lines)
            fn.dynamic_plot(line_plot, resulting_df,controls_column)
        else:
            fn.plot_spectrogram(loaded_sound_file, ifft_file,main_column)

        

if options == 'Music':
    Music = fn.uploader(controls_column)
    spectrogram_checkbox=controls_column.checkbox('Spectrogram')
    if Music:
        if 'music_sliders_data' not in st.session_state:
            st.session_state.music_sliders_data=[]
        st.session_state.music_sliders_data = ms.sliders_generation(main_column)
            
        fn.audio_player(Music,controls_column)
        loaded_sound_file, sampling_rate = fn.sound_loading(Music, 1)
        audio_duration = fn.get_audio_duration(Music)
        original_time_axis = np.linspace(
            0, audio_duration, len(loaded_sound_file))
        amplitude, phase, rfrequency = fn.fourier_transform(
            loaded_sound_file, sampling_rate)
        
        modified_amplitude, empty = ms.music_modification(
            rfrequency, amplitude, st.session_state.music_sliders_data,controls_column)
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
            line_plot = main_column.altair_chart(lines)
            fn.dynamic_plot(line_plot, resulting_df,controls_column)
        else:
            fn.plot_spectrogram(loaded_sound_file, ifft_file,main_column) 
        
    else:
        pass
if options == 'Arrhythmia':
    ar.arrhythima(main_column,controls_column)
if options == 'Voice Changer':
    Sound = fn.uploader(controls_column)
    #spectrogram_checkbox=st.sidebar.checkbox('Spectrogram')
    if Sound:
        main_column.write(
            '<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        voice = main_column.radio(
            'Voice', options=["Low Pitch", "High Pitch"])
        fn.audio_player(Sound,controls_column)
        speed_rate = 1.4
        sampling_rate_factor = 1.4
        main_column.write("Modified Audio")
        empty = main_column.empty()
        if voice == "Low Pitch":
            empty.empty()
            speed_rate = 1.4
            sampling_rate_factor = 1.4
        else:

            empty.empty()
            speed_rate = 0.5
            sampling_rate_factor = 0.5

        loaded_sound_file, sampling_rate = vc.voice_changer(Sound, speed_rate,main_column)
        song = ipd.Audio(loaded_sound_file, rate=sampling_rate /
                         sampling_rate_factor)
        empty.write(song)

if options == 'Vowels':
    Vowels = fn.uploader(controls_column)
    if Vowels:
        # ------------- Sound Generation ---------------------
        music_sliders_data = vl.sliders_generation(main_column)
        fn.audio_player(Vowels,controls_column)
        # ------------   Sound Loading --------------------------
        loaded_sound_file, sampling_rate = fn.sound_loading(Vowels, 1)
        audio_duration = fn.get_audio_duration(Vowels)
        original_time_axis = np.linspace(0, audio_duration, len(loaded_sound_file))
        #-------------   Audio Processing -----------------------
        amplitude, phase, rfrequency = fn.fourier_transform(loaded_sound_file, sampling_rate)
        modified_amplitude, empty = vl.Vowels_modification(rfrequency, amplitude, music_sliders_data,main_column,controls_column)
        modified_time_axis = np.linspace(0, audio_duration, len(modified_amplitude))
        ifft_file = fn.inverse_fourier(modified_amplitude, phase)
        #-------------    Output          ------------------------
        song = ipd.Audio(ifft_file, rate=sampling_rate)
        empty.write(song)
        

    else:
        pass