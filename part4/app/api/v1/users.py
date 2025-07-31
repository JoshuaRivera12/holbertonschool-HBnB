#!/usr/bin/python3
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services.facade import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'id': fields.String(readonly=True, description='The user unique identifier'),
    'email': fields.String(required=True, description='The user email address'),
    'first_name': fields.String(required=True, description='The user first name'),
    'last_name': fields.String(required=True, description='The user last name'),
})

registration_parser = api.parser()
registration_parser.add_argument('email', type=str, required=True, help='User email')
registration_parser.add_argument('password', type=str, required=True, help='User password')
registration_parser.add_argument('first_name', type=str, required=True, help='User first name')
registration_parser.add_argument('last_name', type=str, required=True, help='User last name')

login_parser = api.parser()
login_parser.add_argument('email', type=str, required=True, help='User email')
login_parser.add_argument('password', type=str, required=True, help='User password')

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        users = facade.get_all_users()
        return [user.to_dict() for user in users]

@api.route('/register')
class UserRegister(Resource):
    @api.doc('register_user')
    @api.expect(registration_parser)
    def post(self):
        """Create a new user"""
        data = registration_parser.parse_args()
        try:
            # The create_user method in facade expects 'password', not 'password_hash'
            new_user = facade.create_user(data)
            return new_user.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/login')
class UserLogin(Resource):
    @api.doc('login_user')
    @api.expect(login_parser)
    def post(self):
        """Logs a user into the system"""
        data = login_parser.parse_args()
        email = data.get('email')
        password = data.get('password')
        
        user = facade.verify_user(email, password)
        if user:
            access_token = create_access_token(identity=user.id)
            return {'message': 'Logged in successfully', 'token': access_token}, 200
        else:
            api.abort(401, 'Invalid email or password')

@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
class User(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_model)
    def get(self, user_id):
        """Fetch a user given its identifier"""
        user = facade.get_user_by_id(user_id)
        if not user:
            api.abort(404, "User not found")
        return user.to_dict()

    @api.doc('update_user')
    @api.expect(user_model)
    def put(self, user_id):
        """Update a user given its identifier"""
        data = request.json
        # Here you would implement your update logic
        return {'message': 'User updated successfully'}, 200

    @api.doc('delete_user')
    def delete(self, user_id):
        """Delete a user given its identifier"""
        # Here you would implement your delete logic
        return '', 204
