import trimesh
import numpy as np
from scipy.spatial import KDTree
import os

def evaluate_symmetry(left_mesh, right_mesh, output_dir, tolerance=0.02):
    try:
        # mirror the right mesh to compare
        right_mesh_copy = right_mesh.copy()
        right_mesh_copy.apply_transform(trimesh.transformations.reflection_matrix(point=[0, 0, 0], normal=[1, 0, 0]))

        # Calculate the translation needed to align the right mesh with the left mesh
        translation_vector = left_mesh.bounds[0] - right_mesh_copy.bounds[0]
        right_mesh_copy.apply_translation(translation_vector)

        # Create a KDTree for the mirrored right mesh
        mirrored_tree = KDTree(right_mesh_copy.vertices)

        # For each vertex in the left mesh, find the closest vertex in the mirrored right mesh
        distances, _ = mirrored_tree.query(left_mesh.vertices)

        # Count how many vertices fall within the tolerance distance
        symmetric_vertices = np.sum(distances < tolerance)
        score = symmetric_vertices / len(left_mesh.vertices) * 100

        left_evaluation_file = os.path.join(output_dir, "left_evaluation.obj")
        right_evaluation_file = os.path.join(output_dir, "right_evaluation.obj")

        left_mesh.export(left_evaluation_file)
        right_mesh_copy.export(right_evaluation_file)


        return score

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
