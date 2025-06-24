import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import logging

# Initialize logger for the current module
logger = logging.getLogger(__name__)
# Set basic logging configuration to display DEBUG level messages
logging.basicConfig(level=logging.DEBUG)

# Debug line to check the DB_NAME environment variable
print("[*]ENV DB_NAME:", os.getenv("DB_NAME"))  # debug line

# MongoDB connection configuration:
# - Get MONGO_URI from environment variables or use default local MongoDB URI
# - Get DB_NAME from environment variables or use "asm" as default
# - The "or 'asm'" ensures DB_NAME is never empty if env var is empty string
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
DB_NAME = os.getenv("DB_NAME", "asm") or "asm"

# Create MongoDB client with:
# - The specified URI
# - Server API version 1 for stable API usage
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

# Get the database instance using the configured DB_NAME
db = client[DB_NAME]

# Log which database is being used for Celery operations
logger.info("[*]USING DB for CELERY: %s", db.name)