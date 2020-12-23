from flask_restful import Resource
from flask import request
from shop.models.shop_models import User, Product, Category

import json


class ShopResource(Resource):

    def get(self, category=None, product=None, id=None, telegram_id=None):
        if category:
            categories = Category.objects(parent=category)
            return json.loads(categories.to_json())

        if product:
            product = Product.objects(title__contains=product)
            for p in product:
                p.modify(inc__view=1)
            return json.loads(product.to_json())
        if id:
            product = Product.objects(id=id)
            product.modify(inc__view=1)
            return json.loads(product.to_json())
        else:
            user = User.objects()
            # total_price = Product.objects.sum('price')
            # shop = json.dumps({"products": count_products, "total_price": total_price})
            return json.loads(user.to_json())

    def post(self):
        try:
            ShopProductSchemaWrite().load(request.json)
        except ValidationError as e:
            return {'text': str(e)}
        product = Product(**request.json).save()
        product.reload()
        return ShopProductSchemaRead().dump(product)

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