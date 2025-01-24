from database import db
from datetime import datetime
from flask_login import UserMixin

class Meal(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now(datetime.timezone.utc))
    is_in_diet = db.Column(db.Boolean, nullable=False, default=True)