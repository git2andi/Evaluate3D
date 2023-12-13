
import argparse
import os
import sys

# Importing the functions from the other scripts
from rotateObject import rotate_and_save_obj
from splitObject import split_and_save_obj
from evaluateSymmetry import evaluate_symmetry

def main():
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Process an OBJ file: rotate, split, and evaluate symmetry.')
    parser.add_argument('--obj', type=str, required=True, help='Path to the OBJ file')
    args = parser.parse_args()

    # Rotate the object
    rotated_obj_path = rotate_and_save_obj(args.obj)
    
    # Check if rotation was successful
    if not os.path.exists(rotated_obj_path):
        print("Error: Rotation failed.")
        sys.exit(1)

    # Split the rotated object
    left_obj_path, right_obj_path = split_and_save_obj(rotated_obj_path)

    # Check if splitting was successful
    if not (os.path.exists(left_obj_path) and os.path.exists(right_obj_path)):
        print("Error: Splitting failed.")
        sys.exit(1)

    # Evaluate the symmetry
    evaluate_symmetry(left_obj_path, right_obj_path)

if __name__ == '__main__':
    main()
