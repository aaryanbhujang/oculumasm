import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
print("[*]ENV DB_NAME:", os.getenv("DB_NAME"))  # debug line

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
DB_NAME = os.getenv("DB_NAME", "asm") or "asm"

client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client[DB_NAME]
logger.info("[*]USING DB for CELERY: %s", db.name)
