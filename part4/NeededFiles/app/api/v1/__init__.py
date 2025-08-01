from flask import Blueprint
from flask_restx import Api

api_bp = Blueprint('api_v1', __name__)
api_v1 = Api(api_bp, version='1.0', title='HBnB Evolution API',
             description='The RESTful API for the HBnB Evolution project.')

from .users import api as user_ns
from .auth import api as auth_ns
from .places import api as places_ns
from .amenities import api as amenities_ns
from .cities import api as cities_ns
from .countries import api as countries_ns
from .reviews import api as reviews_ns

api_v1.add_namespace(user_ns, path='/users')
api_v1.add_namespace(auth_ns, path='/auth')
api_v1.add_namespace(places_ns, path='/places')
api_v1.add_namespace(amenities_ns, path='/amenities')
api_v1.add_namespace(cities_ns, path='/cities')
api_v1.add_namespace(countries_ns, path='/countries')
api_v1.add_namespace(reviews_ns, path='/reviews')
