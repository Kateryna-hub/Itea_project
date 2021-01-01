from flask_restful import Resource
from flask import request
from shop.models.shop_models import User, Product, Category
from shop.models.extra_models import News
from marshmallow.exceptions import ValidationError
import json


class ShopResource(Resource):

    def get(self, category=None, product=None, id=None, telegram_id=None):
        if category:
            categories = Category.objects(parent=category)
            return json.loads(categories.to_json())

        if product:
            product = Product.objects(title__contains=product)

            return json.loads(product.to_json())
        if id:
            product = Product.objects(id=id)

            return json.loads(product.to_json())
        if telegram_id:
            user = User.objects(telegram_id=telegram_id)
            return json.loads(user.to_json())

        else:
            news = News.objects()
            return json.loads(news.to_json())

    def post(self):
        try:
            News().load(request.json)
        except ValidationError as e:
            return {'text': str(e)}
        product = Product(**request.json).save()
        product.reload()
        return News().dump(product)

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