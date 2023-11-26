import argparse
from modelLoader import ModelLoader
from surfaceAnalyzer import SurfaceAnalyzer
from reportGenerator import ReportGenerator
from symmetryAnalyzer import SymmetryAnalyzer
import preprocessOBJ

def main():
    parser = argparse.ArgumentParser(description='3D Model Analysis Tool')
    parser.add_argument('--mesh', required=True, help='Path to the 3D mesh file')
    args = parser.parse_args()

    # Check if the file is a .glb and convert it to .obj if necessary
    if args.mesh.endswith('.glb'):
        args.mesh = preprocessOBJ.convert_to_obj(args.mesh)

    # Preprocess the .obj file
    # preprocessOBJ.preprocess(args.mesh)

    # Load the model
    loader = ModelLoader()
    model = loader.load_model(args.mesh)

    if model is not None:
        # Perform analysis
        analyzer = SurfaceAnalyzer(model)
        disconnected_submeshes_count = analyzer.detect_disconnected_submeshes()
        
        symmetry_analyzer = SymmetryAnalyzer(model)
        symmetry_score = symmetry_analyzer.symmetry_score(plane='yz')  # Choose appropriate plane 'xy', 'xz', or 'yz'

        vertex_count = len(model.vertices)
        face_count = len(model.faces)
        # Generate report
        report_gen = ReportGenerator()
        report = report_gen.generate_report({
            "vertex_count": vertex_count,
            "face_count": face_count,
            "disconnected_submeshes": disconnected_submeshes_count,
            "symmetry_score": symmetry_score})
        print(report)
    else:
        print("Failed to load the model.")

if __name__ == "__main__":
    main()
