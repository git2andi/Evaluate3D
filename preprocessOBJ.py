import trimesh
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve


def convert_to_obj(glb_file_path):
    """
    Convert a .glb file to a .obj file using trimesh and save it as a new file.
    :param glb_file_path: Path to the .glb file.
    :return: Path to the converted .obj file.
    """
    # Load the .glb file as a trimesh object
    mesh = trimesh.load(glb_file_path)

    # Define the path for the new .obj file (avoid overwriting the original file)
    obj_file_path = glb_file_path.replace('.glb', '_converted.obj')

    # Export the mesh to the new .obj file
    mesh.export(obj_file_path, file_type='obj')

    return obj_file_path

def preprocess(filepath):
    print(f"Preprocessing {filepath}...")

    # Load the mesh
    mesh = trimesh.load(filepath, force='mesh')

    # Capture the initial face count
    initial_face_count = len(mesh.faces)

    # Apply preprocessing steps
    mesh, simplified_face_count = simplify_mesh(mesh, target_number_of_faces=10000)
    mesh, normalization_scale = normalize_mesh(mesh)
    mesh, smoothing_iterations = smooth_mesh(mesh, iterations=10)

    # Feature extraction
    features = extract_features(mesh)

    # Save the preprocessed mesh back to an OBJ file
    preprocessed_file_path = filepath.replace('.obj', '_preprocessed.obj')
    mesh.export(preprocessed_file_path)

    # Capture the final face count after preprocessing
    final_face_count = len(mesh.faces)

    preprocessing_results = {
        'initial_face_count': initial_face_count,
        'final_face_count': len(mesh.faces),
        'simplified_face_count': simplified_face_count,
        'normalization_scale': normalization_scale,
        'smoothing_iterations': smoothing_iterations,
        'extracted_features': features
    }

    print(f"Mesh preprocessing complete. Saved to {filepath}.")
    return preprocessing_results



# Add this function to simplify the mesh
def simplify_mesh(mesh, target_number_of_faces):
    """
    Simplify the mesh to a target number of faces.
    :param mesh: trimesh object
    :param target_number_of_faces: Desired number of faces after simplification
    :return: Tuple of simplified mesh and final face count
    """
    simplified_mesh = mesh.simplify_quadratic_decimation(target_number_of_faces)
    return simplified_mesh, len(simplified_mesh.faces)

# Add this function to normalize the mesh
def normalize_mesh(mesh):
    """
    Normalize the mesh to fit within a unit cube centered at the origin.
    :param mesh: trimesh object
    :return: Tuple of normalized mesh and normalization scale
    """
    centroid = mesh.centroid
    scale = 1 / max(mesh.extents)
    mesh.apply_translation(-centroid)
    mesh.apply_scale(scale)
    return mesh, scale


# Add this function to reduce noise by smoothing the mesh
def smooth_mesh(mesh, iterations=10):
    """
    Smooth the mesh using Laplacian smoothing.
    """
    L = laplacian_matrix(mesh.vertices, mesh.faces)
    I = csr_matrix(np.eye(mesh.vertices.shape[0]))  # Identity matrix

    for _ in range(iterations):
        mesh.vertices = spsolve(I - L, mesh.vertices)

    return mesh, iterations



# Add this function to extract geometric features from the mesh
def extract_features(mesh):
    """
    Extract geometric features from the mesh.
    :param mesh: trimesh object
    :return: Dictionary of features
    """
    features = {
        "volume": mesh.volume,
        "surface_area": mesh.area,
        "compactness": mesh.volume / (mesh.area ** (3/2)),
        "aspect_ratio": max(mesh.extents) / min(mesh.extents),
        # Add more features as needed
    }
    return features



def laplacian_matrix(vertices, faces):
    """
    Compute the Laplacian matrix of the mesh.
    """
    n_vertices = len(vertices)
    vertex_id_map = {j: i for i, j in enumerate(vertices)}

    # Compute weights for each face
    I = []
    J = []
    V = []
    for face in faces:
        for i in range(3):
            i1, i2, i3 = face[i], face[(i + 1) % 3], face[(i + 2) % 3]

            v1 = vertices[i2] - vertices[i1]
            v2 = vertices[i3] - vertices[i1]
            cot_alpha = np.dot(v1, v2) / np.linalg.norm(np.cross(v1, v2))

            I.append(i1)
            J.append(i2)
            V.append(cot_alpha)

            I.append(i2)
            J.append(i1)
            V.append(cot_alpha)

    L = csr_matrix((V, (I, J)), shape=(n_vertices, n_vertices))
    L.setdiag(-np.array(L.sum(axis=1)).flatten())

    return L

