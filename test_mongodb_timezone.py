"""Test how get_hk_time() is stored in MongoDB"""
from config import Config
from pymongo import MongoClient
from utils.time_utils import get_hk_time
from datetime import datetime

client = MongoClient(Config.MONGODB_URI)
db = client[Config.DATABASE_NAME]

# Generate HK time
hk_time = get_hk_time()
print(f"Generated HK time: {hk_time}")
print(f"Timezone info: {hk_time.tzinfo}")
print(f"Is timezone-aware: {hk_time.tzinfo is not None}")

# Insert test document
test_doc = {
    'test_time': hk_time,
    'description': 'Test HK timezone storage'
}

result = db.test_collection.insert_one(test_doc)
print(f"\nInserted document ID: {result.inserted_id}")

# Retrieve and check
retrieved = db.test_collection.find_one({'_id': result.inserted_id})
retrieved_time = retrieved['test_time']

print(f"\nRetrieved time: {retrieved_time}")
print(f"Timezone info: {retrieved_time.tzinfo}")
print(f"Is timezone-aware: {retrieved_time.tzinfo is not None}")

# Compare
print(f"\nOriginal: {hk_time}")
print(f"Retrieved: {retrieved_time}")
print(f"Are equal: {hk_time == retrieved_time}")

# Cleanup
db.test_collection.delete_one({'_id': result.inserted_id})
print("\nTest document deleted")

print("\n" + "="*60)
print("IMPORTANT: MongoDB stores timezone-aware datetime as UTC")
print("But Python driver converts it back to the original timezone")
print("="*60)
