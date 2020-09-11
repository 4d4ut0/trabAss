from audiolazy import *

fNota = 440
rate = 44100
s, Hz = sHz(rate)

player = AudioIO()
snd =  sinusoid(fNota * Hz).limit(2 * s)
th = player.play(snd, rate=rate)

player.close()