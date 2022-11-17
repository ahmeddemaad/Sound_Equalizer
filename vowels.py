import streamlit as st
import streamlit_vertical_slider as svs
import numpy as np
import scipy as sc

def sliders_generation():
    columns = st.columns(10)
    sliders_data = []

    for i in range(0, 10):
        with columns[i]:

            value = svs.vertical_slider(
                key=i, default_value=0, step=1, min_value=-20, max_value=20,slider_color= '#3182ce',thumb_color = 'black')
            
            if value == None:
                value = 1
            sliders_data.append(value)
    
    return sliders_data


def Uploader():
    file = st.file_uploader(label="Upload your sound", key=1)
    return file


def vowel_modifier(frequency, amplitude, sliders_data):
    empty = st.empty()
    empty.empty()
    # index_a = np.where((frequency >= 0) & (frequency < 1000))
    # f1 = 
    #-------------------------------------------------------------------a vowel-------------------------------------------------------------------#
    f1_holder = np.where((frequency >= 507) & (frequency <= 1521))
    f2_holder = np.where((frequency >= 2536) & (frequency <= 3550))
    # f3_holder = np.where((frequency >= 2835) & (frequency <= 3559))

    f1 = f1_holder[0]
    f2 = f2_holder[0]
    # f3 = f3_holder[0]

    # j = 0
    # for i in f1:
    #     while j < len(f1):
    #         frequency1[j] = frequency[i]
    #         j = j + 1
    #         # break
    # for i in f2:
    #     while j <len(f2):
    #         frequency2[j] = frequency[i]
    #         j = j + 1
    #         # break

    f1_wave = sc.stats.norm.pdf(frequency[f1], 1014, 1521 - 1014)
    f2_wave = sc.stats.norm.pdf(frequency[f2], 3043, 3550 - 3043)
    # f3_wave = sc.stats.norm.pdf(f3, 3199, 3559 - 2835)

    # index_a = np.concatenate((f1, f2, f3))
    index_a = np.concatenate(([frequency[f1]], [frequency[f2]]), axis=0)

    # index_a = f1 + f2 + f3
    # f1_flag = True
    # f2_flag = True
    # f3_flag = True
    # st.write(amplitude)

    for i in index_a:
        # amplitude[i] = amplitude[i]*sliders_data[0]
        if i in f1:
            # while (f1_flag):
            amplitude[i] = f1_wave[i]*sliders_data[0]
                # for j in range(len(f1)):
                #     amplitude[f1[j]] = amplitude1[j]
                # f1_flag = False
        elif i in f2:
            # while (f2_flag):
            amplitude[i] = f2_wave[i]*sliders_data[0]
                # for j in range(len(f2)):
                #     amplitude[f2[j]] = amplitude2[j]
                # f2_flag = False
        # f1_flag = True
        # f2_flag = True
    # st.write(amplitude)
    #-------------------------------------------------------------------i vowel-------------------------------------------------------------------#
    # f1_holder = np.where((frequency >= 692) & (frequency <= 1218))
    # f2_holder = np.where((frequency >= 1218) & (frequency <= 1693))
    # # f3_holder = np.where((frequency >= 2835) & (frequency <= 3559))

    # f1 = f1_holder[0]
    # f2 = f2_holder[0]
    # # f3 = f3_holder[0]

    # f1_wave = sc.stats.norm.pdf(f1, 961, 1218 - 692)
    # f2_wave = sc.stats.norm.pdf(f2, 1434, 1693 - 1218)
    # # f3_wave = sc.stats.norm.pdf(f3, 3199, 3559 - 2835)

    # # index_a = np.concatenate((f1, f2, f3))
    # index_a = np.concatenate((f1, f2))

    # # index_a = f1 + f2 + f3
    # f1_flag = True
    # f2_flag = True
    # # f3_flag = True

    # for i in index_a:
    #     # amplitude[i] = amplitude[i]*sliders_data[0]
    #     if i in f1:
    #         while (f1_flag):
    #             amplitude1 = f1_wave*sliders_data[0]
    #             for j in range(len(f1)):
    #                 amplitude[f1[j]] = amplitude1[j]
    #             f1_flag = False
    #     elif i in f2:
    #         while (f2_flag):
    #             amplitude2 = f2_wave*sliders_data[0]
    #             for j in range(len(f2)):
    #                 amplitude[f2[j]] = amplitude2[j]
    #             f2_flag = False

        # else:
        #     while (f3_flag):
        #         amplitude3 = f3_wave*sliders_data[0]
        #         for j in range(len(f3)):
        #             amplitude[j] = amplitude3[j]
        #         f3_flag = False

    # index_guitar = np.where((frequency >= 1000) & (frequency < 2700))
    # for i in index_guitar:
    #     amplitude[i] = amplitude[i]*sliders_data[1]
    # index_flute = np.where((frequency >= 2700) & (frequency < 25000))
    # for i in index_flute:
    #     amplitude[i] = amplitude[i]*sliders_data[2]

    # index_unwanted_amplitudes = np.where((amplitude < 200))
    # st.write(index_unwanted_amplitudes)
    # for i in index_unwanted_amplitudes:
    #     amplitude[i] = 0
    # st.write(amplitude)
    return amplitude, empty