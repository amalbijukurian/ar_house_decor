from database.supabase_client import supabase
from services.location_service import get_nearby_shop_ids

def recommend_items(budget, color, user_lat=None, user_lon=None):

    query = supabase.table("furniture") \
        .select("*") \
        .lte("price", budget) \
        .eq("color", color)

    if user_lat and user_lon:
        nearby_ids = get_nearby_shop_ids(user_lat, user_lon)
        if nearby_ids:
            query = query.in_("shop_id", nearby_ids)
        else:
            return []

    response = query.execute()
    return response.data