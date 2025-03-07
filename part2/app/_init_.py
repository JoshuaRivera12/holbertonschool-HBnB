from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns

def create_app():
    app = Flask(_name)
    api = Api(app, version='0.1' title='Hbnb api BETA', description='This is the beta verion of the Hbnb Application Api')

    api.add_namespace(users_ns, path='/api/vi/users')
    return app
