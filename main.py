from time import time
from typing import List
import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import itertools


st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)


import librosa
import librosa.display
import IPython.display as ipd

# import thinkdsp
# import thinkplot


# ----------------------------------------------- importing sound

Sound = st.sidebar.file_uploader(label="Upload your sound")
# st.write(Sound.name)
st.audio(Sound, format="audio/wav", start_time=0)

#--------------------------------------------- Simply sampling my sound_file

sound_file , sr = librosa.load(Sound)              # sr: sampling rate ------- here the function does sampling to our file by a specific rate which is sr ( total samples per sec)
st.write(sound_file)                      #Total number of samples in my sound_file
#--------------------------------------------- Appling fourier Transform
sound_file_fft=np.fft.fft(sound_file)
# st.write(sound_file_fft[0])             # we actually move from time domain to frequency domain
magnitude_sound_file_fft=np.abs(sound_file_fft)
# st.write(sound_file_fft.shape,sound_file_fft[0],magnitude_sound_file_fft)
#---------------------------------------------

def magnitude_spectrum_(signal ,sr ,f_ratio):
    ft =np.fft.fft(signal)
    magnitude_spectrum=np.abs(ft)
    frequency =np.linspace(0,sr,len(magnitude_spectrum)) 
    number_frequency_bins = int(len(frequency) * f_ratio)
    frequency=frequency[:number_frequency_bins]
    magnitude_spectrum=magnitude_spectrum[:number_frequency_bins]
    return frequency,magnitude_spectrum

frequency,magnitude_spectrum= magnitude_spectrum_ (sound_file,sr, 0.5 )

ax = plt.figure(figsize=(10, 8))
plt.plot(frequency, magnitude_spectrum, color='black')
st.plotly_chart(ax)


def bins_separation(frequency,magnitude_spectrum):
    List_freq_axis=[]
    List_amplitude_axis=[]
    bin_max_frequency_value =int(len(frequency)/10)
    i=0
    while(i<10):
        List_freq_axis.append(frequency [ i*bin_max_frequency_value : (i+1)*bin_max_frequency_value] )
        List_amplitude_axis.append(magnitude_spectrum [i*bin_max_frequency_value:(i+1)*bin_max_frequency_value])
        i=i+1
    return List_freq_axis,List_amplitude_axis

List_freq_axis,List_amplitude_axis = bins_separation(frequency,magnitude_spectrum)



def bins_modification(List_freq_axis,List_amplitude_axis):
    mod_List_amplitude_axis=[]
    i=0
    while(i<10):
        Amplitude=slider(i)
        mod_List_amplitude_axis.append(List_amplitude_axis[i]*Amplitude)
        i=i+1
    return mod_List_amplitude_axis

def slider(i):
    x = st.slider(min_value=0,max_value=20,key=i,label='saba7o' , value=1)
    return x

mod_List_amplitude_axis=bins_modification(List_freq_axis,List_amplitude_axis)

# result = sum(mod_List_amplitude_axis, [])


mod_List_amplitude_axis=list(itertools.chain.from_iterable(mod_List_amplitude_axis))

ax = plt.figure(figsize=(10, 8))
frequency=frequency[0:len(mod_List_amplitude_axis)]
plt.plot(frequency, mod_List_amplitude_axis, color='black')
st.plotly_chart(ax)

mod_List_amplitude_axis_time = np.fft.ifft(mod_List_amplitude_axis)

hamada=ipd.Audio(mod_List_amplitude_axis_time, rate=sr)
st.write(hamada)

# st.write(result.shape)
# st.write(result)
# st.write(List_amplitude_axis[0])
# st.write(mod_List_amplitude_axis[0])
# st.write(List_amplitude_axis[2])
# st.write(mod_List_amplitude_axis[2])

# duration = librosa.get_duration(sound_file,sr)  # getting the time duration of my file
# st.write(sound_file,sr,duration)  

# fig, ax = plt.subplots()
# st.write(librosa.display.waveshow(sound_file, sr=sr, x_axis='s'))
# librosa.display.waveshow(sound_file, sr=sr, x_axis='s')



# st.pyplot()


# D = librosa.stft(y)
# times=librosa.times_like(D,)
# ax.plot(times,y)
# st.plotly_chart(fig)
# st.write(times)
# st.write(len(times))
# st.write(y)
# st.write(len(y))



