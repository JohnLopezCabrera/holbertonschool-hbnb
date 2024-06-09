from flask import Flask, request, jsonify, abort
from flask_restx import Api, Resource, fields
import sys
sys.path.append('/home/johnlopez90/holbertonschool-hbnb')
from models.user import User
import datetime
app = Flask(__name__)
api = Api(app, version='1.0', title='User API', description='A simple User API')

# Mock database for storing user data
USERS = {}
next_user_id = 1

# Define user model for serialization/deserialization
user_model = api.model('User', {
    'id': fields.Integer(readonly=True, description='The user unique identifier'),
    'email': fields.String(required=True, description='The user email address'),
    'first_name': fields.String(required=True, description='The user first name'),
    'last_name': fields.String(required=True, description='The user last name'),
    'created_at': fields.DateTime(readonly=True, description='The user creation date'),
    'updated_at': fields.DateTime(readonly=True, description='The user update date')
})

# Function to validate email format
def validate_email_format(email):
    if '@' not in email or '.' not in email:
        abort(400, "Invalid email format.")

# Function to validate email uniqueness
def validate_email_unique(email):
    for user in USERS.values():
        if user['email'] == email:
            abort(409, "Email already exists.")

# Function to validate first name and last name
def validate_name(name, field_name):
    if not name.strip():
        abort(400, f"{field_name.capitalize()} cannot be empty.")

# Endpoint for creating users
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    def get(self):
        return list(USERS.values()), 200

    @api.doc('create_user')
    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        data = request.json
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        # Validate inputs
        validate_email_format(email)
        validate_email_unique(email)
        validate_name(first_name, 'first name')
        validate_name(last_name, 'last name')

        # Create user
        user = User(email=email, first_name=first_name, last_name=last_name,
                    created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
        user_id = next_user_id
        USERS[user_id] = user.__dict__
        user_dict = user.__dict__
        user_dict['id'] = user_id
        next_user_id += 1

        return user_dict, 201

api.add_resource(UserList, '/users')

# Endpoint for retrieving, updating, and deleting users by ID
@api.route('/users/<int:user_id>')
@api.response(404, 'User not found')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_model)
    def get(self, user_id):
        if user_id not in USERS:
            abort(404, "User not found")
        return USERS[user_id], 200

    @api.doc('update_user')
    @api.expect(user_model)
    @api.marshal_with(user_model)
    def put(self, user_id):
        if user_id not in USERS:
            abort(404, "User not found")

        data = request.json
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        # Validate inputs
        validate_email_format(email)
        validate_email_unique(email)
        validate_name(first_name, 'first name')
        validate_name(last_name, 'last name')

        # Update user
        USERS[user_id].update(data)
        USERS[user_id]['updated_at'] = datetime.datetime.now()

        return USERS[user_id], 200

    @api.doc('delete_user')
    @api.response(204, 'User deleted')
    def delete(self, user_id):
        if user_id not in USERS:
            abort(404, "User not found")
        del USERS[user_id]
        return '', 204

if __name__ == '__main__':
    app.run(debug=True)

