import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import numpy as np
import matplotlib
import scipy.signal as scipy
matplotlib.use('TkAgg')  # Use TkAgg backend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class SignalProcessingApp:
    def __init__(self, master):
        self.master = master
        master.title("Signal Processing Application")
        master.geometry("800x600")

        # Create the text input area
        self.text_input = ScrolledText(master, height=10)
        self.text_input.pack(fill=tk.BOTH, expand=False)

        # Insert a template into the text input
        self.text_input.insert(tk.END,
                               """def process_signal(x):
                                   # Enter your code here
                                   return x
                               """)

        # Create the Update button
        self.update_button = ttk.Button(master, text="Update", command=self.update_plots)
        self.update_button.pack()

        # Create an area for the plots
        self.figure = plt.Figure(figsize=(8, 4))
        self.ax_time = self.figure.add_subplot(121)
        self.ax_freq = self.figure.add_subplot(122)

        self.canvas = FigureCanvasTkAgg(self.figure, master)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Create a Label to display error messages
        self.error_label = tk.Label(master, text="", fg="red")
        self.error_label.pack()

        # Initialize the signal
        self.fs = 2000  # Sampling frequency
        self.t = np.arange(0, 0.1, 1 / self.fs)  # Time vector

        # Generate the input signal x
        self.x = 0.5 * np.sin(2 * np.pi * 300 * self.t) + 1 * np.sin(2 * np.pi * 500 * self.t)

        # Plot the initial signals
        self.update_plots()

    def update_plots(self):
        try:
            # Clear previous error message
            self.error_label.config(text="")

            # Get the code from the text input
            code = self.text_input.get("1.0", tk.END)

            # Prepare a local namespace for exec
            local_namespace = {}

            # Execute the code
            exec(code, {}, local_namespace)

            # Check if process_signal function is defined
            if 'process_signal' not in local_namespace:
                raise ValueError("Function 'process_signal' is not defined.")

            process_signal = local_namespace['process_signal']

            # Apply the process_signal function to x
            y = process_signal(self.x)

            # Check if y is the same length as x
            if len(y) != len(self.x):
                raise ValueError("Output signal has different length than input signal.")

            # Compute the frequency domain representation
            Y = np.fft.fft(y)
            Y_shifted = np.fft.fftshift(Y)
            freq = np.fft.fftfreq(len(y), d=1 / self.fs)
            freq_shifted = np.fft.fftshift(freq)

            # Clear the previous plots
            self.ax_time.clear()
            self.ax_freq.clear()

            # Plot x(t)
            self.ax_time.plot(self.t, y)
            self.ax_time.set_title('Time Domain Signal')
            self.ax_time.set_xlabel('Time [s]')
            self.ax_time.set_ylabel('Amplitude')

            # Plot x(w)
            self.ax_freq.plot(freq_shifted, np.abs(Y_shifted))
            self.ax_freq.set_title('Frequency Domain Signal')
            self.ax_freq.set_xlabel('Frequency [Hz]')
            self.ax_freq.set_ylabel('Magnitude')

            # Redraw the canvas
            self.canvas.draw()

        except Exception as e:
            # Display the error message
            self.error_label.config(text=str(e))
            print(e)  # For debugging


if __name__ == "__main__":
    root = tk.Tk()
    app = SignalProcessingApp(root)
    root.mainloop()
