from flask import Blueprint, request, jsonify
from services.recommendation_service import recommend_items

recommendation_bp = Blueprint("recommendation", __name__)

@recommendation_bp.route("/recommend", methods=["POST"])
def recommend():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Required fields
        budget = data.get("budget")
        color = data.get("color")

        if budget is None or color is None:
            return jsonify({
                "error": "Missing required fields: budget and color"
            }), 400

        # Optional location fields
        user_lat = data.get("latitude")
        user_lon = data.get("longitude")

        # Call service EXACTLY as defined
        items = recommend_items(
            budget,
            color,
            user_lat,
            user_lon
        )

        return jsonify({
            "status": "success",
            "count": len(items),
            "data": items
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500