# Evaluate3D
code asserting given 3D objects

Currently involves CLIP score and a rough symmetry check

How to use:

Evaluate Symmetry:

```python main.py --obj "path\to\object_file" --output_dir "\path\to\dir" --rotate [yes or no]```

All but Wonder3D require rotation. if no --rotate value is given, `yes` is assumed
