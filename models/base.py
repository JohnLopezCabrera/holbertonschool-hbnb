# models/base.py
import uuid
from datetime import datetime

class BaseModel:
    """
    Base class for all models, providing common attributes and methods.
    """
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at

    def save(self):
        """
        Simulate saving the object to a database.
        """
        self.updated_at = datetime.utcnow()
        # Implement actual database save logic here.

    def delete(self):
        """
        Simulate deleting the object from a database.
        """
        # Implement actual database delete logic here.

    def to_dict(self):
        """
        Convert the object to a dictionary.
        """
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() + 'Z',
            'updated_at': self.updated_at.isoformat() + 'Z',
        }

