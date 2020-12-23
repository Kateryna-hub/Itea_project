from flask import Flask
from flask_restful import Api
from .resources import Resource

app_rest = Flask(__name__)
api = Api(app_rest)


api.add_resource(Resource, '/tb', '/tb/categories/<string:category>', '/tb/products/<string:product>',
                 '/tb/product/<string:id>', '/tb/user/<string:telegram_id>')