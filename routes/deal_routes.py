from flask import Blueprint, request
from services.deal_service import DealService
from utils.response import success_response, error_response

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
