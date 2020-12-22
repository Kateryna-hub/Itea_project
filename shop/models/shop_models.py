import mongoengine as me
from . import me
from .extra_models import TimePublished


class User(me.Document):
    telegram_id = me.IntField(primary_key=True)
    username = me.StringField(min_length=2, max_length=128)
    first_name = me.StringField(min_length=2, max_length=128)
    phone_number = me.StringField(max_length=12)
    email = me.EmailField(min_length=10)
    is_blocked = me.BooleanField(default=False)
    address = me.StringField(min_length=4)
    is_status_change = me.IntField(default=0)

    def formatted_data(self):
        return f'ID - {self.telegram_id}\nНикнейм - {self.username}\n' \
               f'Имя - {self.first_name}\nтелефон - {self.phone_number}\n' \
               f'email - {self.email}'

    def get_active_card(self):
        cart = Cart.objects(user=self, is_active=True).first()
        if not cart:
            cart = Cart.objects.create(user=self)
            return cart
        return cart

    @staticmethod
    def get_status_change(id):
        user = User.objects.get(telegram_id=id)
        user_status_change = user.is_status_change
        return user_status_change


class Category(me.Document):
    title = me.StringField(required=True)
    description = me.StringField(min_length=10, max_length=512)
    parent = me.ReferenceField('self')
    subcategories = me.ListField(me.ReferenceField('self'))

    def get_products(self):
        return Product.objects(category=self)

    @classmethod
    def get_root_categories(cls):
        return cls.objects(
            parent=None
        )

    def is_root(self):
        return not bool(self.parent)

    def add_subcategory(self, category):
        category.parent = self
        category.save()
        self.subcategories.append(category)
        self.save()


class Parameters(me.EmbeddedDocument):
    height = me.FloatField()
    width = me.FloatField()
    weight = me.FloatField()
    additional_description = me.StringField()

    def __str__(self):
        return f'Высота/ширина/вес: {self.height}/{self.width}/{self.weight}\n' \
               f'{self.additional_description}'


class Product(me.Document):
    title = me.StringField(required=True, max_length=256)
    description = me.StringField(max_length=512)
    in_stock = me.BooleanField(default=True)
    discount = me.IntField(min_value=0, max_value=100, default=0)
    price = me.FloatField(required=True)
    image = me.FileField()
    category = me.ReferenceField(Category, required=True)
    parameters = me.EmbeddedDocumentField(Parameters)

    @property
    def product_price(self):
        return (100 - self.discount) / 100 * self.price


class Cart(TimePublished):
    user = me.ReferenceField(User, required=True)
    products = me.ListField(me.ReferenceField(Product))
    is_active = me.BooleanField(default=True)

    def add_product(self, product):
        self.products.append(product)
        self.save()


class OrderProduct(me.EmbeddedDocument):
    title = me.StringField()
    count = me.IntField()
    price = me.FloatField()

    def __str__(self):
        return f'{self.title}\nКоличество - {self.count}\nЦена - {self.price}'


class Order(TimePublished):
    number = me.IntField(min_value=1, required=True)
    user = me.StringField(min_length=2, max_length=100)
    address = me.StringField(max_length=2)
    email = me.StringField()
    phone = me.IntField(min_value=12)
    products = me.ListField(me.EmbeddedDocumentField(OrderProduct))
    total_count = me.IntField()
    total_price = me.IntField()


