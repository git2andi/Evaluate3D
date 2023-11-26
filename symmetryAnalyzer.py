import numpy as np
import trimesh
from scipy.spatial import KDTree

class SymmetryAnalyzer:
    def __init__(self, mesh):
        self.mesh = mesh

    def symmetry_score(self, plane='xz', tolerance=0.01):
        """
        Calculate the symmetry score with respect to a given plane.
        :param plane: A string indicating the symmetry plane ('xy', 'xz', or 'yz').
        :param tolerance: Distance tolerance for symmetry comparison.
        :return: Symmetry score as a percentage.
        """
        mirrored_mesh = self.mirror_mesh(plane)
        mirrored_tree = KDTree(mirrored_mesh.vertices)

        # For each vertex in the original mesh, find the closest vertex in the mirrored mesh
        distances, _ = mirrored_tree.query(self.mesh.vertices)

        # Count how many vertices fall within the tolerance distance
        symmetric_vertices = np.sum(distances < tolerance)
        score = symmetric_vertices / len(self.mesh.vertices) * 100
        return score
    
    def mirror_mesh(self, plane):
        """
        Mirror the mesh with respect to a given plane.
        :param plane: A string indicating the symmetry plane ('xy', 'xz', or 'yz').
        :return: A new trimesh.Trimesh object that is the mirrored version of the original mesh.
        """
        mirrored_vertices = np.copy(self.mesh.vertices)

        # Mirror vertices along the specified plane
        if plane == 'xy':
            mirrored_vertices[:, 2] = -mirrored_vertices[:, 2]
        elif plane == 'xz':
            mirrored_vertices[:, 1] = -mirrored_vertices[:, 1]
        elif plane == 'yz':
            mirrored_vertices[:, 0] = -mirrored_vertices[:, 0]
        else:
            raise ValueError("Invalid plane specified. Choose 'xy', 'xz', or 'yz'.")

        # Create a new mesh with mirrored vertices but the same faces
        return trimesh.Trimesh(vertices=mirrored_vertices, faces=self.mesh.faces, process=False)
