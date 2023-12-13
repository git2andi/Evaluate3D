import argparse
import trimesh
import numpy as np
import os

def rotate_and_save_obj(input_file):
    try:
        # Load the OBJ file
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

        # Apply the x-axis rotation
        mesh.apply_transform(rotation_matrix_x)

        # Construct the output filename
        base_name, ext = os.path.splitext(input_file)
        output_file = f"{base_name}_rotated{ext}"

        # Save the rotated mesh
        mesh.export(output_file)
        print(f"Rotated OBJ file saved as: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Rotate an OBJ file by 90 degrees about the X-axis.')
    parser.add_argument('--mesh', type=str, required=True, help='Path to the OBJ file')
    args = parser.parse_args()

    rotate_and_save_obj(args.mesh)

if __name__ == '__main__':
    main()
