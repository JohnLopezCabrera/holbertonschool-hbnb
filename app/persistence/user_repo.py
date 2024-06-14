from models.user import User
from persistence.database import Database

class UserRepository:
    def __init__(self, db):
        self.db = db

    def add_user(self, user):
        user.id = self.db.generate_id()
        self.db.users[user.id] = user

    def get_user(self, user_id):
        return self.db.users.get(user_id)

    def get_all_users(self):
        return list(self.db.users.values())

    def update_user(self, user_id, user_data):
        user = self.db.users.get(user_id)
        if user:
            user.update(**user_data)
        return user

    def delete_user(self, user_id):
        if user_id in self.db.users:
            del self.db.users[user_id]

