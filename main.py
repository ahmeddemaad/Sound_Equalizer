import functions as fn
import music as ms
import arrhythima as ar
import IPython.display as ipd
import numpy as np
import streamlit as st
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

# ---------------------------------------   Mode Selection
Options = controls_column.selectbox('Mode', ('Audio', 'Music', 'Vowels', 'Arrhythmia'))
#----------------------------------------   Common functions
if Options == 'Arrhythmia':
    ar.arrhythima(main_column,controls_column)
else:    
    Audio = controls_column.file_uploader(label='Upload your sound', label_visibility='hidden')
    if Audio:
        # -----------------------  Orginal Sound
        fn.audio_player(Audio,controls_column)
        # -----------------------  Loading Sound
        Audio_duration = fn.get_audio_duration(Audio)
        loaded_sound_file, sampling_rate = fn.sound_loading(Audio, 1)
        original_time_axis = np.linspace(0, Audio_duration, len(loaded_sound_file))
        # -----------------------  Audio processing
        amplitude, phase, rfrequency = fn.fourier_transform(loaded_sound_file, sampling_rate)
        
        spectrogram_checkbox=controls_column.checkbox('Spectrogram')
        if Options == 'Audio':
            frequency_axis_list, amplitude_axis_list, bin_max_frequency_value = fn.bins_separation(rfrequency, amplitude)
            Audio_sliders_data =fn.sliders_generation(frequency_axis_list[0][-1],main_column,10)
            modified_amplitude, empty = fn.sound_modification(Audio_sliders_data, amplitude_axis_list,controls_column)
            phase = phase[:len(modified_amplitude)]
            
        if Options == 'Music':
                Audio_sliders_data =fn.sliders_generation(0,main_column,3)
                modified_amplitude, empty = ms.music_modification(rfrequency, amplitude,Audio_sliders_data,controls_column)

        if Options == 'Vowels':
                Audio_sliders_data =fn.sliders_generation(0,main_column,5)
                modified_amplitude, empty = vl.Vowels_modification(rfrequency, amplitude, Audio_sliders_data,main_column,controls_column)
        #--------------------- Sound Processing
        modified_time_axis = np.linspace(0, Audio_duration, len(modified_amplitude))
        ifft_file = fn.inverse_fourier(modified_amplitude, phase)
        #--------------------- Sound Output 
        song = ipd.Audio(ifft_file, rate=sampling_rate) 
        empty.write(song)
        #--------------------- Plotting Graphs
        resulting_df , loaded_sound_file = fn.data_preparation(loaded_sound_file,modified_amplitude,original_time_axis,ifft_file)
        if(not spectrogram_checkbox):
            lines = fn.altair_plot(resulting_df)
            line_plot =main_column.altair_chart(lines)
            fn.dynamic_plot(line_plot, resulting_df,controls_column)        
        else:
            fn.plot_spectrogram(loaded_sound_file, ifft_file,main_column)
    else:
        pass