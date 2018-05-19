from .model import Model
from mongoengine import Document, StringField, IntField

class Item(Model):
    name = StringField(max_length=50)
    description = StringField(max_length=50)
    format = StringField(max_length=50)
    image_link = StringField(max_length=50)
    rating = IntField(default=0)

    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'format': self.format,
            'image_link': self.image_link,
            'rating': self.rating
        }
