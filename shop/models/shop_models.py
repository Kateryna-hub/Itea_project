import mongoengine as me
import datetime

me.connect('SHOP')


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


class User(TimePublished):
    telegram_id = me.IntField(primary_key=True)
    username = me.StringField(min_length=2, max_length=128)
    phone_number = me.StringField(max_length=12)
    email = me.EmailField()
    is_blocked = me.BooleanField(default=False)


