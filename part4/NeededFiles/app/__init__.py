import os
from flask import Flask, jsonify
from flask_restx import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS
import redis

# Redis blocklist for JWT
jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)

# Import all models to ensure they are registered with SQLAlchemy
from .models.user import User
from .models.place import Place
from .models.country import Country
from .models.city import City
from .models.amenity import Amenity
from .models.review import Review
from .db import db, migrate


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Load configuration
    app.config.from_pyfile('config.py')
    
    # Configure JWT
    app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY', 'default-super-secret')
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config["JWT_COOKIE_SECURE"] = os.getenv('FLASK_ENV', 'development') == 'production'
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    jwt = JWTManager(app)

    # JWT blocklist callback
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token_in_redis = jwt_redis_blocklist.get(jti)
        return token_in_redis is not None

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # This is the critical part that creates the tables and seeds data
    with app.app_context():
        db.create_all()
        seed_database()

    # Import and register blueprints
    from .api.v1 import api_bp as api_v1_bp
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')

    # JWT error handlers
    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        return jsonify({"msg": "Invalid token", "status": "error"}), 422

    @jwt.unauthorized_loader
    def missing_token_callback(callback):
        return jsonify({"msg": "Missing token", "status": "error"}), 401
    
    # Root route for places to serve the front-end
    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    @app.route('/<path:path>')
    def static_files(path):
        return app.send_static_file(path)

    return app

def seed_database():
    if db.session.query(Place).count() == 0:
        print("Seeding database with sample data...")

        # Create a user for the places
        user = User.query.first()
        if not user:
            user = User(email="test@example.com", password="password", first_name="Test", last_name="User")
            db.session.add(user)
            db.session.commit()

        # Create a country and city for the places
        country = Country.query.first()
        if not country:
            country = Country(name="USA")
            db.session.add(country)
            db.session.commit()
        
        city = City.query.first()
        if not city:
            city = City(name="New York")
            city.country_id = country.id
            db.session.add(city)
            db.session.commit()

        # Create a few places
        place1 = Place(
            name="Cozy Cottage",
            description="A charming little place.",
            number_rooms=2,
            number_bathrooms=1,
            max_guests=4,
            price_by_night=100,
            latitude=40.7128,
            longitude=-74.0060,
            city_id=str(city.id),
            host_id=str(user.id)
        )
        place2 = Place(
            name="Luxury Loft",
            description="A modern loft with a great view.",
            number_rooms=3,
            number_bathrooms=2,
            max_guests=6,
            price_by_night=250,
            latitude=34.0522,
            longitude=-118.2437,
            city_id=str(city.id),
            host_id=str(user.id)
        )

        db.session.add(place1)
        db.session.add(place2)
        db.session.commit()
        print("Database seeded successfully.")
