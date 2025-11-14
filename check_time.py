"""Quick check of migrated data"""
from config import Config
from pymongo import MongoClient

client = MongoClient(Config.MONGODB_URI)
db = client[Config.DATABASE_NAME]

# Find activity with responses
act = db.activities.find_one({'responses': {'$exists': True, '$ne': []}})
if act and act.get('responses'):
    resp = act['responses'][-1]
    print(f"Activity: {act.get('title')}")
    print(f"Student: {resp.get('student_name')}")
    print(f"Submitted at (HK): {resp.get('submitted_at')}")
    print(f"\nThis time should be 8 hours ahead of the original UTC time")
