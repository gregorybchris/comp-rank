from mongoengine import connect
connect("comprank")
from app.topic import Topic
from app.comparison import Comparison
from app.item import Item
from app.category import Category


import csv

with open('data/tuxc.tsv') as names:
    reader = csv.DictReader(names, dialect='excel-tab')
    for row in reader:
        first = row['first']
        last = row['last']
        name = first + ' ' + last
        p = Item(name=name, description='XC Student Athlete', format='text')
        p.save()
