import trimesh
import numpy as np
import os

def split_and_return_objs(input_file, output_dir):
    try:
        # Make a copy of the input mesh to avoid modifying it
        mesh = trimesh.load(input_file, force='mesh')

        # Apply subdivision
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
        base_name = "rotated_mesh"
        base_name = "rotated_mesh"  # Adjust this as needed
        left_file = os.path.join(output_dir, f"{base_name}_left.obj")
        right_file = os.path.join(output_dir, f"{base_name}_right.obj")

        # Save the left and right meshes
        left_mesh.export(left_file)
        right_mesh.export(right_file)

        return left_mesh, right_mesh

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None
