import os

# Database configuration
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hbnb.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DB_FILE
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT configuration
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-super-secret')
