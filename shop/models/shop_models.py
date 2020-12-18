import mongoengine as me
from . import me


class User(me.Document):
    telegram_id = me.IntField(primary_key=True)
    username = me.StringField(min_length=2, max_length=128)
    first_name = me.StringField(min_length=2, max_length=128)
    phone_number = me.StringField(max_length=12)
    email = me.EmailField()
    is_blocked = me.BooleanField(default=False)

    def formatted_data(self):
        return f'ID - {self.telegram_id}\nНикнейм - {self.username}\n' \
               f'Имя - {self.first_name}\nтелефон - {self.phone_number}\n' \
               f'email - {self.email}'


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




