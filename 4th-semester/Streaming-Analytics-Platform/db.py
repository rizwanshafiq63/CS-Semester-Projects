import os
from pymongo import MongoClient

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = "new_streaming"

_client_cache = None

def get_client():
    global _client_cache
    if _client_cache is None:
        _client_cache = MongoClient(MONGODB_URI)
    return _client_cache

def get_db():
    client = get_client()
    return client[DB_NAME]

def test_connection():
    try:
        client = get_client()
        client.admin.command('ismaster')
        print("✓ MongoDB connection successful")
        return True
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()