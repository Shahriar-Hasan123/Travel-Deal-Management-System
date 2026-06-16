from database.models import db, ApiStat, DealView, Deal
from utils.logger import get_logger
import json

logger = get_logger(__name__)


def _get_or_create_stat():
    stat = ApiStat.query.first()
    if not stat:
        stat = ApiStat()
        db.session.add(stat)
        db.session.commit()
    return stat


def record_request(success, destination=None):

    stat = _get_or_create_stat()
    stat.total_requests += 1

    if success:
        stat.successful_requests += 1
    else:
        stat.failed_requests += 1

    if destination:
        tally = json.loads(stat.search_destination_tally)
        key = destination.strip().lower()
        tally[key] = tally.get(key, 0) + 1
        stat.search_destination_tally = json.dumps(tally)

    db.session.commit()
    logger.info(f"API stat recorded — success={success}, destination={destination}")


def get_most_searched_destination():
    
    stat = ApiStat.query.first()
    if not stat:
        return None
    
    tally = json.loads(stat.search_destination_tally)
    if not tally:
        return None
    
    return max(tally, key=tally.get)


def get_api_stats():
    stat = ApiStat.query.first()
    if not stat:
        return {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "most_searched_destination": None,
            "most_viewed_deal": None,
        }

    # Use join to filter out orphaned records (where deal was deleted)
    most_viewed = DealView.query.join(Deal).order_by(DealView.view_count.desc()).first()

    return {
        "total_requests": stat.total_requests,
        "successful_requests": stat.successful_requests,
        "failed_requests": stat.failed_requests,
        "most_searched_destination": get_most_searched_destination(),
        "most_viewed_deal": most_viewed.to_dict() if most_viewed else None,
    }
