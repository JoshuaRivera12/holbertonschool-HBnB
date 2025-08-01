from app.db import db
from app.models.base import Base
import uuid

class Place(Base, db.Model):
    __tablename__ = 'places'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(1024))
    number_rooms = db.Column(db.Integer, default=0)
    number_bathrooms = db.Column(db.Integer, default=0)
    max_guests = db.Column(db.Integer, default=1)
    price_by_night = db.Column(db.Integer, default=0)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    city_id = db.Column(db.String(36), db.ForeignKey('cities.id'), nullable=False)
    host_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
