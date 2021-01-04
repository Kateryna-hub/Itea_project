from flask_restful import Resource
from flask import request
from shop.models.shop_models import User, Product, Category
from shop.models.extra_models import News
from shop.models.schemas import ProductSchemaRead, ProductSchemaWrite
from marshmallow.exceptions import ValidationError

import json


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
    def get(self, category=None):
        if category:
            categories = Category.objects(parent=category)
            return json.loads(categories.to_json())
        else:
            category = Category.objects()
            return json.loads(category.to_json())

    def post(self):
        pass

    def put(self, id):
        categories = Category.objects(id=id)
        categories.update(**request.json)
        categories.reload()
        return json.loads(categories.to_json())

    def delete(self, id):
        categories = Category.objects(id=id)
        categories.delete()
        text = f'Категория удалена'
        return text


class ProductResource(Resource):
    def get(self, product=None):
        if product:
            product = Product.objects(title__contains=product)
            return json.loads(product.to_json())
        else:
            product = Product.objects()
            return json.loads(product.to_json())

    def post(self):
        try:

            ProductSchemaWrite().load(request.json)
        except ValidationError as e:
            return {'text': str(e)}
        product = Product(**request.json).save()
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
    def get(self, news):
        if news:
            news = News.objects(title__contains=news)

            return json.loads(news.to_json())

    def post(self):
        pass

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