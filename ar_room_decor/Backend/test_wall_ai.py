import cv2
import numpy as np

from models.wall_segmentation_model import get_wall_mask
from models.wall_recolor import recolor_wall


# Test image
image_path = "C:\\Users\\adars\\Desktop\\ar_house_decor\\ar_room_decor\\Backend\\test_room.jpg"

# Load image
image = cv2.imread(image_path)

if image is None:
    print("Image not found")
    exit()

print("Image loaded")

# Step 1: Get segmentation mask
mask = get_wall_mask(image_path)

print("Mask generated")

# Save mask to verify segmentation
cv2.imwrite("wall_mask.png", mask)

# Step 2: Test recoloring
paint_color = [180, 80, 60]  # BGR color

recolored = recolor_wall(image, mask, paint_color)

# Save output
cv2.imwrite("recolored_wall.jpg", recolored)

print("Recolored image saved")