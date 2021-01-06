import mongoengine as me
from . import me
import datetime


class TimePublished(me.Document):
    created = me.DateTimeField()
    modified = me.DateTimeField()
    meta = {
        'abstract': True,
    }

    def save(self, *args, **kwargs):
        self.created = datetime.datetime.now()
        super().save(*args, **kwargs)

    def modify(self, query=None, **update):
        self.modified = datetime.datetime.now()
        super().save(query=None, **update)


class News(TimePublished):
    title = me.StringField(required=True, min_length=2, max_length=256)
    body = me.StringField(required=True, min_length=2, max_length=2048)


class User(me.Document):
    telegram_id = me.IntField(primary_key=True)
    username = me.StringField(min_length=2, max_length=128)
    first_name = me.StringField(min_length=2, max_length=128)
    phone_number = me.StringField(max_length=13)
    email = me.EmailField(min_length=10)
    is_blocked = me.BooleanField(default=False)
    address = me.StringField(min_length=4)
    is_status_change = me.IntField(default=0)
    is_status_order = me.IntField(default=0)

    def formatted_data(self):
        return f'ID - {self.telegram_id}\nНикнейм - {self.username}\n' \
               f'Имя - {self.first_name}\nтелефон - {self.phone_number}\n' \
               f'email - {self.email}'

    def get_active_cart(self):
        cart = Cart.objects(user=self, is_active=True).first()
        if not hasattr(cart, 'id'):
            Cart(user=self).save()
            cart = Cart.objects(user=self, is_active=True).first()
            return cart
        return cart

    def get_active_order(self):
        order = Order.objects(user=self, is_active=True).first()
        return order

    @staticmethod
    def get_status_change(id_):
        user = User.objects.get(telegram_id=id_)
        user_status_change = user.is_status_change
        return user_status_change

    @staticmethod
    def get_is_order(id_):
        user = User.objects.get(telegram_id=id_)
        user_status_order = user.is_status_order
        return user_status_order


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


class CartProducts(me.EmbeddedDocument):
    product = me.ReferenceField(Product)
    title = me.StringField()
    count = me.IntField(default=1, min_value=1)
    price = me.FloatField()

    def __str__(self):
        total_price = self.count * self.price
        return f'{self.title}, Количество - {self.count}, Цена - {total_price}'


class Cart(TimePublished):
    user = me.ReferenceField(User, required=True)
    products = me.ListField(me.EmbeddedDocumentField(CartProducts))
    is_active = me.BooleanField(default=True)
    is_status = me.IntField(default=0)

    def add_product(self, product):
        is_product = False
        for p in self.products:
            if product.id == p.product.id:
                is_product = True
        if not is_product:
            cart_product = CartProducts(product=product, title=product.title, price=product.product_price)
            self.products.append(cart_product)
            self.save()
        return is_product

    def total_count(self):
        total_count = 0
        for p in self.products:
            total_count += p.count
        return total_count

    def total_price(self):
        total_price = 0
        for p in self.products:
            tmp_price = p.price * p.count
            total_price += tmp_price
        return total_price


class Order(TimePublished):
    user = me.ReferenceField(User, required=True)
    number = me.IntField(min_value=1, required=True)
    cart = me.ReferenceField(Cart, required=True)
    user_name = me.StringField(min_length=2, max_length=100)
    address = me.StringField(min_length=2)
    email = me.EmailField()
    phone = me.StringField(in_value=12)
    total_count = me.IntField()
    total_price = me.FloatField()
    is_active = me.BooleanField(default=True)