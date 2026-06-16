"""Database models for travel deals and recent views."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()


class Deal(db.Model):
    """Travel deal record."""
    __tablename__ = "deals"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    destination = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    platform = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    travel_type = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        """Convert the model instance to a JSON-friendly dictionary."""
        return {
            "id": self.id,
            "destination": self.destination,
            "price": self.price,
            "platform": self.platform,
            "rating": self.rating,
            "travel_type": self.travel_type,
        }


class RecentView(db.Model):
    """Tracks recently viewed deals."""
    __tablename__ = "recent_views"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    deal_id = db.Column(db.Integer, db.ForeignKey("deals.id", ondelete="CASCADE"), unique=True, nullable=False)
    viewed_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    
    deal = db.relationship("Deal", backref="recent_view")

class DealView(db.Model):
    __tablename__="deal_views"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    deal_id=db.Column(db.Integer, db.ForeignKey("deals.id", ondelete="CASCADE"),nullable=False, unique=True)
    view_count=db.Column(db.Integer, nullable=False, default=False)

    deal = db.relationship("Deal", backref="view_stat")

    def to_dict(self):
        return {
            "deal": self.deal.to_dict(),
            "view_count":self.view_count,
        }


class ApiStat(db.Model):
    __tablename__ = "api_stats"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_requests = db.Column(db.Integer, nullable=False, default=0)
    successful_requests = db.Column(db.Integer, nullable=False, default=0)
    failed_requests = db.Column(db.Integer, nullable=False, default=0)
    # Column name matches existing database schema: 'search_destination_tally'
    search_destination_tally = db.Column(db.Text, nullable=False, default="{}")
