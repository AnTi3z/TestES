from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from elasticsearch import AsyncElasticsearch

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
es = AsyncElasticsearch(app.config.get('ELASTICSEARCH_URL'))

from app import routes
