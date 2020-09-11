import sys
from audiolazy import (tostream, zcross, lag2freq, AudioIO, freq2str, sHz,
                       lowpass, envelope, pi, maverage, Stream, thub, chunks)

def limiter(sig, threshold=.1, size=256, env=envelope.rms, cutoff=pi/2048):
  sig = thub(sig, 2)
  return sig * Stream( 1. if el <= threshold else threshold / el
                       for el in maverage(size)(env(sig, cutoff=cutoff)) )

@tostream
def zcross_pitch(sig, size=2048, hop=None):
  for blk in zcross(sig, hysteresis=.01).blocks(size=size, hop=hop):
    crossings = sum(blk)
    yield 0. if crossings == 0 else lag2freq(2. * size / crossings)


def pitch_from_mic(upd_time_in_ms):
  rate = 44100
  s, Hz = sHz(rate)

  api = sys.argv[1] if sys.argv[1:] else None
  chunks.size = 1 if api == "jack" else 16

  with AudioIO(api=api) as recorder:
    snd = recorder.record(rate=rate)
    sndlow = lowpass(400 * Hz)(limiter(snd, cutoff=20 * Hz))
    hop = int(upd_time_in_ms * 1e-3 * s)
    for pitch in freq2str(zcross_pitch(sndlow, size=2*hop, hop=hop) / Hz):
      yield pitch


if __name__ == "__main__":
  try:
    import tkinter
  except ImportError:
    import Tkinter as tkinter
  import threading
  import re

  tk = tkinter.Tk()
  tk.title(__doc__.strip().splitlines()[0])
  lbldata = tkinter.StringVar(tk)
  lbltext = tkinter.Label(tk, textvariable=lbldata, font=("Purisa", 72),
                          width=10)
  lbltext.pack(expand=True, fill=tkinter.BOTH)
  btnclose = tkinter.Button(tk, text="Close", command=tk.destroy,
                            default="active")
  btnclose.pack(fill=tkinter.X)

  regex_note = re.compile(r"^([A-Gb#]*-?[0-9]*)([?+-]?)(.*?%?)$")
  upd_time_in_ms = 200

  def upd_value(): 
    pitches = iter(pitch_from_mic(upd_time_in_ms))
    while not tk.should_finish:
      tk.value = next(pitches)

  def upd_timer(): 
    lbldata.set("\n".join(regex_note.findall(tk.value)[0]))
    tk.after(upd_time_in_ms, upd_timer)

  
  tk.should_finish = False
  tk.value = freq2str(0) 
  lbldata.set(tk.value)
  tk.upd_thread = threading.Thread(target=upd_value)

  tk.upd_thread.start()
  tk.after_idle(upd_timer)
  tk.mainloop()
  tk.should_finish = True
  tk.upd_thread.join()
