import numpy as np

import soundcard
import aubio

hop_size = 3072 # we measure pitch every hop_size frames
window = 8192 # number of previous frames analysed for each pitch measurement
sample_rate = 44100

pitcher = aubio.pitch("default", window, hop_size, sample_rate)

guitar = soundcard.get_microphone('Rocksmith')

# Collapse octaves and map notes linearly between 0 and 1
def normalise(freq):
    base_freq = 82.40689  # Low E a.k.a. E2

    if freq == 0:
        freq += base_freq
    while freq > base_freq*2:
        freq /= 2
    while freq < base_freq:
        freq *= 2

    return np.log2(freq) - np.log2(base_freq)

while True:
    samples = np.array(guitar.record(hop_size, sample_rate), dtype=np.float32)
    freq = pitcher(samples)[0]

    print("%.2f" % normalise(freq),  end='\r')