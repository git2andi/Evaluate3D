import argparse
import os
from rotateObject import rotate_and_return_obj
from splitObject import split_and_return_objs
from evaluateSymmetry import evaluate_symmetry

def main():
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Process an OBJ file: rotate, split, and evaluate symmetry.')
    parser.add_argument('--obj', required=True, help='Path to the OBJ file')
    parser.add_argument('--output_dir', required=True, help='Directory to save the output files')
    parser.add_argument('--rotate', choices=['yes', 'no'], default='yes', help='Perform rotation (yes/no)')
    args = parser.parse_args()

    # Check if the output directory exists, and create it if not
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)


    # Rotate the object if --rotate is 'yes'
    if args.rotate == 'yes':
        rotated_mesh = rotate_and_return_obj(args.obj)

        if rotated_mesh is None:
            print("Error: Rotation failed.")
            return
    else:
        rotated_mesh = args.obj

    # Split the rotated object
    left_mesh, right_mesh = split_and_return_objs(rotated_mesh, args.output_dir)

    if left_mesh is None or right_mesh is None:
        print("Error: Splitting failed.")
        return

    # Evaluate the symmetry
    symmetry_score = evaluate_symmetry(left_mesh, right_mesh, args.output_dir)

    if symmetry_score is not None:
        print(f"Symmetry score: {symmetry_score:.2f}%")

if __name__ == '__main__':
    main()
