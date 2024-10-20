import sys
import time

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout,
    QVBoxLayout, QLabel, QLineEdit, QPushButton
)
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
import numpy as np
import adi
import audio_stream
import public_variables as pv

class SpectrumAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize PlutoSDR
        self.sdr = adi.Pluto()
        self.sdr.rx_rf_bandwidth = pv.bandwidth      # 20 MHz RF bandwidth
        self.sdr.rx_lo = pv.center_freq                # LO frequency at 100 MHz
        self.sdr.sample_rate = pv.sdr_sample_rate
        self.sdr.rx_buffer_size = pv.BUFFER_SAMPLES             # Buffer size

        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Create input fields
        input_layout = QHBoxLayout()

        # Center Frequency Input
        self.freq_label = QLabel("Center Frequency (Hz):")
        self.freq_input = QLineEdit(str(self.sdr.rx_lo))
        input_layout.addWidget(self.freq_label)
        input_layout.addWidget(self.freq_input)

        # Bandwidth Input
        self.bandwidth_label = QLabel("Bandwidth (Hz):")
        self.bandwidth_input = QLineEdit(str(self.sdr.rx_rf_bandwidth))
        input_layout.addWidget(self.bandwidth_label)
        input_layout.addWidget(self.bandwidth_input)

        self.vol_label = QLabel("Volume:")
        self.vol_input = QLineEdit(str(pv.volume))
        input_layout.addWidget(self.vol_label)
        input_layout.addWidget(self.vol_input)

        # Update Button
        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update_sdr_settings)
        input_layout.addWidget(self.update_button)

        main_layout.addLayout(input_layout)

        # Set up the plotting window
        self.plot_widget = pg.PlotWidget()
        main_layout.addWidget(self.plot_widget)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.plot_widget.setTitle("Live Spectrum from ADALM-PLUTO")
        self.plot_widget.setLabel('left', 'Amplitude', units='dB')
        self.plot_widget.setLabel('bottom', 'Frequency', units='Hz')
        self.plot_widget.setYRange(-100, 0)  # Adjust based on expected signal levels
        self.update_plot_axis()

        self.curve = self.plot_widget.plot()

        # Set up a timer to update the plot
        self.timer = QTimer()
        self.timer.setInterval(int(pv.interval * 0.5))
        # self.timer.setInterval(20)
        self.timer.timeout.connect(self.update_with_samples)
        self.timer.start()

    def update_with_samples(self):
        samples = self.sdr.rx()

        if pv.play_audio:
            audio_stream.demodulate_and_play(samples)

        self.update_plot(samples)

    def update_plot_axis(self):
        # Update the X-axis range based on the current LO and sample rate
        self.plot_widget.setXRange(
            self.sdr.rx_lo - self.sdr.sample_rate / 2,
            self.sdr.rx_lo + self.sdr.sample_rate / 2
        )
    def change_volume(self):
        new_lo = float(self.freq_input.text())

    def update_sdr_settings(self):
        try:
            # Get input values
            new_lo = float(self.freq_input.text())
            new_bandwidth = float(self.bandwidth_input.text())
            new_volume = float(self.vol_input.text())

            pv.volume = new_volume

            self.sdr.rx_lo = int(new_lo)
            self.sdr.rx_rf_bandwidth = int(new_bandwidth)

            self.update_plot_axis()

            print(f"Updated SDR settings: LO = {self.sdr.rx_lo} Hz, Bandwidth = {self.sdr.rx_rf_bandwidth} Hz and sample rate {self.sdr.sample_rate}")
        except ValueError:
            print("Invalid input for frequency or bandwidth.")

    def update_plot(self, samples):
        try:
            # Compute the spectrum
            fft_samples = np.fft.fftshift(np.fft.fft(samples))
            spectrum = 20 * np.log10(np.abs(fft_samples))

            # Frequency axis
            freq = np.fft.fftshift(
                np.fft.fftfreq(len(spectrum), 1 / self.sdr.sample_rate)
            ) + self.sdr.rx_lo

            # Update the plot
            self.curve.setData(freq, spectrum)
        except Exception as e:
            print(f"Error fetching samples: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpectrumAnalyzer()
    window.show()
    sys.exit(app.exec_())