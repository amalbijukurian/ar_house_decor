from database.supabase_client import supabase

def calculate_total_cost(item_ids):
    response = supabase.table("furniture") \
        .select("price") \
        .in_("id", item_ids) \
        .execute()

    items = response.data
    total = sum(item["price"] for item in items)

    return {"total": total}