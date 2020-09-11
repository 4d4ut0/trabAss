import wave
import numpy as np
from matplotlib import pyplot as plt

wf = wave.open("C:\Users\K4tr1n4\Documents\TrabASS\Mi_44.1.wav", 'rb')
sinal = wf.readframes(-1)

Amplitude = np.fromstring(sinal, dtype=np.int16)

AmplitudeJanelada=Amplitude*np.hamming(len(Amplitude))
print Amplitude
print np.hamming(len(Amplitude))
Fourier=np.fft.rfft(AmplitudeJanelada)

NyquistTeorema = (wf.getframerate() / 2.0)


MinFrequencia = (NyquistTeorema / (len(Amplitude)/2))

Frequencias=np.linspace(MinFrequencia, NyquistTeorema, num=(len(Amplitude) / 2))

print "Frequencia", len(Frequencias), max(Frequencias)
print Frequencias 

print "Fourier", len(Fourier), max(Fourier)
print Fourier

plt.figure(1)
plt.title('Fourier')
plt.plot(Frequencias,Fourier[0:len(Frequencias)])
plt.axis([0, max(Frequencias)/5, -max(Fourier), max(Fourier)])

plt.show()
