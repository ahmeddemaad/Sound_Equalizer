
import numpy as np

def Vowels_modification(frequency, amplitude, sliders_data,main_column,controls_column):
    controls_column.write("Modified Audio")
    empty = controls_column.empty()
    empty.empty()

    index_sh = np.where((frequency >= 800) & (frequency <= 5000))
    for i in index_sh:
        amplitude[i] = amplitude[i]*sliders_data[0]
    index_guitar = np.where((frequency >= 500) & (frequency <= 2000))
    for i in index_guitar:
        amplitude[i] = amplitude[i]*sliders_data[1]
    index_flute = np.where((frequency >= 500) & (frequency <= 1200))
    for i in index_flute:
        amplitude[i] = amplitude[i]*sliders_data[2]
    index_hoba = np.where((frequency >= 900) & (frequency <= 5000))
    for i in index_hoba:
        amplitude[i] = amplitude[i]*sliders_data[3]
    index_b = np.where((frequency >= 1200) & (frequency <= 5000))
    for i in index_b:
        amplitude[i] = amplitude[i]*sliders_data[4]

    return amplitude, empty