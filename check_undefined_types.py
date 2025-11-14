"""
Test script to check if responses can be JSON serialized
"""
from services.db_service import db_service
from bson import ObjectId
import json

activity_id = "6916d2131476b67917e4c381"

try:
    # Get the activity
    activity = db_service.find_one("activities", {"_id": ObjectId(activity_id)})
    
    if activity:
        print(f"Activity: {activity.get('title')}")
        print(f"Type: {activity.get('type')}")
        
        responses = activity.get('responses', [])
        print(f"\nTotal responses: {len(responses)}")
        
        for i, response in enumerate(responses):
            print(f"\n--- Response {i+1} ---")
            print(f"Student: {response.get('student_name')}")
            
            # Check each field
            for key, value in response.items():
                print(f"  {key}: {type(value).__name__}")
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        print(f"    {sub_key}: {type(sub_value).__name__}")
            
            # Try to JSON serialize the response
            print("\n  Testing JSON serialization...")
            try:
                json_str = json.dumps(response, default=str)
                print(f"  ✅ Response is JSON serializable")
            except TypeError as e:
                print(f"  ❌ JSON serialization error: {e}")
                print(f"  Error type: {type(e)}")
                
                # Find which field causes the error
                for key, value in response.items():
                    try:
                        json.dumps({key: value}, default=str)
                    except TypeError as field_error:
                        print(f"    Problem field: {key} - {field_error}")
                
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

