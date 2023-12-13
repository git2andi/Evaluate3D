import argparse
import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def load_and_render_obj(obj_file):
    try:
        # Load the OBJ file
        mesh = trimesh.load(obj_file, force='mesh')

        # Check if the mesh is valid
        if mesh is not None:
          fig = plt.figure()
          ax = fig.add_subplot(111, projection='3d')

          ax.plot_trisurf(*mesh.vertices.T, triangles=mesh.faces, color='skyblue', edgecolor='b')
          ax.set_title('3D Object Render')
          plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Render an OBJ file to a 3D view.')
    parser.add_argument('--mesh', required=True, help='Path to the OBJ file')
    args = parser.parse_args()

    load_and_render_obj(args.mesh)

if __name__ == '__main__':
    main()