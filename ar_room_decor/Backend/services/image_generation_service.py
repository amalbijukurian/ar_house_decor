import cv2
import os
from models.wall_recolor import recolor_wall

OUTPUT_FOLDER = "outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def generate_wall_images(image, mask, colors):

    output_images = []

    for i, color in enumerate(colors):

        recolored = recolor_wall(image, mask, color)

        path = os.path.join(OUTPUT_FOLDER, f"wall_color_{i}.jpg")

        cv2.imwrite(path, recolored)

        output_images.append(path)

    return output_images