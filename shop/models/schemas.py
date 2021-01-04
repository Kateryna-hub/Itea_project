from marshmallow import Schema, fields
from marshmallow.validate import Length


class CategorySchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(validate=Length(min=2, max=65), required=True)
    parent = fields.Nested('self')
    subcategories = fields.Nested('self')


class ParametersSchema(Schema):
    id = fields.String(dump_only=True)
    height = fields.Float()
    width = fields.Float()
    weight = fields.Float()
    additional_description = fields.String()


class ProductSchemaRead(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True, max_length=256)
    description = fields.String(max_length=512)
    in_stock = fields.Boolean(default=True)
    price = fields.Float(required=True)
    image = fields.String()
    category = fields.Nested(CategorySchema)
    parameters = fields.Nested(ParametersSchema)


class ProductSchemaWrite(ProductSchemaRead):
    category = fields.String()


class UserSchema(Schema):
    id = fields.String(dump_only=True)
    telegram_id = fields.Integer(primary_key=True)
    username = fields.String(min_length=2, max_length=128)
    first_name = fields.String(min_length=2, max_length=128)
    phone_number = fields.String(max_length=13)
    email = fields.Email(min_length=10)
    is_blocked = fields.Boolean(default=False)
    address = fields.String(min_length=4)
    is_status_change = fields.Integer(default=0)
    is_status_order = fields.Integer(default=0)


class TimePublishedSchema(Schema):
    id = fields.String(dump_only=True)
    created = fields.DateTime()
    modified = fields.DateTime()


class CartProductsSchema(Schema):
    id = fields.String(dump_only=True)
    product = fields.Nested(ProductSchemaRead)
    title = fields.String()
    count = fields.Integer(default=1, min_value=1)
    price = fields.Float()


class CartSchema(TimePublishedSchema):
    id = fields.String(dump_only=True)
    user = fields.Nested(UserSchema, required=True)
    products = fields.Nested(CartProductsSchema)
    is_active = fields.Boolean(default=True)
    is_status = fields.Integer(default=0)


class OrderSchema(TimePublishedSchema):
    id = fields.String(dump_only=True)
    user = fields.Nested(UserSchema, required=True)
    number = fields.Integer(min_value=1, required=True)
    cart = fields.Nested(CartSchema, required=True)
    user_name = fields.String(min_length=2, max_length=100)
    address = fields.String(min_length=2)
    email = fields.Email()
    phone = fields.String(in_value=12)
    total_count = fields.Integer()
    total_price = fields.Float()
    is_active = fields.Boolean(default=True)

