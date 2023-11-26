import trimesh

class ModelLoader:
    def load_model(self, filepath):
        """
        Loads a 3D model from a given file path.
        Currently supports only .obj file formats.
        """
        return trimesh.load(filepath, force='mesh')
        