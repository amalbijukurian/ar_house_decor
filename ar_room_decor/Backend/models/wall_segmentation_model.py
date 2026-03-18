import torch
import numpy as np
import cv2
from transformers import SegformerImageProcessor, SegformerForSemanticSegmentation
from PIL import Image


# Load segmentation model once
processor = SegformerImageProcessor.from_pretrained(
    "nvidia/segformer-b0-finetuned-ade-512-512"
)

model = SegformerForSemanticSegmentation.from_pretrained(
    "nvidia/segformer-b0-finetuned-ade-512-512"
)

model.eval()


def get_wall_mask(image_path):

    # Load image once
    image_cv = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)

    image = Image.fromarray(image_rgb)

    # Run segmentation
    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits

    upsampled_logits = torch.nn.functional.interpolate(
        logits,
        size=image.size[::-1],
        mode="bilinear",
        align_corners=False,
    )

    pred_seg = upsampled_logits.argmax(dim=1)[0].cpu().numpy()

    # ADE20K wall class
    wall_class = 0

    mask = np.zeros_like(pred_seg, dtype=np.uint8)
    mask[pred_seg == wall_class] = 255


    # -------------------------
    # 1. Morphological cleanup
    # -------------------------
    kernel = np.ones((7,7), np.uint8)

    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)


        # Smooth boundaries first
    mask = cv2.GaussianBlur(mask, (11,11), 0)

    # Edge protection AFTER smoothing
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 80, 160)

    edges = cv2.dilate(edges, np.ones((2,2), np.uint8))

    mask[edges > 0] = mask[edges > 0] * 0.2


    # -------------------------
    # 4. Prevent floor painting
    # -------------------------
    h, w = mask.shape
    mask[int(h*0.92):h, :] = 0


    return mask