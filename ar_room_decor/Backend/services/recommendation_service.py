from models.furniture_model import get_furniture_by_budget_and_color
from models.shop_model import get_all_shops
from utils.haversine import calculate_distance


def recommend_items(budget, color, user_lat=None, user_lon=None):

    # Step 1: Fetch matching furniture items
    items = get_furniture_by_budget_and_color(budget, color)

    # Step 2: Fetch shop data once (optimization)
    shops = get_all_shops()
    shop_map = {shop["id"]: shop for shop in shops}

    ranked_items = []

    for item in items:

        # ------------------------
        # Budget Score
        # ------------------------
        if budget > 0:
            budget_score = max(0, 1 - (item["price"] / budget))
        else:
            budget_score = 0

        # ------------------------
        # Color Match Score
        # ------------------------
        if item["color"].lower() == color.lower():
            style_score = 1
        else:
            style_score = 0.5

        # ------------------------
        # Distance Score
        # ------------------------
        distance_score = 0
        shop_details = shop_map.get(item["shop_id"])

        if user_lat is not None and user_lon is not None and shop_details:

            distance = calculate_distance(
                user_lat,
                user_lon,
                shop_details["latitude"],
                shop_details["longitude"]
            )

            distance_score = max(0, 1 - (distance / 10))

        # ------------------------
        # Final Weighted Score
        # ------------------------
        final_score = (
            0.4 * budget_score +
            0.3 * style_score +
            0.3 * distance_score
        )

        ranked_item = {
            "id": item["id"],
            "name": item["furniture"],
            "category": item["category"],
            "price": item["price"],
            "color": item["color"],
            "style": item["style"],
            "score": round(final_score, 3),

            "shop": {
                "id": shop_details["id"],
                "name": shop_details["shop_name"],
                "address": shop_details["address"],
                "latitude": shop_details["latitude"],
                "longitude": shop_details["longitude"]
            }
        }

        ranked_items.append(ranked_item)

    ranked_items.sort(key=lambda x: x["score"], reverse=True)

    return ranked_items


# ------------------------------------------------
# NEW FUNCTION FOR WALL COLOR RECOMMENDATION
# ------------------------------------------------

def recommend_colors(style):

    palettes = {

        "modern interior design": [
            "soft white wall",
            "light grey wall",
            "navy blue wall"
        ],

        "minimalist interior design": [
            "white wall",
            "beige wall",
            "light grey wall"
        ],

        "traditional interior design": [
            "cream wall",
            "olive green wall",
            "warm beige wall"
        ],

        "industrial interior design": [
            "dark grey wall",
            "concrete wall",
            "charcoal wall"
        ],

        "scandinavian interior design": [
            "soft white wall",
            "pastel blue wall",
            "light wood tone wall"
        ]
    }

    return palettes.get(style, ["white wall", "light grey wall"])