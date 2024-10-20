import soundfile as sf
import sounddevice as sd
import numpy as np

# fi(t) = fc + deltat * m(t)
# delta t wynika z zasady Carsona

x, fs = sf.read('')
dt = 1 / fs
Nx = len(x)
t = dt * np.arange(Nx)
# demod - as you wish


# FM demod
fi3 = (1 / (2 * np.pi)) * np.angle(x[2:] * np.conj(x[:-2])) / (2 * dt)
fi3 = np.append(fi3, 0)


# play sound

sd.play(x, fs)
sd.wait()