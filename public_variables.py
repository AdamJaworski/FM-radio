import pyaudio

SOUND_SAMPLE_RATE = int(192e3)
BUFFER_SAMPLES = int(5096)
DATA_TYPE = pyaudio.paInt16
CHANNELS = 1

bandwidth = int(20e6)
center_freq = int(104.1e6)
sdr_sample_rate = int(521e3)
interval = (BUFFER_SAMPLES * 1000) / sdr_sample_rate
volume = 0.1

play_audio = True

print(f'interval {interval}ms')
print(f'Update every {interval * 0.5}ms')

# SoundQuality: sdr_sample_rate = int(521e3), BUFFER_SAMPLES = int(5096 * 2 * 10)
# SoundQuality: sdr_sample_rate = int(521e3), BUFFER_SAMPLES = int(5096 * 2)
# SoundQuality: sdr_sample_rate = int(521e3), BUFFER_SAMPLES = int(5096), SOUND_SAMPLE_RATE = int(192e3)


# Display quality: sdr_sample_rate = int(5e6), BUFFER_SAMPLES = int(1024 * 2)