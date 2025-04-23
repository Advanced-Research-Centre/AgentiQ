import numpy as np

class PetriNetQuantum:
    def __init__(self, adjacency_matrix, entanglement_rates, local_qubits):
        self.adjacency_matrix = np.array(adjacency_matrix)
        self.entanglement_rates = entanglement_rates
        self.local_qubits = local_qubits
        self.num_nodes = len(local_qubits)
        self.tokens = np.zeros(self.num_nodes, dtype=int)

    def generate_entanglement(self):
        """Simulate entanglement generation at each node."""
        for i in range(self.num_nodes):
            self.tokens[i] += self.entanglement_rates[i]

    def distribute_entanglement(self):
        """Simulate entanglement distribution based on the adjacency matrix."""
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if self.adjacency_matrix[i, j] == 1 and self.tokens[i] > 0:
                    self.tokens[i] -= 1
                    self.tokens[j] += 1

    def simulate(self, steps):
        """Run the Petri net simulation for a given number of steps."""
        for step in range(steps):
            print(f"Step {step + 1}:")
            self.generate_entanglement()
            print(f"  After generation: {self.tokens}")
            self.distribute_entanglement()
            print(f"  After distribution: {self.tokens}")

if __name__ == "__main__":
    # Example input
    adjacency_matrix = [
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
    ]
    entanglement_rates = [2, 1, 3]  # Entanglement generation rate for each node
    local_qubits = [5, 5, 5]  # Number of qubits local to each node

    petri_net = PetriNetQuantum(adjacency_matrix, entanglement_rates, local_qubits)
    petri_net.simulate(steps=5)