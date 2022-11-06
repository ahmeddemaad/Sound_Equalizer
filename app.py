import streamlit as st
import streamlit_vertical_slider as svs
from scipy.io.wavfile import read,write
from scipy.fft import rfft, irfft
import numpy as np
import altair as alt
import pandas as pd
import json
from utils import equalizer

import streamlit.components.v1 as components
import os
root_dir= os.path.dirname(os.path.abspath(__file__))
build_dir= os.path.join(root_dir,"Virtical_slider","vertical_slider","frontend","build")
_vertical_slider = components.declare_component(
    "Vertical Silder",
    path=build_dir
)

def VerticalSlider(minValue=0, maxValue=100, step=1,default=0,height=400,label=None,disabled=False,key=None):
    return _vertical_slider(minValue=minValue,maxValue=maxValue,step=step,default=default,height=height,label=label,disabled=disabled,key=key)

st.set_page_config(
    page_title="Equalizer",
    page_icon="🔊",
    layout="wide"
)
with open("modes.json") as infile:
    data = json.load(infile)
if "is_uploaded" not in st.session_state:
    st.session_state.is_uploaded=True

returned_signal= np.zeros(1000)
if "time" not in st.session_state:
    st.session_state.time=np.linspace(0,5,1000)


col1, col2, col3= st.columns([0.7,1,1])
with col1:
    mode=st.selectbox("Mode",data["modes"])
    uploader= st.file_uploader("upload wav")

col5, col6,_,col7= st.columns([0.7,0.7,1.2,0.1])

if uploader:
    with col5:
        st.write("Original Sound")
        st.audio(uploader)
    if st.session_state.is_uploaded:
        sample_rate, signal= read(uploader)
        time=signal.shape[0]/sample_rate
        st.session_state["time"]=np.linspace(0,signal.shape[0],signal.shape[0])
        mono= signal.copy()
        st.session_state["sample_rate"]=sample_rate
        st.session_state["original_signal"]=mono
        st.session_state["transformed_signal"]= rfft(mono)
        st.session_state["points_per_freq"] = len(st.session_state["transformed_signal"]) / (sample_rate / 2)
        st.session_state.is_uploaded=False
    
    gain_list=[]
    for i in range(10):
        try:
            gain_list.append(st.session_state[f"slider{i}"])
        except:
            gain_list.append(0)
    transformed= equalizer(data[mode]["sliders"],st.session_state["transformed_signal"],st.session_state["points_per_freq"],gain_list)
    returned_signal= np.asarray(irfft(transformed), dtype=np.int16)
    modified_audio=write("clean.wav",st.session_state["sample_rate"], returned_signal)
else:
    st.session_state.is_uploaded=True
    st.session_state.time=np.linspace(0,5,1000)
    

cols= st.columns([ 1 for i in range(data[mode]["num_sliders"])])
for index,i in enumerate(cols):
    with i:
        VerticalSlider(default=0.0,minValue=-12.0,maxValue=12.0,step=0.1,height=300,label=data[mode]["sliders"][index]["label"],key=f"slider{index}" )

if uploader:
    with col6:
        st.write("Modified sound")
        st.audio("clean.wav")

ploted_rec_data= pd.DataFrame({"time":st.session_state.time[::300],"signal":returned_signal[::300]})
ploted_ori_data= pd.DataFrame({"time":st.session_state.time[::300],"signal":st.session_state["original_signal"][::300]})
df1=ploted_rec_data.iloc[0:700]
df2=ploted_ori_data.iloc[0:700]
lines_rec = alt.Chart(df1).mark_line().encode(
    x=alt.X('time:T', axis=alt.Axis(title='date',labels=False)),
    y=alt.Y('signal:Q',axis=alt.Axis(title='value')),
    ).properties(
        width=600, 
        height=300
    ).configure_view(strokeWidth=0).configure_axis(grid=False, domain=False)
lines_ori = alt.Chart(df2).mark_line().encode(
    x=alt.X('time:T', axis=alt.Axis(title='date',labels=False)),
    y=alt.Y('signal:Q',axis=alt.Axis(title='value')),
    ).properties(
        width=600, 
        height=300
    ).configure_view(strokeWidth=0).configure_axis(grid=False, domain=False)

def plot_animation(df):
    lines = alt.Chart(df).mark_line().encode(
    x=alt.X('time:T', axis=alt.Axis(title='date',labels=False)),
    y=alt.Y('signal:Q',axis=alt.Axis(title='value')),
    ).properties(
        width=600, 
        height=300
    ).configure_view(strokeWidth=0).configure_axis(grid=False, domain=False)
    return lines

N = ploted_rec_data.shape[0] 
burst = 700       
line_plot_rec= col2.altair_chart(lines_rec,use_container_width=True)
line_plot_ori= col3.altair_chart(lines_ori,use_container_width=True)
start_btn = col7.button('Start')

if start_btn:
    for i in range(700,N-burst):
        step_df_rec = ploted_rec_data.iloc[i:burst+i]       
        step_df_ori = ploted_ori_data.iloc[i:burst+i]       
        lines_rec = plot_animation(step_df_rec)
        lines_ori = plot_animation(step_df_ori)
        line_plot_rec.altair_chart(lines_rec,use_container_width=True)
        line_plot_ori.altair_chart(lines_ori,use_container_width=True)
        
        
