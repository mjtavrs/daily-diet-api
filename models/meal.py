from database import db
from datetime import datetime, timezone
from flask_login import UserMixin

class Meal(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    is_in_diet = db.Column(db.Boolean, nullable=False, default=True)

    # Method to convert the object data into a dictionary
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "date": self.date.isoformat(),
            "is_in_diet": self.is_in_diet
        }