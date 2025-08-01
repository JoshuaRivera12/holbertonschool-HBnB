from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.services.facade import facade

api = Namespace('auth', description='Authentication related operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class UserLogin(Resource):
    @api.doc('user_login')
    @api.expect(login_model)
    def post(self):
        '''Log in a user and return a JWT access token'''
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {'message': 'Email and password are required'}, 400

        user = facade.get_user_by_email(email)

        # Fixed method call here
        if user and user.verify_password(password):
            access_token = create_access_token(identity=user.id)
            return {'message': 'Login successful', 'access_token': access_token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401

@api.route('/logout')
class UserLogout(Resource):
    @api.doc('user_logout')
    @jwt_required()
    def delete(self):
        '''Log out a user by blacklisting their JWT token'''
        jti = get_jwt()['jti']
        from app import jwt_redis_blocklist
        jwt_redis_blocklist.set(jti, "", ex=60 * 60 * 24)  # Token expires in 24 hours
        return {'message': 'Logout successful'}, 200
signup_model = api.model('SignUp', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name')
})

@api.route('/signup')
class UserSignup(Resource):
    @api.doc('user_signup')
    @api.expect(signup_model)
    def post(self):
        '''Register a new user'''
        data = request.json
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        if not all([email, password, first_name, last_name]):
            return {'message': 'All fields are required'}, 400

        # Check if user already exists
        if facade.get_user_by_email(email):
            return {'message': 'User already exists'}, 409

        # Create new user
        new_user = facade.create_user({
    'email': email,
    'password': password,
    'first_name': first_name,
    'last_name': last_name
})

        return {'message': 'User created successfully', 'user_id': new_user.id}, 201

