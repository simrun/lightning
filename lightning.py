import numpy as np

import soundcard
import aubio

sample_rate = 44100

hop_size = round(sample_rate * 1/1000)  # we take a pitch measurement every hop_size frames
window = 2048  # number of previous frames analysed for each pitch measurement

pitcher = aubio.pitch("default", window, hop_size, sample_rate)

input_device = soundcard.get_microphone('Rocksmith')


# Collapse octaves and map notes linearly between 0 and 1
def normalise(freq):
    base_freq = 440 * 2**(-29/12) # guitar open sixth string (E2)

    if freq == 0:
        freq += base_freq
    while freq > base_freq*2:
        freq /= 2
    while freq < base_freq:
        freq *= 2

    return np.log2(freq) - np.log2(base_freq)


with input_device.recorder(sample_rate) as recorder:
    while True:
        samples = np.array(recorder.record(hop_size), dtype=np.float32)
        pitch = pitcher(samples)[0]

        print("%.2f" % normalise(pitch),  end='\r')
