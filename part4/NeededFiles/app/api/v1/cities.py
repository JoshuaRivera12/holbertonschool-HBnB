#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
from app.models.city import City

api = Namespace('cities', description='City operations')

city_model = api.model('City', {
    'id': fields.String(readOnly=True),
    'name': fields.String(required=True)
})

@api.route('/')
class CityList(Resource):
    @api.marshal_list_with(city_model)
    def get(self):
        """List all cities"""
        return facade.get_all_cities()

    @api.expect(city_model)
    @api.marshal_with(city_model, code=201)
    def post(self):
        """Create a new city"""
        return facade.create_city(api.payload), 201

@api.route('/<string:id>')
@api.param('id', 'The city identifier')
@api.response(404, 'City not found')
class City(Resource):
    @api.marshal_with(city_model)
    def get(self, id):
        """Get a city by ID"""
        city = facade.get_city_by_id(id)
        if not city:
            api.abort(404, "City not found")
        return city

    @api.expect(city_model)
    @api.marshal_with(city_model)
    def put(self, id):
        """Update a city by ID"""
        try:
            return facade.update_city(id, api.payload)
        except ValueError as e:
            api.abort(404, str(e))

    def delete(self, id):
        """Delete a city by ID"""
        try:
            facade.delete_city(id)
            return '', 204
        except ValueError as e:
            api.abort(404, str(e))
