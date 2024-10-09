import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from scipy.fft import fftshift
import public_variables as pv

fig, ax = plt.subplots()

def create_plot():
    plt.ion()
    plt.show()

def update_plot(samples):
    f, t, Sxx = spectrogram(samples, pv.SDR_SAMPLE_RATE, return_onesided=False)
    ax.cla()
    ax.pcolormesh(t, fftshift(f), fftshift(Sxx, axes=0), shading='gouraud')
    ax.set_title("Live Spectrogram")
    ax.set_ylabel("Frequency [Hz]")
    ax.set_xlabel("Time [s]")

    plt.draw()
    plt.pause(0.001)