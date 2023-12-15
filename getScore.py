import torch
import clip
from PIL import Image
import argparse

parser = argparse.ArgumentParser(description="Image Path for CLIP")
parser.add_argument("--path", type=str, help="Path to the image file")
parser.add_argument("--prompt", type=str, help="Text prompt for CLIP")
args = parser.parse_args()

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

image_path = args.path
prompt = args.prompt

image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
text = clip.tokenize([prompt]).to(device)


with torch.no_grad():
    # Encode the image and text
    image_features = model.encode_image(image)
    text_features = model.encode_text(text)

    # Compute the logits and probabilities
    logits_per_image, logits_per_text = model(image, text)
    probs = logits_per_image.softmax(dim=-1).cpu().numpy()

# Print the label probabilities
print("Label probabilities:", probs)
