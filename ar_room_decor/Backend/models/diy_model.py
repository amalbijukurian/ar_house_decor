from database.supabase_client import supabase


def get_diy_by_item(item_id):
    """
    Returns DIY installation guide for selected furniture item.
    """
    response = supabase.table("diy_guide") \
        .select("*") \
        .eq("item_id", item_id) \
        .execute()

    return response.data