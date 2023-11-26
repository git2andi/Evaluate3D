import trimesh

class SurfaceAnalyzer:
    def __init__(self, mesh):
        self.mesh = mesh

    def detect_disconnected_submeshes(self):
        """
        Detects disconnected submeshes in the model.
        :return: Number of disconnected submeshes or floating particles.
        """
        # Split the mesh into disconnected components
        components = self.mesh.split(only_watertight=False)

        # The number of disconnected submeshes is the total number of components minus one
        # (assuming the largest component is the main mesh)
        return len(components) - 1
