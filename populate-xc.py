from mongoengine import connect
connect("comprank")
from app.models.topic import Topic
from app.models.comparison import Comparison
from app.models.item import Item
from app.models.category import Category


import csv

with open('data/tuxc.tsv') as names:
    reader = csv.DictReader(names, dialect='excel-tab')
    for row in reader:
        first = row['first']
        last = row['last']
        name = first + ' ' + last
        p = Item(name=name, description='XC Student Athlete', format='text')
        p.save()
