import os
import argparse
import trimesh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def evaluate_symmetry(obj_file):
    try:
        # Load the OBJ file
        mesh = trimesh.load(obj_file, force='mesh')

        # apply subdivision
        mesh = mesh.subdivide(2)

        # Find the midpoint along the X-axis
        max_x = np.max(mesh.vertices[:, 0])
        min_x = np.min(mesh.vertices[:, 0])
        mid_x = (max_x + min_x) / 2

        # Indices for splitting the mesh
        left_indices = mesh.vertices[:, 0] < mid_x
        right_indices = mesh.vertices[:, 0] >= mid_x

        # Filter faces for each half
        left_faces = [face for face in mesh.faces if np.all(left_indices[face])]
        right_faces = [face for face in mesh.faces if np.all(right_indices[face])]

        # Create two separate meshes
        left_mesh = trimesh.Trimesh(vertices=mesh.vertices, faces=left_faces)
        right_mesh = trimesh.Trimesh(vertices=mesh.vertices, faces=right_faces)

        # Construct the output filenames
        base_name, ext = os.path.splitext(obj_file)
        left_file = f"{base_name}_left{ext}"
        right_file = f"{base_name}_right{ext}"

        # Save the left and right meshes
        left_mesh.export(left_file)
        right_mesh.export(right_file)
        
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Evaluate the symmetry of a 3D model.')
    parser.add_argument('--mesh', type=str, required=True, help='Path to the OBJ file')
    args = parser.parse_args()

    evaluate_symmetry(args.mesh)

if __name__ == '__main__':
    main()
