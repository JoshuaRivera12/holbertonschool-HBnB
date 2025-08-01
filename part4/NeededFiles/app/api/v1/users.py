#!/usr/bin/python3
from flask import jsonify
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
from app.models.user import User
from flask_jwt_extended import jwt_required

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'id': fields.String(readOnly=True, description='The user unique identifier'),
    'first_name': fields.String(required=True, description='The user first name'),
    'last_name': fields.String(required=True, description='The user last name'),
    'email': fields.String(required=True, description='The user email')
})

user_input_model = api.model('UserInput', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

@api.route('/', strict_slashes=False)
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        return facade.get_all_users()

    @api.expect(user_input_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        try:
            return facade.create_user(api.payload), 201
        except ValueError as e:
            api.abort(409, str(e))

@api.route('/<string:id>')
@api.param('id', 'The user identifier')
@api.response(404, 'User not found')
class User(Resource):
    @api.marshal_with(user_model)
    def get(self, id):
        """Get a user by ID"""
        user = facade.get_user_by_id(id)
        if not user:
            api.abort(404, "User not found")
        return user

    @api.expect(user_input_model)
    @api.marshal_with(user_model)
    def put(self, id):
        """Update a user by ID"""
        try:
            return facade.update_user(id, api.payload)
        except ValueError as e:
            api.abort(404, str(e))

    def delete(self, id):
        """Delete a user by ID"""
        try:
            facade.delete_user(id)
            return '', 204
        except ValueError as e:
            api.abort(404, str(e))#
