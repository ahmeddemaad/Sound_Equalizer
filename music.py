import numpy as np

def music_modification(frequency, amplitude, sliders_data,controls_column):
    controls_column.write("Modified Audio")
    empty = controls_column.empty()
    empty.empty()
    index_drums = np.where((frequency >= 0) & (frequency < 1000))
    for i in index_drums:
        amplitude[i] = amplitude[i]*sliders_data[0]

    index_guitar = np.where((frequency >= 1000) & (frequency < 2700))
    for i in index_guitar:
        amplitude[i] = amplitude[i]*sliders_data[1]
    index_flute = np.where((frequency >= 2700) & (frequency < 25000))
    for i in index_flute:
        amplitude[i] = amplitude[i]*sliders_data[2]
    return amplitude, empty,
