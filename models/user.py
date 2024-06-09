"""
Module for User class.
"""

from models.base import BaseModel
from models.review import Review

class User(BaseModel):
    """
    Class representing a user.
    """
    def __init__(self, email, password, first_name='', last_name=''):
        super().__init__()
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.places = []
        self.reviews = []

    def add_place(self, place):
        """
        Add a place to the user's list of places.

        :param place: Place object
        """
        self.places.append(place)

    def add_review(self, rating, text, place):
        """
        Add a review to the user's list of reviews if they are not the host of the place.

        :param rating: Rating of the review
        :param text: Text of the review
        :param place: Place object
        :return: Review object or str if review is not allowed
        """
        if place.host == self:
            return "The owner can't review their own place."

        review = Review(rating=rating, text=text, user=self, place=place)
        self.reviews.append(review)
        place.reviews.append(review)
        return review

    def some_public_method(self):
        """
        Example public method.
        """
        # Implementation here
        return "This is a public method."

