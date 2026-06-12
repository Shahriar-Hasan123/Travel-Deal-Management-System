from database.models import Deal
from utils.validator import validate_deal_input
from database.models import db


class DealService:
    @staticmethod
    def get_all_deals():
        deals = Deal.query.all()
        return [deal.to_dict() for deal in deals]

    @staticmethod
    def create_deal(data):
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
        deal = Deal.query.get(id)
        if deal is None:
            return None
        return deal.to_dict()
