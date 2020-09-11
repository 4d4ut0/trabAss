from scipy.fftpack import fft
import math
import numpy as np
from matplotlib import pyplot as pl


N = 48000
fs = 48000.0
sine_list_x = []
K = (10000.0 - 1000.0)/(48000.0)
for x in range(N):
    sine_list_x.append(math.sin(2*math.pi*(1000.0*(x/48000.0)+(K/2.0)*(x**2)/(48000.0))))

xf = np.linspace(0.0, fs/2.0, N/2)
yf = fft(sine_list_x)
yf = yf / math.sqrt(N)
#yf = yf / N

pl.figure()
pl.plot(xf, abs(yf[0:N/2]))

pl.show()