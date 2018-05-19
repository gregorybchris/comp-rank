import uuid
import os
from .model import Model
from .item import Item
from .topic import Topic
from mongoengine import Document, UUIDField, ReferenceField, StringField

def gen_comparison_key():
    return str(uuid.UUID(bytes=os.urandom(16)))

class Comparison(Model):
    item_a = ReferenceField(Item)
    item_b = ReferenceField(Item)
    topic = ReferenceField(Topic)
    address = StringField(max_length=50)
    winning_item = ReferenceField(Item)
    key = UUIDField(default=gen_comparison_key)

    def serialize(self):
        return {
            'item_a': self.item_a.serialize(),
            'item_b': self.item_b.serialize(),
            'key': self.key
        }
