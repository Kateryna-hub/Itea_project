from flask import Flask
from flask_restful import Api
from .resources import UserResource, CategoryResource, ProductResource, NewsResource, OrderResource


app_rest = Flask(__name__)
api = Api(app_rest)


api.add_resource(UserResource, '/rtg/user', '/rtg/user/<string:telegram_id>')
api.add_resource(CategoryResource, '/rtg/category', '/rtg/category/<string:id>')
api.add_resource(ProductResource, '/rtg/product', '/rtg/product/<string:id>', '/rtg/product/<string:title>')
api.add_resource(NewsResource, '/rtg', '/rtg/news/<string:id>')
api.add_resource(OrderResource, '/rtg/order', '/rtg/order/<string:id>')

