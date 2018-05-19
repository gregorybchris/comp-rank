from .model import Model
from .topic import Topic
from mongoengine import StringField, ListField, ReferenceField


class Category(Model):
    name = StringField(max_length=50)
    description = StringField(max_length=50)
    topics = ListField(ReferenceField(Topic))

    def serialize(self):
        serialized_topics = [topic.serialize() for topic in self.topics
                             if topic.enabled]
        return {
            'id': str(self.id),
            'name': self.name,
            'topics': serialized_topics
        }
