#!/usr/bin/python3
from flask import jsonify
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
from app.models.place import Place
from flask_jwt_extended import jwt_required

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'id': fields.String(readOnly=True, description='The place unique identifier'),
    'name': fields.String(required=True, description='The name of the place'),
    'description': fields.String(description='The place description'),
    'number_rooms': fields.Integer(required=True, description='The number of rooms'),
    'number_bathrooms': fields.Integer(required=True, description='The number of bathrooms'),
    'max_guests': fields.Integer(required=True, description='The maximum number of guests'),
    'price_per_night': fields.Integer(required=True, description='The price per night'),
    'user_id': fields.String(required=True, description='The ID of the owner'),
    'city_id': fields.String(required=True, description='The ID of the city')
})

place_input_model = api.model('PlaceInput', {
    'name': fields.String(required=True),
    'description': fields.String(),
    'number_rooms': fields.Integer(required=True),
    'number_bathrooms': fields.Integer(required=True),
    'max_guests': fields.Integer(required=True),
    'price_per_night': fields.Integer(required=True),
    'user_id': fields.String(required=True),
    'city_id': fields.String(required=True)
})

@api.route('/', strict_slashes=False)
class PlaceList(Resource):
    @api.marshal_list_with(place_model)
    def get(self):
        """List all places"""
        return facade.get_all_places()

    @api.expect(place_input_model)
    @api.marshal_with(place_model, code=201)
    def post(self):
        """Create a new place"""
        return facade.create_place(api.payload), 201

@api.route('/<string:id>', strict_slashes=False)
@api.param('id', 'The place identifier')
@api.response(404, 'Place not found')
class Place(Resource):
    @api.marshal_with(place_model)
    def get(self, id):
        """Get a place by ID"""
        place = facade.get_place_by_id(id)
        if not place:
            api.abort(404, "Place not found")
        return place

    @api.expect(place_input_model)
    @api.marshal_with(place_model)
    def put(self, id):
        """Update a place by ID"""
        try:
            return facade.update_place(id, api.payload)
        except ValueError as e:
            api.abort(404, str(e))

    def delete(self, id):
        """Delete a place by ID"""
        try:
            facade.delete_place(id)
            return '', 204
        except ValueError as e:
            api.abort(404, str(e))
