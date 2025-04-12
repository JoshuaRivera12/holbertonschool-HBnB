# HBnB Application Setup

## Directory Overview

The project follows a structured organization as outlined below:

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

### Breakdown:

- **`app/`** - Core application logic resides here.
- **`api/`** - Houses API routes, structured by version (`v1/`).
- **`models/`** - Defines business logic models such as `user.py`, `place.py`.
- **`services/`** - Implements the Facade pattern to manage inter-component interactions.
- **`persistence/`** - Provides an in-memory repository, which will later integrate SQLAlchemy.
- **`run.py`** - The main entry point for launching the Flask application.
- **`config.py`** - Handles configuration settings and environment variables.
- **`requirements.txt`** - Lists dependencies required for the project.
- **`README.md`** - Contains project documentation and usage guidelines.

## Setup Instructions

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

### 3. Install Required Dependencies

```bash
pip install -r requirements.txt
```

## Running the Project

### Start the Application

```bash
python run.py
```

Once the server is up and running, although no routes are active yet, this confirms the environment is correctly set up for further development.

