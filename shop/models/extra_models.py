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


