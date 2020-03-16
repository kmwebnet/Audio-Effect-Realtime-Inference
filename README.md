# Audio-Effect-Realtime-Inference
NNabla train model(.nnp) executable that you can run on Raspberry pi 3B+,Jetson Nano.

# Usage  
At first, you need to find your audio device by detect.py.

example for Jetson Nano :


{'index': 0, 'structVersion': 2, 'name': 'tegra-hda: HDMI 0 (hw:0,3)', 'hostApi': 0, 'maxInputChannels': 0, 'maxOutputChannels': 8, 'defaultLowInputLatency': -1.0, 'defaultLowOutputLatency': 0.005804988662131519, 'defaultHighInputLatency': -1.0, 'defaultHighOutputLatency': 0.034829931972789115, 'defaultSampleRate': 44100.0}
{'index': 1, 'structVersion': 2, 'name': 'tegra-snd-t210ref-mobile-rt565x: - (hw:1,0)', 'hostApi': 0, 'maxInputChannels': 16, 'maxOutputChannels': 16, 'defaultLowInputLatency': 0.008707482993197279, 'defaultLowOutputLatency': 0.008707482993197279, 'defaultHighInputLatency': 0.034829931972789115, 'defaultHighOutputLatency': 0.034829931972789115, 'defaultSampleRate': 44100.0}
{'index': 2, 'structVersion': 2, 'name': 'tegra-snd-t210ref-mobile-rt565x: - (hw:1,1)', 'hostApi': 0, 'maxInputChannels': 16, 'maxOutputChannels': 16, 'defaultLowInputLatency': 0.008707482993197279, 'defaultLowOutputLatency': 0.008707482993197279, 'defaultHighInputLatency': 0.034829931972789115, 'defaultHighOutputLatency': 0.034829931972789115, 'defaultSampleRate': 44100.0}


example for Raspberry Pi:

{'index': 0, 'structVersion': 2, 'name': 'bcm2835 ALSA: IEC958/HDMI (hw:0,1)', 'hostApi': 0, 'maxInputChannels': 0, 'maxOutputChannels': 8, 'defaultLowInputLatency': -1.0, 'defaultLowOutputLatency': 0.0016099773242630386, 'defaultHighInputLatency': -1.0, 'defaultHighOutputLatency': 0.034829931972789115, 'defaultSampleRate': 44100.0}
{'index': 1, 'structVersion': 2, 'name': 'bcm2835 ALSA: IEC958/HDMI1 (hw:0,2)', 'hostApi': 0, 'maxInputChannels': 0, 'maxOutputChannels': 8, 'defaultLowInputLatency': -1.0, 'defaultLowOutputLatency': 0.0016099773242630386, 'defaultHighInputLatency': -1.0, 'defaultHighOutputLatency': 0.034829931972789115, 'defaultSampleRate': 44100.0}
{'index': 2, 'structVersion': 2, 'name': 'snd_rpi_simple_card: simple-card_codec_link snd-soc-dummy-dai-0 (hw:1,0)', 'hostApi': 0, 'maxInputChannels': 2, 'maxOutputChannels': 2, 'defaultLowInputLatency': 0.005804988662131519, 'defaultLowOutputLatency': 0.005804988662131519, 'defaultHighInputLatency': 0.034829931972789115, 'defaultHighOutputLatency': 0.034829931972789115, 'defaultSampleRate': 44100.0}
{'index': 3, 'structVersion': 2, 'name': 'dmix', 'hostApi': 0, 'maxInputChannels': 0, 'maxOutputChannels': 2, 'defaultLowInputLatency': -1.0, 'defaultLowOutputLatency': 0.021333333333333333, 'defaultHighInputLatency': -1.0, 'defaultHighOutputLatency': 0.021333333333333333, 'defaultSampleRate': 48000.0}


you need to set index number into this "predict-realtime.py" code.
