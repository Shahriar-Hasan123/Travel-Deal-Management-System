from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()


class Deal(db.Model):
    __tablename__ = "deals"
    
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    platform = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    travel_type = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        """model instance to dictionary for JSON response"""
        return {
            "id": self.id,
            "destination": self.destination,
            "price": self.price,
            "platform": self.platform,
            "rating": self.rating,
            "travel_type": self.travel_type,
        }


class RecentView(db.Model):
    __tablename__ = "recent_views"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    deal_id = db.Column(db.Integer, db.ForeignKey("deals.id", ondelete="CASCADE"), unique=True, nullable=False)
    viewed_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    
    deal = db.relationship("Deal", backref="recent_view")
