import torch
import clip
from PIL import Image
import argparse

# Define command-line arguments
parser = argparse.ArgumentParser(description="Image Path and Prompt for CLIP")
parser.add_argument("--path", help="Path to the image file")
parser.add_argument("--prompt", nargs='+', help="Text prompts for CLIP")
args = parser.parse_args()

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

image_path = args.path
prompts = args.prompt

# Print image path and prompts for verification
print("Image path:", image_path)
print("Prompts:", prompts)

# Load and preprocess the image
image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
text = clip.tokenize(prompts).to(device)

with torch.no_grad():
    # Encode the image and text
    image_features = model.encode_image(image)
    text_features = model.encode_text(text)

    # Compute the logits and probabilities
    logits_per_image, logits_per_text = model(image, text)
    probs = logits_per_image.softmax(dim=-1).cpu().numpy()

# Print the label probabilities in decimal form
print("Label probabilities:", probs.tolist())
