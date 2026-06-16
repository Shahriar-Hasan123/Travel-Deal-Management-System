from database.models import db, DealView, Deal
from utils.logger import get_logger

logger = get_logger(__name__)


def record_deal_view(deal_id):
    view_stat = DealView.query.filter_by(deal_id=deal_id).first()
    if view_stat:
        view_stat.view_count += 1
    else:
        view_stat = DealView(deal_id=deal_id, view_count=1)
        db.session.add(view_stat)
    
    db.session.commit()
    logger.info(f"View count incremented for deal_id={deal_id} - total={view_stat.view_count}")


def get_popular_deals(limit=5):
    results = DealView.query.join(Deal).filter(DealView.view_count > 0).order_by(DealView.view_count.desc()).limit(limit).all()
    logger.info(f"Popular deals fetched - {len(results)} deal(s)")
    return [r.to_dict() for r in results]
