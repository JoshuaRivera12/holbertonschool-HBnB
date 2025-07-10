from models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = min(max(rating, 1), 5)
        self.place = place  # Place object
        self.user = user    # User object
