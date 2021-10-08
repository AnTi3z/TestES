from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"
ELASTICSEARCH_URL = "http://localhost:9200"

db = SQLAlchemy(app)
es = Elasticsearch(ELASTICSEARCH_URL)
