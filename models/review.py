# models/review.py
from models.base import BaseModel

class Review(BaseModel):
    """
    Class representing a review.
    """
    def __init__(self, rating, text, user, place):
        super().__init__()
        self.rating = rating
        self.text = text
        self.user = user
        self.place = place

    def to_dict(self):
        """
        Convert the review object to a dictionary.
        """
        review_dict = super().to_dict()
        review_dict.update({
            'rating': self.rating,
            'text': self.text,
            'user_id': self.user.id,
            'place_id': self.place.id
        })
        return review_dict

