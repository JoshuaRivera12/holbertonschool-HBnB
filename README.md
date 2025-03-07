# HBnB Clone

## Overview
HBnB is a simplified clone of the popular AirBnB application. This project is designed to replicate core functionalities such as user management, property listings, reviews, and booking systems. It serves as a hands-on learning experience in full-stack web development, covering backend logic, database management, and API interactions.

## Features
- **User Authentication**: Users can register, log in, and manage their accounts.
- **Property Listings**: Hosts can create, update, and delete property listings.
- **Booking System**: Users can book available properties.
- **Reviews & Ratings**: Guests can leave reviews and rate properties.
- **RESTful API**: Provides endpoints for interacting with the application.
- **Database Integration**: Uses SQLAlchemy to manage data storage.

## Project Structure
```text
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
```

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository_url>
cd hbnb
```

### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python run.py
```

## API Documentation
The application provides a RESTful API with the following endpoints:

| Method | Endpoint        | Description |
|--------|----------------|-------------|
| GET    | /api/v1/users  | Retrieve all users |
| POST   | /api/v1/users  | Create a new user |
| GET    | /api/v1/places | Retrieve all places |
| POST   | /api/v1/places | Create a new place |
| GET    | /api/v1/reviews | Retrieve all reviews |

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch.
3. Make changes and commit.
4. Open a pull request.

## License
This project is for educational purposes and does not have a specific license.

