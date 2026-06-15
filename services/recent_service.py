"""Services for tracking and fetching recently viewed deals."""

from database.models import db, RecentView
from utils.logger import get_logger
from datetime import datetime, timezone

logger = get_logger(__name__)


def record_view(deal_id):
    """Record or update a recent view for a deal."""
    existing = RecentView.query.filter_by(deal_id=deal_id).first()
    if existing:
        existing.viewed_at = datetime.now(timezone.utc)
        logger.info(f"Updated recent view timestamp for deal_id={deal_id}")
    else:
        db.session.add(RecentView(deal_id=deal_id))
        logger.info(f"Recorded new recent view for deal_id={deal_id}")

    db.session.commit()


def get_recently_viewed_deals():
    """Return the last 10 recently viewed deals."""
    recent_views = (
        RecentView.query.order_by(RecentView.viewed_at.desc()).limit(10).all()
    )

    if not recent_views:
        logger.info("Recently viewed deals requested - list is empty")
        return []

    deals = [view.deal.to_dict() for view in recent_views]
    logger.info(f"Recently viewed deals fetched - {len(deals)} deal(s)")
    return deals
