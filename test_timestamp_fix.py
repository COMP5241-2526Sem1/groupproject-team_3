"""
Test script to verify timestamp display fix
"""

from services.db_service import db_service
from models.activity import Activity
from datetime import datetime

def test_timestamp_fix():
    """Test that timestamps are stored and displayed correctly"""
    
    print("🔍 Testing Timestamp Display Fix\n")
    
    # Get sample activities with responses
    activities = list(db_service.find_many('activities', {}, limit=5))
    
    print(f"✅ Found {len(activities)} activities to check\n")
    
    issues_found = 0
    
    for activity in activities:
        activity_id = str(activity['_id'])
        title = activity.get('title', 'Untitled')
        responses = activity.get('responses', [])
        
        print(f"📝 Activity: {title}")
        print(f"   ID: {activity_id}")
        print(f"   Responses: {len(responses)}")
        
        if responses:
            for i, response in enumerate(responses[:3], 1):  # Check first 3 responses
                submitted_at = response.get('submitted_at')
                has_timestamp = response.get('timestamp')
                
                print(f"   Response {i}:")
                print(f"      - submitted_at: {submitted_at}")
                print(f"      - timestamp (old): {has_timestamp}")
                
                if submitted_at:
                    if isinstance(submitted_at, datetime):
                        formatted = submitted_at.strftime('%Y-%m-%d %H:%M:%S')
                        print(f"      ✅ Correctly formatted: {formatted}")
                    else:
                        print(f"      ⚠️  Not a datetime object: {type(submitted_at)}")
                        issues_found += 1
                else:
                    print(f"      ❌ Missing submitted_at field")
                    issues_found += 1
                    
                if has_timestamp:
                    print(f"      ⚠️  Old 'timestamp' field still present (should be removed)")
        
        print()
    
    print("\n" + "="*60)
    if issues_found == 0:
        print("✅ All timestamps are correctly stored!")
    else:
        print(f"⚠️  Found {issues_found} issue(s)")
        print("\nℹ️  Note: Existing responses might still have old field names.")
        print("   New responses will use 'submitted_at' field.")
    print("="*60)

def check_response_structure():
    """Check the structure of response data"""
    
    print("\n\n🔍 Checking Response Data Structure\n")
    
    activities = list(db_service.find_many('activities', {'responses': {'$exists': True, '$ne': []}}, limit=1))
    
    if not activities:
        print("❌ No activities with responses found")
        return
    
    activity = activities[0]
    responses = activity.get('responses', [])
    
    if responses:
        sample_response = responses[0]
        print("Sample Response Structure:")
        print("-" * 40)
        for key, value in sample_response.items():
            value_type = type(value).__name__
            if isinstance(value, datetime):
                value_str = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(value, list):
                value_str = f"[{len(value)} items]"
            else:
                value_str = str(value)[:50]
            
            print(f"{key:20s}: {value_str:30s} ({value_type})")
        print("-" * 40)

if __name__ == '__main__':
    test_timestamp_fix()
    check_response_structure()
