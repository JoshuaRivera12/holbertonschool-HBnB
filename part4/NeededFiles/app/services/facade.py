#!/usr/bin/python3
from app.db import db
from app.models.amenity import Amenity
from app.models.city import City
from app.models.country import Country
from app.models.place import Place
from app.models.review import Review
from app.models.user import User
from sqlalchemy.exc import IntegrityError
from uuid import UUID

class Facade:
    def __init__(self):
        pass

    def get_user_by_id(self, user_id):
        """Get a user by their ID."""
        try:
            return db.session.get(User, UUID(user_id))
        except (ValueError, TypeError):
            return None

    def get_user_by_email(self, email):
        """Get a user by their email address."""
        return db.session.query(User).filter_by(email=email).first()

    def get_all_users(self):
        """Retrieve all users."""
        return db.session.query(User).all()

    def create_user(self, data):
        """Create a new user."""
        new_user = User(**data)
        db.session.add(new_user)
        try:
            db.session.commit()
            return new_user
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Email already exists")

    def update_user(self, user_id, data):
        """Update an existing user."""
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return user

    def delete_user(self, user_id):
        """Delete a user by ID."""
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        db.session.delete(user)
        db.session.commit()

    # --- Places ---
    def get_all_places(self):
        """Retrieve all places."""
        return db.session.query(Place).all()

    def get_place_by_id(self, place_id):
        """Get a place by its ID."""
        try:
            return db.session.get(Place, UUID(place_id))
        except (ValueError, TypeError):
            return None

    # --- Other entities (Countries, Cities, Amenities, Reviews) ---

    def create_country(self, data):
        """Create a new country."""
        new_country = Country(**data)
        db.session.add(new_country)
        db.session.commit()
        return new_country

    def get_all_countries(self):
        """Retrieve all countries."""
        return db.session.query(Country).all()

    def create_city(self, data):
        """Create a new city."""
        new_city = City(**data)
        db.session.add(new_city)
        db.session.commit()
        return new_city

    def get_all_cities(self, country_id=None):
        """Retrieve all cities."""
        query = db.session.query(City)
        if country_id:
            query = query.filter_by(country_id=country_id)
        return query.all()

    def create_amenity(self, data):
        """Create a new amenity."""
        new_amenity = Amenity(**data)
        db.session.add(new_amenity)
        db.session.commit()
        return new_amenity

    def get_all_amenities(self):
        """Retrieve all amenities."""
        return db.session.query(Amenity).all()

    def create_review(self, data):
        """Create a new review."""
        new_review = Review(**data)
        db.session.add(new_review)
        db.session.commit()
        return new_review

    def get_all_reviews(self):
        """Retrieve all reviews."""
        return db.session.query(Review).all()

facade = Facade()
