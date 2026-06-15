"""Search, filter, and sort helpers for deals."""

from database.models import Deal
from utils.logger import get_logger

logger = get_logger(__name__)


def search_deals(destination, platform, travel_type):
    """Return deals matching search criteria."""
    query = Deal.query

    if destination:
        query = query.filter(Deal.destination.ilike(f"%{destination}%"))
    if platform:
        query = query.filter(Deal.platform.ilike(f"%{platform}%"))
    if travel_type:
        query = query.filter(Deal.travel_type == travel_type.capitalize())

    results = query.all()
    logger.info(
        f"Search executed - destination={destination}, platform={platform}, travel_type={travel_type} - {len(results)} result(s)"
    )

    return [deal.to_dict() for deal in results]


def filter_deals_by_budget(min_price, max_price):
    """Return deals within the requested price range."""
    query = Deal.query

    if min_price is not None:
        query = query.filter(Deal.price >= min_price)
    if max_price is not None:
        query = query.filter(Deal.price <= max_price)

    results = query.all()
    logger.info(
        f"Filter executed - min_price={min_price}, max_price={max_price} - {len(results)} result(s)"
    )

    return [deal.to_dict() for deal in results]


def sort_deals(sort_by, order):
    """Return deals sorted by the given field."""
    sort_column = getattr(Deal, sort_by)  # example: sort_column = Deal.price
    sort_column = sort_column.desc() if order == "desc" else sort_column.asc()

    results = Deal.query.order_by(sort_column).all()

    logger.info(
        f"Sort executed - sort_by={sort_by}, order={order} - {len(results)} result(s)"
    )

    return [deal.to_dict() for deal in results]

