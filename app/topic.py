from .model import Model
from .item import Item
from mongoengine import StringField, ListField, ReferenceField


class Topic(Model):
    name = StringField(max_length=50)
    description = StringField(max_length=50)
    items = ListField(ReferenceField(Item))

    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
        }
