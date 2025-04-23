import pubchempy as pcp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def visualize_molecule(cid = 962):
    try:
        # Query PubChem for the molecule using its CID
        # compound = pcp.Compound.from_cid(cid, record_type="3d")
        compound = pcp.Compound.from_cid(cid).to_dict()

        # Extract 3D coordinates from PubChem
        # print(compound)
        molecule_name = compound['iupac_name']
        atoms = compound['atoms']
        bonds = compound['bonds']
        print(bonds)
        if 'z' in atoms[0]:
            coordinates = np.array([[atom['x'], atom['y'], atom['z']] for atom in atoms])
        else:
            coordinates = np.array([[atom['x'], atom['y'], 0] for atom in atoms])
        atom_labels = [atom['element'] for atom in atoms]
        atom_size = [atom['number'] for atom in atoms]

        # Create a 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot atoms
        text_dist = 0.01
        for i, (x, y, z) in enumerate(coordinates):
            ax.scatter(x, y, z, label=atom_labels[i], s=atom_size[i]*20, c='b')
            ax.text(x+text_dist, y+text_dist, z+text_dist, atom_labels[i], fontsize=10, ha='center')

        # Plot bonds
        for bond in bonds:
            start_idx, end_idx = bond['aid1'] - 1, bond['aid2'] - 1
            start_coord = coordinates[start_idx]
            end_coord = coordinates[end_idx]
            ax.plot([start_coord[0], end_coord[0]],
                    [start_coord[1], end_coord[1]],
                    [start_coord[2], end_coord[2]], 'k-', linewidth=1)
            
        # Set plot labels
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        ax.set_zlabel("Z-axis")
        ax.set_title(f"3D Visualization of {molecule_name}")

        ax.set_aspect('equal', adjustable='box')
        

        plt.legend()
        plt.show()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    visualize_molecule()