from models.diy_model import get_diy_by_item as fetch_diy


def get_diy_by_item(item_id):
    """
    Service layer for DIY guide.
    Can add business logic here later if needed.
    """
    return fetch_diy(item_id)