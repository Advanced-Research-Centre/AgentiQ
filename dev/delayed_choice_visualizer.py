import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DelayedChoiceQuantumEraser:
    def __init__(self, root):
        self.root = root
        self.root.title("Delayed Choice Quantum Eraser")

        # Create main frames
        self.control_frame = ttk.Frame(root)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.visual_frame = ttk.Frame(root)
        self.visual_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add controls
        self.setup_controls()

        # Add visualizations
        self.setup_visualization()
        self.setup_detector_pattern()

    def setup_controls(self):
        ttk.Label(self.control_frame, text="Experiment Parameters", font=("Arial", 14)).pack(pady=10)

        # Add sliders for parameters
        self.photon_source_var = tk.DoubleVar(value=0.5)
        ttk.Label(self.control_frame, text="Photon Source Intensity").pack()
        ttk.Scale(self.control_frame, from_=0, to=1, variable=self.photon_source_var, command=self.update_visualization).pack(pady=5)

        self.detector_choice_var = tk.IntVar(value=1)
        ttk.Label(self.control_frame, text="Detector Choice").pack()
        ttk.Radiobutton(self.control_frame, text="Detector D1/D2", variable=self.detector_choice_var, value=1, command=self.update_visualization).pack()
        ttk.Radiobutton(self.control_frame, text="Detector D3/D4", variable=self.detector_choice_var, value=2, command=self.update_visualization).pack()

    def setup_visualization(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.visual_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.update_visualization()

    def setup_detector_pattern(self):
        self.detector_fig, self.detector_ax = plt.subplots(figsize=(8, 6))
        self.detector_canvas = FigureCanvasTkAgg(self.detector_fig, master=self.visual_frame)
        self.detector_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.update_detector_pattern()

    def update_visualization(self, *args):
        self.ax.clear()

        # Simulate interference or no-interference patterns based on detector choice
        x = range(100)
        if self.detector_choice_var.get() == 1:
            y = [0.5 + 0.5 * (1 + (-1)**i) for i in x]  # Interference pattern
        else:
            y = [0.5 for _ in x]  # No interference pattern

        self.ax.plot(x, y, label="Photon Intensity")
        self.ax.set_title("Photon Detection Pattern")
        self.ax.set_xlabel("Position")
        self.ax.set_ylabel("Intensity")
        self.ax.legend()

        self.canvas.draw()

    def update_detector_pattern(self, *args):
        self.detector_ax.clear()

        # Simulate detector setup visualization
        detectors = ["D1", "D2", "D3", "D4"]
        counts = [50, 50, 0, 0] if self.detector_choice_var.get() == 1 else [0, 0, 50, 50]

        self.detector_ax.bar(detectors, counts, color=['blue', 'blue', 'red', 'red'])
        self.detector_ax.set_title("Detector Setup")
        self.detector_ax.set_ylabel("Photon Counts")

        self.detector_canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = DelayedChoiceQuantumEraser(root)
    root.mainloop()