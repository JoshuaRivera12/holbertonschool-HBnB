from app.db import db
from app.models.base import Base
import uuid

class Country(Base, db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(120), unique=True, nullable=False)
