"""
Re-migrate only feedback_at timestamps that were missed
"""

from datetime import datetime, timezone, timedelta
from config import Config
from pymongo import MongoClient

# MongoDB connection
client = MongoClient(Config.MONGODB_URI)
db = client[Config.DATABASE_NAME]

# Hong Kong timezone
HK_TZ = timezone(timedelta(hours=8))

def convert_utc_to_hk(dt):
    """Add 8 hours to convert UTC to HK time"""
    if dt is None:
        return None
    
    if dt.tzinfo is not None:
        offset_hours = dt.utcoffset().total_seconds() / 3600 if dt.utcoffset() else 0
        if offset_hours == 8:
            return dt.replace(tzinfo=None)
        else:
            hk_time = dt.astimezone(HK_TZ)
            return hk_time.replace(tzinfo=None)
    
    # Naive datetime - add 8 hours
    hk_time = dt + timedelta(hours=8)
    return hk_time

print("="*60)
print("RE-MIGRATING FEEDBACK_AT TIMESTAMPS")
print("="*60)

collection = db['activities']
activities = list(collection.find({'responses.feedback_at': {'$exists': True}}))

print(f"\nFound {len(activities)} activities with feedback")

for activity in activities:
    activity_id = activity['_id']
    responses = activity.get('responses', [])
    
    for i, response in enumerate(responses):
        if 'feedback_at' in response:
            old_dt = response['feedback_at']
            
            # Check if it needs migration (hour < 12 might be UTC)
            # Or if tzinfo exists
            needs_migration = False
            
            if old_dt.tzinfo is not None:
                needs_migration = True
                print(f"  Found timezone-aware feedback_at: {old_dt}")
            elif old_dt.hour < 12:
                # Might be UTC (HK business hours are usually 9-22)
                # Check against current time
                now_hk = datetime.now(HK_TZ).replace(tzinfo=None)
                # If date is same and hour is suspiciously low, might be UTC
                if old_dt.date() == now_hk.date() and old_dt.hour < 12:
                    needs_migration = True
                    print(f"  Found suspicious time (might be UTC): {old_dt}")
            
            if needs_migration:
                new_dt = convert_utc_to_hk(old_dt)
                result = collection.update_one(
                    {'_id': activity_id},
                    {'$set': {f'responses.{i}.feedback_at': new_dt}}
                )
                if result.modified_count > 0:
                    print(f"    ✓ Updated: {old_dt} -> {new_dt}")

print("\n" + "="*60)
print("RE-MIGRATION COMPLETED")
print("="*60)
