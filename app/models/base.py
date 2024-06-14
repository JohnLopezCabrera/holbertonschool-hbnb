from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = None
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        self.updated_at = datetime.now()

# models/user.py
from models.base import BaseModel

class User(BaseModel):
    def __init__(self, email, first_name, last_name):
        super().__init__()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

# models/review.py
from models.base import BaseModel

class Review(BaseModel):
    def __init__(self, rating, text, user, place):
        super().__init__()
        self.rating = rating
        self.text = text
        self.user = user
        self.place = place
