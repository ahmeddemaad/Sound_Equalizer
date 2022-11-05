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


def Voice_changer(file,speed_rate):
    loaded_sound_file, sampling_rate = librosa.load(file, sr=None)
    loaded_sound_file = librosa.effects.time_stretch(loaded_sound_file, rate=speed_rate)
    return loaded_sound_file ,sampling_rate