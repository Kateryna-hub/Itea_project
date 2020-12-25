from flask import Flask
from flask_restful import Api
from .resources import Resource

app_rest = Flask(__name__)
api = Api(app_rest)


api.add_resource(Resource, '/tg', '/tg/categories/<string:category>', '/tg/products/<string:product>',
                 '/tg/product/<string:id>', '/tg/user/<string:telegram_id>')