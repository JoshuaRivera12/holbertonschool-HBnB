from models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title[:100]
        self.description = description
        self.price = max(price, 0)
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner  # User object
        self.reviews = []   # list of Review objects
        self.amenities = [] # list of Amenity objects

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)
