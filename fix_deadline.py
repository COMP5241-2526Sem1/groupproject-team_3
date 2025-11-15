"""Fix deadline for Software Testing activity"""
from config import Config
from pymongo import MongoClient
from datetime import timedelta

client = MongoClient(Config.MONGODB_URI)
db = client[Config.DATABASE_NAME]

# Find the activity
act = db.activities.find_one({'title': 'Software Testing Fundamentals Quiz'})

if act and act.get('deadline'):
    old_deadline = act['deadline']
    # Add 8 hours to convert UTC to HK time
    new_deadline = old_deadline + timedelta(hours=8)
    
    print(f"Activity: {act['title']}")
    print(f"Old deadline (UTC): {old_deadline}")
    print(f"New deadline (HKT): {new_deadline}")
    
    # Update
    result = db.activities.update_one(
        {'_id': act['_id']},
        {'$set': {'deadline': new_deadline}}
    )
    
    if result.modified_count > 0:
        print(f"✓ Updated!")
    else:
        print("No update needed")
else:
    print("Activity not found or no deadline")
