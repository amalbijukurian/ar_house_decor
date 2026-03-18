import clip
import torch
from PIL import Image

# Select device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load CLIP model
model, preprocess = clip.load("ViT-B/32", device=device)

# Interior style labels
STYLE_LABELS = [
    "modern interior design",
    "minimalist interior design",
    "traditional interior design",
    "industrial interior design",
    "scandinavian interior design"
]


def detect_style(image_path):
    """
    Detect interior design style from room image
    """

    try:
        # Load and preprocess image
        image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)

        # Convert style labels to text tokens
        text_inputs = clip.tokenize(STYLE_LABELS).to(device)

        with torch.no_grad():
            image_features = model.encode_image(image)
            text_features = model.encode_text(text_inputs)

            # Calculate similarity
            similarity = (image_features @ text_features.T).softmax(dim=-1)

        # Get best style match
        index = similarity.argmax().item()

        return STYLE_LABELS[index]

    except Exception as e:
        print("Style detection error:", e)
        return "modern interior design"