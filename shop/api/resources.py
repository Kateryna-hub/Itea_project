from flask_restful import Resource
from flask import request
from shop.models.shop_models import User, Product, Category, News, Order
from shop.models.schemas import ProductSchemaRead, ProductSchemaWrite, NewsSchema, CategorySchema
from shop.bot.sending_news import Sender
from marshmallow.exceptions import ValidationError

import json


class OrderResource(Resource):

    def get(self, id=None):
        if id:
            order = Order.objects(id=id)
            return json.loads(order.to_json())
        else:
            orders = Order.objects()
            return json.loads(orders.to_json())

    def put(self, id):
        order = Order.objects(id=id)
        order.update(**request.json)
        order.reload()
        return json.loads(order.to_json())

    def delete(self, id):
        order = Order.objects(id=id)
        order.delete()
        text = f'Заказ {order.number} удален'
        return text


class UserResource(Resource):

    def get(self, telegram_id=None):
        if telegram_id:
            user = User.objects(telegram_id=telegram_id)
            return json.loads(user.to_json())
        else:
            users = User.objects()
            return json.loads(users.to_json())

    def post(self):
        pass

    def put(self, telegram_id):
        user = User.objects(telegram_id=telegram_id)
        user.update(**request.json)
        user.reload()
        return json.loads(user.to_json())

    def delete(self, telegram_id):
        user = User.objects(telegram_id=telegram_id)
        user.delete()
        text = f'Пользователь удален'
        return text


class CategoryResource(Resource):
    def get(self, id=None):
        if id:
            categories = Category.objects(parent=id)
            return json.loads(categories.to_json())
        else:
            category = Category.objects()
            return json.loads(category.to_json())

    def post(self):
        try:
            CategorySchema().load(request.json)
        except ValidationError as e:
            return {'text': str(e)}
        categories = Category(**request.json)
        categories.save()
        categories.reload()
        return CategorySchema().dump(categories)

    def put(self, id):
        categories = Category.objects.get(id=id)
        categories.update(**request.json)
        categories.reload()
        return json.loads(categories.to_json())

    def delete(self, id):
        categories = Category.objects(id=id)
        categories.delete()
        text = f'Категория удалена'
        return text


class ProductResource(Resource):
    def get(self, id=None, title=None):
        if id:
            product = Product.objects(id=id)
            return json.loads(product.to_json())
        if title:
            product = Product.objects(title__contains=title)
            return json.loads(product.to_json())
        else:
            products = Product.objects()
            return json.loads(products.to_json())

    def post(self):
        try:
            ProductSchemaWrite().load(request.json)
        except ValidationError as e:
            return {'text': str(e)}
        product = Product(**request.json)
        product.save()
        product.reload()
        return ProductSchemaRead().dump(product)

    def put(self, id):
        product = Product.objects(id=id)
        product.update(**request.json)
        product.reload()
        return json.loads(product.to_json())

    def delete(self, id):
        product = Product.objects(id=id)
        product.delete()
        text = f'Товар удален'
        return text


class NewsResource(Resource):
    def get(self, id=None):
        if id:
            news = News.objects(id=id)
            return json.loads(news.to_json())
        else:
            news = News.objects()
            return json.loads(news.to_json())

    def post(self):
        try:
            NewsSchema().load(request.json)
        except ValidationError as e:
            return {'text': str(e)}
        news = News(**request.json)
        news.save()
        news.reload()
        show_news = f' {news.title}\n{news.body}'
        s = Sender(User.objects(), text=show_news)
        s.send_message()
        return NewsSchema().dump(news)

    def put(self, id):
        news = News.objects.get(id=id)
        news.update(**request.json)
        news.reload()
        return json.loads(news.to_json())

    def delete(self, id):
        news = News.objects(id=id)
        news.delete()
        text = f'Новость удалена'
        return text
