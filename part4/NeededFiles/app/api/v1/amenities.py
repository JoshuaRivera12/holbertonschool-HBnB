#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
from app.models.amenity import Amenity

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'id': fields.String(readOnly=True),
    'name': fields.String(required=True)
})

@api.route('/')
class AmenityList(Resource):
    @api.marshal_list_with(amenity_model)
    def get(self):
        """List all amenities"""
        return facade.get_all_amenities()

    @api.expect(amenity_model)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity"""
        return facade.create_amenity(api.payload), 201

@api.route('/<string:id>')
@api.param('id', 'The amenity identifier')
@api.response(404, 'Amenity not found')
class Amenity(Resource):
    @api.marshal_with(amenity_model)
    def get(self, id):
        """Get an amenity by ID"""
        amenity = facade.get_amenity_by_id(id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity

    @api.expect(amenity_model)
    @api.marshal_with(amenity_model)
    def put(self, id):
        """Update an amenity by ID"""
        try:
            return facade.update_amenity(id, api.payload)
        except ValueError as e:
            api.abort(404, str(e))

    def delete(self, id):
        """Delete an amenity by ID"""
        try:
            facade.delete_amenity(id)
            return '', 204
        except ValueError as e:
            api.abort(404, str(e))
