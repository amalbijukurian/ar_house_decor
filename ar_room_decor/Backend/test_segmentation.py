import torch
import cv2
import numpy as np
import matplotlib.pyplot as plt
from transformers import SegformerImageProcessor, SegformerForSemanticSegmentation
from PIL import Image

# Load model
processor = SegformerImageProcessor.from_pretrained(
    "nvidia/segformer-b0-finetuned-ade-512-512"
)

model = SegformerForSemanticSegmentation.from_pretrained(
    "nvidia/segformer-b0-finetuned-ade-512-512"
)

# Load image
image_path = "test_room.jpg"

image = Image.open(image_path).convert("RGB")

# Preprocess
inputs = processor(images=image, return_tensors="pt")

# Run segmentation
with torch.no_grad():
    outputs = model(**inputs)

logits = outputs.logits

# Resize output to original image size
upsampled_logits = torch.nn.functional.interpolate(
    logits,
    size=image.size[::-1],
    mode="bilinear",
    align_corners=False,
)

pred_seg = upsampled_logits.argmax(dim=1)[0].cpu().numpy()

# ADE20K dataset class index for wall
wall_class = 0

# Create mask
wall_mask = np.zeros_like(pred_seg)
wall_mask[pred_seg == wall_class] = 255

# Show results
plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.title("Original Image")
plt.imshow(image)
plt.axis("off")

plt.subplot(1,2,2)
plt.title("Wall Mask")
plt.imshow(wall_mask, cmap="gray")
plt.axis("off")

plt.show()