import wave
import numpy as np
from matplotlib import pyplot as plt

wf = wave.open("C:\Users\K4tr1n4\Documents\TrabASS\Mi_44.1.wav", 'rb')
print wf.getnchannels(), 'canais'
print wf.getsampwidth(), 'largura'
print wf.getframerate(), 'frequancia'
print wf.getnframes(), 'frames'
sinal = wf.readframes(-1)

Amplitude = np.fromstring(sinal, dtype=np.int16)
#print max(Amplitude)


AmplitudeJanelada=Amplitude*np.hamming(len(Amplitude))
Fourier=abs(np.fft.rfft(AmplitudeJanelada))

NyquistTeorema = (wf.getframerate() / 2.0)


MinFrequencia = (NyquistTeorema / (len(Amplitude)/2))

Frequencias=np.linspace(MinFrequencia, NyquistTeorema, num=(len(Amplitude) / 2))

print "Frequencia", len(Frequencias)
print Frequencias 

print "Fourier", len(Fourier)
print Fourier

plt.figure(1)
plt.title('Fourier')
plt.plot()
#plt.plot(range(0,len(Amplitude)), Amplitude)
#plt.axis([0, 4400, -1e8,1e8])

#plt.show()
