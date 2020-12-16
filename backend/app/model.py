from mongoengine import Document, DateTimeField, BooleanField
from datetime import datetime


class Model(Document):
    meta = {'allow_inheritance': True, 'abstract': True}
    created_at = DateTimeField()
    modified_at = DateTimeField()
    enabled = BooleanField(default=True)

    def save(self, *args, **kwargs):
            if not self.created_at:
                self.created_at = datetime.now()
            self.modified_at = datetime.now()
            return super(Model, self).save(*args, **kwargs)
