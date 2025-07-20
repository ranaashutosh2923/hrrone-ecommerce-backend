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
        
        # Create indexes
        try:
            # Text index for product name
            Database.database.products.create_index([("name", "text")])
            # Compound index for product uniqueness check
            Database.database.products.create_index(
                [("name", 1), ("size", 1), ("price", 1)],
                unique=True
            )
        except Exception as e:
            print(f"Warning: Index creation failed: {str(e)}")
            
    return Database.database

def close_database():
    if Database.client:
        Database.client.close()
        Database.client = None
        Database.database = None