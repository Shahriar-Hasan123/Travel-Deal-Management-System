"""Deal service helpers for CRUD operations."""

from database.models import Deal
from utils.validator import validate_deal_input
from database.models import db
from utils.logger import get_logger

logger = get_logger(__name__)


class DealService:
    @staticmethod
    def get_all_deals():
        """Return all deals as dictionaries."""
        deals = Deal.query.all()
        return [deal.to_dict() for deal in deals]

    @staticmethod
    def create_deal(data):
        """Validate and create a new deal record."""
        is_validate, errors = validate_deal_input(data)

        if not is_validate:
            return None, errors

        deal = Deal(
            destination=data["destination"].strip(),
            price=float(data["price"]),
            platform=data["platform"].strip(),
            rating=float(data["rating"]),
            travel_type=data["travel_type"],
        )

        db.session.add(deal)
        db.session.commit()

        return deal.to_dict(), None

    @staticmethod
    def get_deal_by_id(id):
        """Return a single deal by ID or None if not found."""
        deal = Deal.query.get(id)
        if deal is None:
            return None
        return deal.to_dict()

    @staticmethod
    def update_deal(deal_id, data):

        deal = Deal.query.get(deal_id)
        if not deal:
            return None, [f"Deal with id '{deal_id}' not found"], 404

        isValid, errors = validate_deal_input(data)
        if not isValid:
            return None, errors, 422

        deal.destination = data["destination"].strip()
        deal.price = float(data["price"])
        deal.platform = data["platform"].strip()
        deal.rating = float(data["rating"])
        deal.travel_type = data["travel_type"]

        db.session.commit()
        logger.info(f"Deal Updated: id={deal_id}")

        return deal.to_dict(), None, 200

    @staticmethod
    def delete_deal(deal_id):
        deal = Deal.query.get(deal_id)
        if not deal:
            logger.warning(f"Delete attempted on non-existent deal_id={deal_id}")
            return False, f"Deal with id '{deal_id}' not found"

        db.session.delete(deal)
        db.session.commit()

        logger.info(f"Deal deleted — id={deal_id}")
        return True, None
