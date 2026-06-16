from flask import Blueprint
from services.stats_service import get_api_stats
from utils.response import success_response
from utils.logger import get_logger


logger = get_logger(__name__)

stats_bp = Blueprint("stats", __name__, url_prefix="/stats")

@stats_bp.route("", methods=["GET"])
def api_stats():
    stats = get_api_stats()
    logger.info("GET /stats — stats fetched")
    return success_response({"stats": stats})
