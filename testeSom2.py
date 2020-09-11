from scipy.io.wavfile import read
from scipy.fftpack import fft, ifft
from matplotlib.mlab import specgram
import matplotlib.pyplot as plt
import numpy as np
import wave
 
#https://en.wikipedia.org/wiki/Special_information_tones
freq_913 = 913      #low
freq_1370 = 1370    #low
freq_1776 = 1776    #low
 
short_duration = 0.276          #short duration 276 ms
long_duration = 0.380           #long duration 380 ms
interval = 0.004                #interval between tones.
 
path_ic = "IC_SIT.wav"
path_ro1 = "RO'_SIT.wav"
path_rec = "recording.wav"
 
short_duration_window = int(fs * short_duration)
long_duration_window = int(fs * long_duration)
 
stop = 0
 
data = data[0:,0]
data_ro = data_ro[0:,0]
data_rec = data_rec[0:,0]
 
#Checking first frequency.
#print all found in the file.
for i in range(0,len(data)):
    if int(data[i]) == freq_913 or int(data[i])+1 == freq_913 or int(data[i])-1 == freq_913:
        print i, data[i]
 
for i in range(stop,short_duration_window):
    if data[i] == freq_1370:
        print i, data[i]
 
#referenece 2 to plot: https://sites.google.com/site/haskell102/home/frequency-analysis-of-audio-file-with-python-numpy-scipy
# https://gist.github.com/livibetter/4118062
data = data/6
 
fft_data = fft(data)
fft_data_ro = fft(data_ro)
fft_data_rec = fft(data_rec)
 
ifft_data = ifft(data)
ifft_data_ro = ifft(data_ro)
 
t = np.arange(0.,6.,6./len(ifft_data))
t_ro = np.arange(0.,6.,6./len(ifft_data_ro))
 
plt.figure(1)
plt.subplot(211)
plt.plot(t,ifft_data,"ro")
 
plt.subplot(212)
plt.plot(t_ro,fft_data_ro,"bo")
plt.show()
 
# getting 1ms window based in the audio sample rate and lenght of the file.
window = len(data)/fs*1000
window_ro = len(data_ro)/fs_ro*1000
 
offset = 0
for i in range(offset,len(data)/window):
    for i in range(offset+window,window*offset):
        print i, data[i]
    raw_input("<Enter to continue>")
    print offset
    offset += 1