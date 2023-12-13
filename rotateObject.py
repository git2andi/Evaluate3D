import trimesh
import numpy as np

def rotate_and_return_obj(input_file):
    try:
        # Make a copy of the input mesh to avoid modifying it
        mesh = trimesh.load(input_file, force='mesh')

        # Define a rotation matrix for 90 degrees about the Z-axis
        rotation_matrix_z = trimesh.transformations.rotation_matrix(
            np.radians(90), [0, 0, -1]
        )

        # Apply the Z-axis rotation
        mesh.apply_transform(rotation_matrix_z)

        # Define a rotation matrix for 90 degrees about the X-axis
        rotation_matrix_x = trimesh.transformations.rotation_matrix(
            np.radians(90), [-1, 0, 0]
        )

        # Apply the X-axis rotation
        mesh.apply_transform(rotation_matrix_x)

        return mesh

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
