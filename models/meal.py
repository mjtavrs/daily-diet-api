from database import db
from flask_login import UserMixin

class Meal(db.Model, UserMixin):
    meal_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    isInDiet = db.Column(db.Boolean, nullable=False, default=True)