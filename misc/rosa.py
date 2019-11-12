import librosa as lr
import sounddevice as sd
import numpy as np

testfile = 'F:/videos/lotl/SwanSongsII/lighthouse.mp3'

print(sd.query_devices())

sr = lr.get_samplerate(testfile)
y = lr.load(testfile, sr, False)

yarr = y[0].T

ydiff = yarr.T[0]-yarr.T[1]


np.amin(ydiff), np.amax(ydiff)

sd.play(np.flipud(yarr), sr, device=15)
sd.stop()
