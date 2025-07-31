#!/usr/bin/python3
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'id': fields.String(readonly=True, description='The place unique identifier'),
    'title': fields.String(required=True, description='The place title'),
    'description': fields.String(description='The place description'),
    'price': fields.Float(required=True, description='The price per night'),
    'image_url': fields.String(description='URL of the place image'),
    'owner_id': fields.String(required=True, description='The user ID of the owner'),
    'amenities': fields.List(fields.String, description='List of amenity IDs'),
    # You can add more fields here as needed
})

@api.route('') # This line was changed from @api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    def get(self):
        """List all places"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places]

    @api.doc('create_place')
    @api.expect(place_model, validate=True)
    @jwt_required()
    def post(self):
        """Create a new place"""
        data = request.json
        current_user_id = get_jwt_identity()
        data['owner_id'] = current_user_id
        try:
            new_place = facade.create_place(data)
            return new_place.to_dict(), 201
        except Exception as e:
            api.abort(400, str(e))

@api.route('/<string:place_id>')
@api.param('place_id', 'The place identifier')
class Place(Resource):
    @api.doc('get_place')
    def get(self, place_id):
        """Fetch a place given its identifier"""
        place = facade.get_place_by_id(place_id)
        if not place:
            api.abort(404, "Place not found")
        return place.to_dict()
