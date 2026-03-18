from flask import Blueprint, request, jsonify
import os
import cv2

from services.wall_analysis_service import analyze_wall
from services.recommendation_service import recommend_colors
from services.image_generation_service import generate_wall_images


wall_ai_bp = Blueprint("wall_ai", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@wall_ai_bp.route("/wall-ai/recommend", methods=["POST"])
def recommend_wall():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]

    image_path = os.path.join(UPLOAD_FOLDER, file.filename)

    file.save(image_path)

    image = cv2.imread(image_path)

    if image is None:
        return jsonify({"error": "OpenCV failed to load image"}), 400

    try:

        mask, dominant_color, style = analyze_wall(image, image_path)

        colors = recommend_colors(style)

        images = generate_wall_images(image, mask, colors)

        return jsonify({
            "detected_style": style,
            "dominant_color": str(dominant_color),
            "recommended_images": images
        })

    except Exception as e:

        print("Wall AI error:", str(e))

        return jsonify({"error": str(e)}), 500