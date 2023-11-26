from pygltflib import GLTF2
import trimesh

def convert_to_obj(glb_file_path):
    """
    Convert a .glb file to a .obj file using trimesh.
    :param glb_file_path: Path to the .glb file.
    :return: Path to the converted .obj file.
    """
    # Load the .glb file as a trimesh object
    mesh = trimesh.load(glb_file_path)

    # Define the path for the .obj file
    obj_file_path = glb_file_path.replace('.glb', '.obj')

    # Export the mesh to an .obj file
    mesh.export(obj_file_path, file_type='obj')

    return obj_file_path

def preprocess(filepath):
    """
    Preprocess a given .obj file.
    :param filepath: Path to the .obj file.
    """
    print(f"Preprocessing {filepath}...")

    # Load the mesh
    mesh = trimesh.load(filepath)
    print("Mesh loaded.")

    # Remove degenerate and duplicate faces
    initial_face_count = len(mesh.faces)
    mesh.remove_degenerate_faces()
    if len(mesh.faces) < initial_face_count:
        print(f"Removed {initial_face_count - len(mesh.faces)} degenerate faces.")

    initial_face_count = len(mesh.faces)
    mesh.remove_duplicate_faces()
    if len(mesh.faces) < initial_face_count:
        print(f"Removed {initial_face_count - len(mesh.faces)} duplicate faces.")

    # Fill holes
    initial_hole_count = len(mesh.bounding_box_oriented.vertices)
    mesh.fill_holes()
    if len(mesh.bounding_box_oriented.vertices) > initial_hole_count:
        print(f"Filled {len(mesh.bounding_box_oriented.vertices) - initial_hole_count} holes.")

    # Fix normals
    mesh.fix_normals()
    print("Normals fixed.")

    # Handle disjoint shells
    shells = mesh.split(only_watertight=False)
    if len(shells) > 1:
        print(f"Found and separated {len(shells)} disjoint shells.")
        for shell in shells:
            shell.fill_holes()
            shell.fix_normals()

    # Save the preprocessed mesh back to an OBJ file
    mesh.export(filepath)
    print(f"Mesh preprocessing complete. Saved to {filepath}.")
