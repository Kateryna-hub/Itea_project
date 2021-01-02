from flask import Flask
from flask_restful import Api
from shop.bot.shop_bot import app
from .resources import UserResource, CategoryResource, ProductResource, NewsResource

app_rest = Flask(__name__)
api = Api(app_rest)


api.add_resource(UserResource, '/tg/user', '/tg/user/<string:telegram_id>')
api.add_resource(CategoryResource, '/tg/category', '/tg/category/<string:id>')
api.add_resource(ProductResource, '/tg/product', '/tg/product/<string:title>')
api.add_resource(NewsResource, '/tg/news')
