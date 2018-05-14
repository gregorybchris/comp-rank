from flask import Flask
from mongoengine import connect

app = Flask(__name__)
# app.config['MONGO_DBNAME'] = 'comprank'
connect('comprank')
