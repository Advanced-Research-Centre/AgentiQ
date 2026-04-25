import tkinter as tk
import random
from qiskit import QuantumCircuit

class QuantumCircuitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Circuit Error Propagation")
        self.root.geometry("600x400")

        self.canvas = tk.Canvas(root, width=600, height=300, bg="white")
        self.canvas.pack(pady=20)

        self.generate_button = tk.Button(root, text="Generate Circuit", command=self.generate_circuit)
        self.generate_button.pack(pady=10)

        self.error_label = tk.Label(root, text="Select a wire and error type (X or Z):")
        self.error_label.pack()

        self.error_type = tk.StringVar(value="X")
        self.error_x = tk.Radiobutton(root, text="X Error", variable=self.error_type, value="X")
        self.error_x.pack()
        self.error_z = tk.Radiobutton(root, text="Z Error", variable=self.error_type, value="Z")
        self.error_z.pack()

        self.insert_error_button = tk.Button(root, text="Insert Error", command=self.insert_error)
        self.insert_error_button.pack(pady=10)

        self.circuit = None
        self.error_wire = None

    def generate_circuit(self):
        self.circuit = QuantumCircuit(3)
        self.canvas.delete("all")

        for qubit in range(3):
            self.circuit.h(qubit)
            self.draw_gate("H", qubit, 0)

        for _ in range(3):
            qubit = random.randint(0, 2)
            gate = random.choice(["T", "CNOT"])
            if gate == "T":
                self.circuit.t(qubit)
                self.draw_gate("T", qubit, _ + 1)
            elif gate == "CNOT":
                target = (qubit + 1) % 3
                self.circuit.cx(qubit, target)
                self.draw_gate("CNOT", qubit, _ + 1, target)

    def draw_gate(self, gate, qubit, column, target=None):
        x = 50 + column * 100
        y = 50 + qubit * 80
        self.canvas.create_rectangle(x, y, x + 40, y + 40, fill="lightblue")
        self.canvas.create_text(x + 20, y + 20, text=gate)
        if target is not None:
            target_y = 50 + target * 80
            self.canvas.create_line(x + 20, y + 20, x + 20, target_y + 20, width=2)

    def insert_error(self):
        if self.circuit is None:
            return

        self.error_wire = random.randint(0, 2)
        error_type = self.error_type.get()
        self.canvas.create_text(300, 350, text=f"Inserted {error_type} error on wire {self.error_wire}", fill="red")
        self.propagate_error()

    def propagate_error(self):
        if self.error_wire is None:
            return

        for qubit in range(3):
            if qubit == self.error_wire:
                self.canvas.create_line(50, 50 + qubit * 80 + 20, 550, 50 + qubit * 80 + 20, fill="red", width=3)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuantumCircuitApp(root)
    root.mainloop()