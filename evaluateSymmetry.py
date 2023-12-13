import argparse
import trimesh
import numpy as np
from scipy.spatial import KDTree

def calculate_symmetry(left_file, right_file, tolerance = 0.034):
    try:
        # Load the left and right meshes
        left_mesh = trimesh.load(left_file, force='mesh')
        right_mesh = trimesh.load(right_file, force='mesh')

        # mirror the right mesh to compare
        right_mesh.apply_transform(trimesh.transformations.reflection_matrix(point=[0, 0, 0], normal=[1, 0, 0]))

        # Calculate the bounding boxes
        left_bounds = left_mesh.bounds
        right_bounds = right_mesh.bounds

        # Calculate the translation needed to align the right mesh with the left mesh
        translation_vector = left_bounds[0] - right_bounds[0]
        right_mesh.apply_translation(translation_vector)

        # Create a KDTree for the mirrored right mesh
        mirrored_tree = KDTree(right_mesh.vertices)

        # For each vertex in the left mesh, find the closest vertex in the mirrored right mesh
        distances, _ = mirrored_tree.query(left_mesh.vertices)

        # Count how many vertices fall within the tolerance distance
        symmetric_vertices = np.sum(distances < tolerance)
        score = symmetric_vertices / len(left_mesh.vertices) * 100

        print(f"Symmetry score: {score}%")
        
        
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Calculate the symmetry between two halves of a figure.')
    parser.add_argument('--left', required=True, help='Path to the left OBJ file')
    parser.add_argument('--right', required=True, help='Path to the right OBJ file')
    args = parser.parse_args()

    calculate_symmetry(args.left, args.right)

if __name__ == '__main__':
    main()
