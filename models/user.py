"""
Module for User class.
"""

from models.base import BaseModel
from models.review import Review
from datetime import datetime
import re

class User(BaseModel):
    """
    Class representing a user.
    """
    def __init__(self, email, password, first_name='', last_name=''):
        super().__init__()
        self.validate_email(email)
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at
        self.places = []
        self.reviews = []

    def add_place(self, place):
        """
        Add a place to the user's list of places.

        :param place: Place object
        """
        self.places.append(place)
        self.updated_at = datetime.utcnow()

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
        self.updated_at = datetime.utcnow()
        return review

    def update(self, email=None, password=None, first_name=None, last_name=None):
        """
        Update the user's information.

        :param email: New email address
        :param password: New password
        :param first_name: New first name
        :param last_name: New last name
        """
        if email:
            self.validate_email(email)
            self.email = email
        if password:
            self.password = password
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        self.updated_at = datetime.utcnow()

    @staticmethod
    def validate_email(email):
        """
        Validate the email address format.

        :param email: Email address to validate
        :raises ValueError: If the email format is invalid
        """
        email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format.")

    def to_dict(self):
        """
        Convert the user object to a dictionary format.

        :return: Dictionary representation of the user
        """
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat() + 'Z',
            'updated_at': self.updated_at.isoformat() + 'Z',
            'places': [place.id for place in self.places],
            'reviews': [review.id for review in self.reviews],
        }

    def some_public_method(self):
        """
        Example public method.
        """
        # Implementation here
        return "This is a public method."

