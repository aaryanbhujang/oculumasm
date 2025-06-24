from flask import current_app
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def init_db(app):
    mongo_uri = app.config['MONGO_URI']
    client = MongoClient(mongo_uri, server_api=ServerApi('1'), connect=False)
    app.db = client["asm"]