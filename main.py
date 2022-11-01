import functions as fn
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


st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Audio", "Music", "Vowels", "Arrhythima", "Audio conversion"])
with tab1:

    # ----------------------------------------------- importing sound

    Sound = fn.Uploader()
    if Sound:
        fn.Audio_player(Sound)
        loaded_sound_file, sampling_rate = fn.Sound_loading(Sound)

    fn.Sliders_generation()
