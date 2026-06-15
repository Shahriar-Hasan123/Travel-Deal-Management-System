"""Blueprint routes for deals and recent view endpoints."""

from flask import Blueprint, request
from services.deal_service import DealService
from utils.response import success_response, error_response
from utils.query_validator import (
    validate_search_params,
    validate_filter_params,
    validate_sort_params,
)
from utils.logger import get_logger
from services.search_service import search_deals, filter_deals_by_budget, sort_deals
from services.recent_service import get_recently_viewed_deals, record_view

logger = get_logger(__name__)

deal_bp = Blueprint("deals", __name__, url_prefix="/deals")


@deal_bp.route("", methods=["GET"])
def list_deals():
    """Return all travel deals."""
    deals = DealService.get_all_deals()
    return success_response({"total": len(deals), "deals": deals}, 200)


@deal_bp.route("", methods=["POST"])
def add_deal():
    """Create a new travel deal from request JSON."""
    data = request.get_json()
    if not data:
        return error_response("Request body must be valid JSON", 400)

    deal, errors = DealService.create_deal(data)

    if errors:
        return error_response("Validation failed", 422, error=errors)

    return success_response({"message": "Deal created successfully", "deal": deal}, 201)


@deal_bp.route("/<int:deal_id>", methods=["GET"])
def get_deal(deal_id):
    """Return a deal by ID and record it as viewed."""
    deal = DealService.get_deal_by_id(deal_id)
    if not deal:
        return error_response(f"Deal with id {deal_id} not found", 404)

    record_view(deal_id)
    return success_response({"deal": deal}, 200)


@deal_bp.route("/search", methods=["GET"])
def search():
    """Search deals by destination, platform, or travel type."""

    destination = request.args.get("destination", "").strip() or None
    platform = request.args.get("platform", "").strip() or None
    travel_type = request.args.get("travel_type", "").strip() or None

    is_valid, errors = validate_search_params(destination, platform, travel_type)
    if not is_valid:
        logger.warning(f"GET /deals/search - Invalid params: {errors}")
        return error_response("Invalid search parameters", 400, error=errors)

    results = search_deals(destination, platform, travel_type)

    if not results:
        logger.info("GET /deals/search - No match found")
        return success_response(
            {
                "message": "No deals matched your search criteria",
                "total": 0,
                "deals": [],
            }
        )

    return success_response({"total": len(results), "deals": results})


@deal_bp.route("/filter", methods=["GET"])
def filter_by_budget():

    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")

    if min_price is None and max_price is None:
        logger.warning("GET /deals/filter called with no parameters")
        return error_response("At least one of min_price or max_price is required", 400)

    is_valid, parsed, errors = validate_filter_params(min_price, max_price)

    if not is_valid:
        logger.warning(f"GET /deals/filter - validation failed: {errors}")
        return error_response("Invalid filter parameters", 400, error=errors)

    results = filter_deals_by_budget(parsed.get("min_price"), parsed.get("max_price"))
    if not results:
        logger.info(
            f"GET /deals/filter no deals in range min={parsed.get("min_price")} max={parsed.get("max_price")}"
        )
        return success_response(
            {
                "message": "No deals found in given price range",
                "total": 0,
                "deals": [],
            }
        )

    return success_response({"total": len(results), "deals": results})


@deal_bp.route("/sort", methods=["GET"])
def sort():
    """Sort deals by the requested field and order."""
    sort_by = request.args.get("sort_by")
    order = request.args.get("order")

    is_valid, errors = validate_sort_params(sort_by, order)

    if not is_valid:
        logger.warning(f"GET /deals/sort — invalid params: {errors}")
        return error_response("Invalid sort parameters", 400, error=errors)

    results = sort_deals(sort_by, order)

    logger.info(
        f"GET /deals/sort — sort_by={sort_by}, order={order}, returned {len(results)} deal(s)"
    )

    return success_response({"total": len(results), "deals": results})


@deal_bp.route("/recent", methods=["GET"])
def recently_viewed():
    """GET /deals/recent — Returns last 10 recently viewed deals."""
    deals = get_recently_viewed_deals()

    if not deals:
        return success_response(
            {"message": "No recently viewed deals", "total": 0, "deals": []}
        )

    return success_response({"total": len(deals), "deals": deals})
