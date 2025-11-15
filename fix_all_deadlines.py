"""Check and fix all activity deadlines that might be in UTC"""
from config import Config
from pymongo import MongoClient
from datetime import timedelta, datetime
from utils.time_utils import get_hk_time

client = MongoClient(Config.MONGODB_URI)
db = client[Config.DATABASE_NAME]

print("="*60)
print("CHECKING ALL ACTIVITY DEADLINES")
print("="*60)

# Find all activities with deadlines
activities = list(db.activities.find({'deadline': {'$exists': True, '$ne': None}}))

print(f"\nFound {len(activities)} activities with deadlines\n")

current_hk = get_hk_time()
suspicious_count = 0
fixed_count = 0

for activity in activities:
    deadline = activity['deadline']
    
    # Check if deadline looks suspicious (might be UTC instead of HK)
    # If deadline is in the past but created recently, and hour is suspiciously early
    # This indicates it might be UTC time that needs +8 hours
    
    is_suspicious = False
    
    # Check 1: If deadline is earlier today and activity is marked expired
    if deadline.date() == current_hk.date():
        # If deadline hour is < 16 (4pm), might be UTC (would be 12am-12am next day HKT)
        if deadline.hour < 16 and current_hk > deadline:
            is_suspicious = True
            reason = f"Same day deadline at {deadline.hour}:00 (might be UTC)"
    
    # Check 2: If deadline was today but in early hours (0-12)
    elif deadline.date() == current_hk.date() and deadline.hour < 12:
        is_suspicious = True
        reason = f"Early morning deadline at {deadline.hour}:00 (unusual)"
    
    if is_suspicious:
        suspicious_count += 1
        new_deadline = deadline + timedelta(hours=8)
        
        print(f"⚠️  {activity['title'][:50]}")
        print(f"    Old: {deadline} ({reason})")
        print(f"    New: {new_deadline}")
        
        # Ask to fix
        result = db.activities.update_one(
            {'_id': activity['_id']},
            {'$set': {'deadline': new_deadline}}
        )
        
        if result.modified_count > 0:
            print(f"    ✓ Fixed!")
            fixed_count += 1
        print()

print("="*60)
print(f"Summary:")
print(f"  Total activities with deadlines: {len(activities)}")
print(f"  Suspicious deadlines found: {suspicious_count}")
print(f"  Fixed: {fixed_count}")
print("="*60)
