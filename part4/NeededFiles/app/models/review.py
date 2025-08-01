#!/usr/bin/python3
from app.db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(UUID(as_uuid=True), db.ForeignKey('places.id'), nullable=False)

    def __repr__(self):
        return f'<Review {self.rating}>'

    def to_dict(self):
        return {
            'id': str(self.id),
            'text': self.text,
            'rating': self.rating,
            'user_id': str(self.user_id),
            'place_id': str(self.place_id)
        }
