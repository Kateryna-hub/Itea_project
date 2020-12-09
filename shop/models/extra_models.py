from .import me


class News(me.Document):
    title = me.StringField(required=True, min_length=2, max_length=256)
    body = me.StringField(required=True, min_length=2, max_length=2048)
    # TODO use abstract datetime class
