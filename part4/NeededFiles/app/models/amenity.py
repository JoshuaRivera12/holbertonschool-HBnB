#!/usr/bin/python3
from app.db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Amenity(db.Model):
    __tablename__ = 'amenities'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(128), nullable=False, unique=True)

    def __repr__(self):
        return f'<Amenity {self.name}>'

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name
        }
