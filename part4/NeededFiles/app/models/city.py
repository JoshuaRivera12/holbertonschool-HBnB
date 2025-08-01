from app.db import db
from app.models.base import Base
import uuid

class City(Base, db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(120), nullable=False)
    country_id = db.Column(db.String(36), db.ForeignKey('countries.id'), nullable=False)
    
    places = db.relationship('Place', backref='city', lazy='dynamic')
