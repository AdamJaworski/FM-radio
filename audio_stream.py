import pyaudio
import public_variables as pv
import numpy as np
from scipy.signal import resample_poly
from numba import njit

p = pyaudio.PyAudio()
output_stream = p.open(format=pv.DATA_TYPE, channels=int(pv.CHANNELS), rate=int(pv.SOUND_SAMPLE_RATE), output=True, frames_per_buffer=int(pv.BUFFER_SAMPLES))

def play_samples(samples):
    output_stream.write(samples.tobytes())

@njit
def fm_demodulate(iq_samples):
    # Compute the phase difference between consecutive samples
    demodulated = np.angle(iq_samples[1:] * np.conj(iq_samples[:-1]))
    return demodulated

def demodulate_and_play(samples):
    samples = fm_demodulate(samples)
    # Resample to match the audio sample rate
    samples = resample_poly(samples, pv.SOUND_SAMPLE_RATE, pv.sdr_sample_rate)
    samples = final_stage(samples, volume=pv.volume)
    play_samples(samples)

@njit
def final_stage(samples, volume: float):
    # Normalize the audio signal
    samples /= np.max(np.abs(samples))
    # Convert to 16-bit integer
    samples = (samples * 32767 * volume).astype(np.int16)
    return samples

