import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class Database:
    client = None
    database = None

def get_database():
    if Database.client is None:
        mongodb_url = os.getenv("MONGODB_URL")
        Database.client = MongoClient(mongodb_url)
        Database.database = Database.client[os.getenv("DATABASE_NAME", "ecommerce")]
    return Database.database

def close_database():
    if Database.client:
        Database.client.close()
        Database.client = None
        Database.database = None