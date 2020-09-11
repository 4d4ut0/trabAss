from __future__ import division
from audiolazy import sHz, chunks, AudioIO, line, pi, window
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from numpy.fft import rfft
import numpy as np
import collections, sys, threading

# AudioLazy init
rate = 44100
s, Hz = sHz(rate)
ms = 1e-3 * s

length = 2 ** 12
data = collections.deque([0.] * length, maxlen=length)
wnd = np.array(window.hamming(length))

api = sys.argv[1] if sys.argv[1:] else None
chunks.size = 1 if api == "jack" else 16

def update_data():
  with AudioIO(api=api) as rec:
    for el in rec.record(rate=rate):
      data.append(el)
      if update_data.finish:
        break

update_data.finish = False
th = threading.Thread(target=update_data)
th.start() 

fig = plt.figure("AudioLazy in a Matplotlib animation", facecolor='#cccccc')

time_values = np.array(list(line(length, -length / ms, 0)))
time_ax = plt.subplot(2, 1, 1,
                      xlim=(time_values[0], time_values[-1]),
                      ylim=(-1., 1.),
                      axisbg="black")
time_ax.set_xlabel("Time (ms)")
time_plot_line = time_ax.plot([], [], linewidth=2, color="#00aaff")[0]

dft_max_min, dft_max_max = .01, 1.
freq_values = np.array(line(length, 0, 2 * pi / Hz).take(length // 2 + 1))
freq_ax = plt.subplot(2, 1, 2,
                      xlim=(freq_values[0], freq_values[-1]),
                      ylim=(0., .5 * (dft_max_max + dft_max_min)),
                      axisbg="black")
freq_ax.set_xlabel("Frequency (Hz)")
freq_plot_line = freq_ax.plot([], [], linewidth=2, color="#00aaff")[0]


def init(): 
  time_plot_line.set_data([], []) 
  freq_plot_line.set_data([], [])
  fig.tight_layout()
  return [] if init.rempty else [time_plot_line, freq_plot_line]

init.rempty = False 

def animate(idx):
  array_data = np.array(data)
  spectrum = np.abs(rfft(array_data * wnd)) / length

  time_plot_line.set_data(time_values, array_data)
  freq_plot_line.set_data(freq_values, spectrum)

 
  smax = spectrum.max()
  top = freq_ax.get_ylim()[1]
  if top < dft_max_max and abs(smax/top) > 1:
    freq_ax.set_ylim(top=top * 2)
  elif top > dft_max_min and abs(smax/top) < .3:
    freq_ax.set_ylim(top=top / 2)
  else:
    init.rempty = True 
    return [time_plot_line, freq_plot_line] 
  return []


anim = FuncAnimation(fig, animate, init_func=init, interval=10, blit=True)
plt.ioff()
plt.show() 


update_data.finish = True
th.join()
