from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Deal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
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
