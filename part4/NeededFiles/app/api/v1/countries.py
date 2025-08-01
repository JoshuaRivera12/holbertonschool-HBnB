from flask_restx import Namespace, Resource, fields
from flask import jsonify, request
from app.services.facade import facade

api = Namespace('countries', description='Country related operations')

country_model = api.model('Country', {
    'id': fields.String(readOnly=True, description='The unique identifier for a country'),
    'name': fields.String(required=True, description='The country name')
})

@api.route('/')
class CountryList(Resource):
    @api.doc('list_countries')
    @api.marshal_list_with(country_model)
    def get(self):
        '''List all countries'''
        countries = facade.get_all_countries()
        return countries

    @api.doc('create_country')
    @api.expect(country_model)
    @api.marshal_with(country_model, code=201)
    def post(self):
        '''Create a new country'''
        new_country_data = request.json
        if not new_country_data or not new_country_data.get('name'):
            api.abort(400, 'Country name is required')
        
        try:
            new_country = facade.create_country(new_country_data)
            return new_country, 201
        except ValueError as e:
            api.abort(409, str(e))

@api.route('/<string:country_id>')
@api.param('country_id', 'The country identifier')
class Country(Resource):
    @api.doc('get_country')
    @api.marshal_with(country_model)
    def get(self, country_id):
        '''Fetch a country given its identifier'''
        country = facade.get_country_by_id(country_id)
        if not country:
            api.abort(404, "Country not found")
        return country
