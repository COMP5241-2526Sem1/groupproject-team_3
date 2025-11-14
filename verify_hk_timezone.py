"""
Verify that all timestamps are now in Hong Kong timezone
"""

from config import Config
from pymongo import MongoClient
from datetime import timezone, timedelta

# MongoDB connection
client = MongoClient(Config.MONGODB_URI)
db = client[Config.DATABASE_NAME]

HK_TZ = timezone(timedelta(hours=8))

def verify_collection_timezones():
    """Check all activity responses for timezone info"""
    print("="*60)
    print("VERIFYING HONG KONG TIMEZONE IN DATABASE")
    print("="*60)
    
    # Check activities with responses
    activities = list(db.activities.find(
        {'responses': {'$exists': True, '$ne': []}},
        {'_id': 1, 'title': 1, 'responses': 1}
    ).limit(5))
    
    print(f"\nChecking {len(activities)} recent activities with responses:\n")
    
    for activity in activities:
        print(f"Activity: {activity.get('title', 'Untitled')}")
        print(f"ID: {activity['_id']}")
        
        responses = activity.get('responses', [])
        if responses:
            latest_response = responses[-1]  # Get most recent response
            
            submitted_at = latest_response.get('submitted_at')
            student_name = latest_response.get('student_name', 'Unknown')
            
            print(f"  Latest response from: {student_name}")
            
            if submitted_at:
                print(f"  Submitted at: {submitted_at}")
                
                # Check if timezone-aware
                if submitted_at.tzinfo is not None:
                    tz_offset = submitted_at.utcoffset()
                    hours = tz_offset.total_seconds() / 3600
                    print(f"  ✓ Timezone: UTC{hours:+.0f}:00")
                    
                    if hours == 8:
                        print(f"  ✓ Correct: Hong Kong Time (UTC+8)")
                    else:
                        print(f"  ✗ Wrong: Expected UTC+8, got UTC{hours:+.0f}:00")
                else:
                    print(f"  ✗ Warning: No timezone info (naive datetime)")
            else:
                print(f"  ✗ No submitted_at field")
        
        print()
    
    print("="*60)
    print("VERIFICATION COMPLETE")
    print("="*60)

if __name__ == '__main__':
    try:
        verify_collection_timezones()
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
