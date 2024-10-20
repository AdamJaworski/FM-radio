import soundfile as sf
import sounddevice as sd

x, fs = sf.read('')

# demod - as you wish


# play sound

sd.play(x, fs)
sd.wait()