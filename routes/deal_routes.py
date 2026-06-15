from flask import Blueprint, request
from services.deal_service import DealService
from utils.response import success_response, error_response
from utils.query_validator import validate_search_params
from utils.logger import get_logger
from services.search_service import search_deals


logger = get_logger(__name__)

deal_bp = Blueprint("deals", __name__, url_prefix="/deals")


@deal_bp.route("", methods=["GET"])
def list_deals():
    deals = DealService.get_all_deals()
    return success_response({"total": len(deals), "deals": deals}, 200)


@deal_bp.route("", methods=["POST"])
def add_deal():
    data = request.get_json()
    if not data:
        return error_response("Request body must be valid JSON", 400)

    deal, errors = DealService.create_deal(data)

    if errors:
        return error_response("Validation failed", 422, error=errors)

    return success_response({"message": "Deal created successfully", "deal": deal}, 201)


@deal_bp.route("/<int:id>", methods=["GET"])
def get_deal(id):
    deal = DealService.get_deal_by_id(id)
    if not deal:
        return error_response(f"Deal with id {id} not found", 404)

    return success_response({"deal": deal}, 200)


@deal_bp.route("/search", methods=["GET"])
def search():
    destination = request.args.get("destination", "").strip() or None
    platform = request.args.get("platform", "").strip() or None
    travel_type = request.args.get("travel_type", "").strip() or None

    is_valid, errors = validate_search_params(destination, platform, travel_type)
    if not is_valid:
        logger.warning(f" GET /deals/search - Invalid params: {errors}")
        return error_response("Invalid search parameters", 400, error=errors)

    results = search_deals(destination, platform, travel_type)

    if not results:
        logger.info(" GET /deals/search - No match found")
        return success_response(
            {
                "message": "No deals matched your search criteria",
                "total": 0,
                "deals": [],
            }
        )

    return success_response({"total": len(results), "deals": results})
