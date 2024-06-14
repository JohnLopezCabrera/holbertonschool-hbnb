import unittest
import json
from endpoints import app, db, user_repo
from models.user import User

class UserApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        db.users = {}
        db.next_id = 1

    def test_create_user(self):
        response = self.app.post('/users/', data=json.dumps({
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['email'], 'test@example.com')
        self.assertEqual(data['first_name'], 'John')
        self.assertEqual(data['last_name'], 'Doe')

    def test_get_user(self):
        user = User(email='test@example.com', first_name='John', last_name='Doe')
        user_repo.add_user(user)
        response = self.app.get(f'/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['email'], 'test@example.com')
        self.assertEqual(data['first_name'], 'John')
        self.assertEqual(data['last_name'], 'Doe')

    def test_update_user(self):
        user = User(email='test@example.com', first_name='John', last_name='Doe')
        user_repo.add_user(user)
        response = self.app.put(f'/users/{user.id}', data=json.dumps({
            'email': 'updated@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['email'], 'updated@example.com')
        self.assertEqual(data['first_name'], 'Jane')
        self.assertEqual(data['last_name'], 'Smith')

    def test_delete_user(self):
       

