from flask import Flask
from mongoengine import connect
from flask_cors import CORS, cross_origin

app = Flask(__name__)
# app.config['MONGO_DBNAME'] = 'comprank'
CORS(app)
connect('comprank')
