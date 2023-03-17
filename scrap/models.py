from mongoengine import *

connect(host="mongodb+srv://Web9:567234@web9.3z5zqgw.mongodb.net/hw_9_scrapy", ssl=True)


class Authors(Document):
    fullname = StringField(required=True, unique=True)
    born_date = DateTimeField()
    born_location = StringField(max_length=300)
    description = StringField()


class Quotes(Document):
    tags = ListField(StringField())
    author = ReferenceField(Authors, reverse_delete_rule=CASCADE)
    quote = StringField(required=True)
    meta = {'allow_inheritance': True}
