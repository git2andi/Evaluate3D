class ReportGenerator:
    def generate_report(self, analysis_results):
        report = "3D Model Analysis Report\n"
        report += "=========================\n"

        # Geometric Complexity
        if "vertex_count" in analysis_results and "face_count" in analysis_results:
            vertex_count = analysis_results["vertex_count"]
            face_count = analysis_results["face_count"]
            report += f"Geometric Complexity:\n"
            report += f" - Number of Vertices: {vertex_count}\n"
            report += f" - Number of Faces: {face_count}\n"

        # Include disconnected submeshes count
        if "disconnected_submeshes" in analysis_results:
            count = analysis_results["disconnected_submeshes"]
            report += f"Number of Disconnected Submeshes: {count}\n"

        # Include symmetry score
        if "symmetry_score" in analysis_results:
            score = analysis_results["symmetry_score"]
            report += f"Symmetry Score: {score:.2f}%\n"

        return report
