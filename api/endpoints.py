from flask_restx import Namespace, Resource, fields

ns = Namespace('users', description='User operations')

user_model = ns.model('User', {
    'id': fields.String(readonly=True, description='The user unique identifier'),
    'email': fields.String(required=True, description='The user email address'),
    'first_name': fields.String(required=True, description='The user first name'),
    'last_name': fields.String(required=True, description='The user last name'),
    'created_at': fields.DateTime(readonly=True, description='The user creation date'),
    'updated_at': fields.DateTime(readonly=True, description='The user update date')
})

# Mock data store
USERS = {}
next_user_id = 1

def validate_email_unique(email):
    for user in USERS.values():
        if user['email'] == email:
            ns.abort(409, "Email already exists.")

@ns.route('/')
class UserList(Resource):
    @ns.doc('list_users')
    @ns.marshal_list_with(user_model)
    def get(self):
        return list(USERS.values()), 200

    @ns.doc('create_user')
    @ns.expect(user_model)
    @ns.marshal_with(user_model, code=201)
    def post(self):
        global next_user_id
        data = ns.payload
        validate_email_unique(data['email'])
        if not data['first_name'] or not data['last_name']:
            ns.abort(400, "First name and last name cannot be empty.")
        user_id = str(next_user_id)
        user_data = {
            'id': user_id,
            'email': data['email'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        USERS[user_id] = user_data
        next_user_id += 1
        return user_data, 201

@ns.route('/<string:user_id>')
@ns.response(404, 'User not found')
@ns.param('user_id', 'The user identifier')
class User(Resource):
    @ns.doc('get_user')
    @ns.marshal_with(user_model)
    def get(self, user_id):
        if user_id not in USERS:
            ns.abort(404, "User not found")
        return USERS[user_id], 200

    @ns.doc('delete_user')
    @ns.response(204, 'User deleted')
    def delete(self, user_id):
        if user_id not in USERS:
            ns.abort(404, "User not found")
        del USERS[user_id]
        return '', 204

    @ns.doc('update_user')
    @ns.expect(user_model)
    @ns.marshal_with(user_model)
    def put(self, user_id):
        if user_id not in USERS:
            ns.abort(404, "User not found")
        data = ns.payload
        validate_email_unique(data.get('email', USERS[user_id]['email']))
        if not data['first_name'] or not data['last_name']:
            ns.abort(400, "First name and last name cannot be empty.")
        user_data = USERS[user_id]
        user_data.update({
            'email': data.get('email', user_data['email']),
            'first_name': data.get('first_name', user_data['first_name']),
            'last_name': data.get('last_name', user_data['last_name']),
            'updated_at': datetime.utcnow()
        })
        return user_data, 200
