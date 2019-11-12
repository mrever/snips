import sounddevice as sd
import numpy as np
from librosa.effects import pitch_shift
import matplotlib.pyplot as plt
import scipy.io
swrite = scipy.io.wavfile.write

p2 = 2*3.14159
fs = 44100
dur = 5
t = np.linspace(0, dur, dur*fs)
# sd.play(10*np.sin(2*3.14159*440*(2**(1/12))*t), fs, device=8)
# wf = 10*np.sin(2*3.14159*440*(2**(1/12))*t)
freq = 900
wf = np.abs(np.cos(p2*2*t))*1*np.sin(p2*freq*t)
wf += np.abs(0.2+np.cos(p2*1.1*t))*np.cos(p2*400*t)
# wf = 0
wf += np.abs(0.2+np.cos(p2*4*t))*np.cos(p2*120*t)
sd.play(wf, fs, device=8)
swrite('swav.wav', fs, wf)

plt.figure()
plt.plot(t, wf)
plt.show(block=False)

sd.play(10*np.sin(2*3.14159*220*(2**(1/12))*t), fs, device=8)
440*2**(1/12)440*2**(1/12)

sd.play(100*np.sin(2*3.14159*440*(2**(3/12))*t), fs, device=8)


wf = 10*np.sin(2*3.14159*220*(2**(1/12))*t)
wfps = pitch_shift(wf, fs, n_steps=0.5)
sd.play(wf, fs)
sd.play(wfps, fs)

mr = sd.rec(fs*dur, fs, channels=1, dtype='float64', device=1)
mr = mr.squeeze()
mrps = pitch_shift(mr, fs, n_steps=-5)

sd.play(10*mrps, fs)

sd.query_devices()


mrps.shape
mrps.dtype
np.amin(mrps)

plt.figure()
plt.plot(np.flipud(mrps))
plt.show(block=False)
