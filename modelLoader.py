import trimesh

class ModelLoader:
    def load_model(self, filepath):
        """
        Loads a 3D model from a given file path.
        Currently supports only .obj file formats.
        """
        if filepath.endswith('.obj'):
            return self.load_obj(filepath)
        else:
            raise ValueError("Unsupported file format: only .obj files are supported.")

    def load_obj(self, filepath):
        """
        Loads an OBJ file.
        """
        try:
            return trimesh.load(filepath, force='mesh')
        except Exception as e:
            print(f"Error loading OBJ file: {e}")
            return None
