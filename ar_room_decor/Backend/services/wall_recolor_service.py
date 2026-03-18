import cv2
from models.wall_segmentation_model import get_wall_mask
from models.wall_recolor import recolor_wall

def recolor(image_path, color):

    image = cv2.imread(image_path)

    mask = get_wall_mask(image_path)

    result = recolor_wall(image, mask, color)

    return result