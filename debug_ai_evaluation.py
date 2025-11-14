"""
Debug script to check AI evaluation data structure
"""
from services.db_service import db_service
from bson import ObjectId
import json

# Activity ID from the error
activity_id = "6916d2131476b67917e4c381"

try:
    # Get the activity
    activity = db_service.find_one("activities", {"_id": ObjectId(activity_id)})
    
    if activity:
        print(f"Activity found: {activity.get('title')}")
        print(f"Activity type: {activity.get('type')}")
        print(f"\nResponses count: {len(activity.get('responses', []))}")
        
        # Check each response for ai_evaluation structure
        for i, response in enumerate(activity.get('responses', [])):
            print(f"\n--- Response {i+1} ---")
            print(f"Student: {response.get('student_name', response.get('student_id'))}")
            
            if 'ai_evaluation' in response:
                ai_eval = response['ai_evaluation']
                print(f"AI Evaluation exists: {type(ai_eval)}")
                
                if isinstance(ai_eval, dict):
                    print(f"  Keys: {list(ai_eval.keys())}")
                    print(f"  Score: {ai_eval.get('score', 'NOT FOUND')}")
                    print(f"  Feedback: {ai_eval.get('feedback', 'NOT FOUND')[:50] if ai_eval.get('feedback') else 'NOT FOUND'}...")
                    
                    # Check for problematic data types
                    for key, value in ai_eval.items():
                        print(f"  {key}: {type(value).__name__}")
                else:
                    print(f"  Warning: ai_evaluation is not a dict, it's {type(ai_eval)}")
                    print(f"  Value: {ai_eval}")
            else:
                print("No AI evaluation found")
                
            # Check for text or keywords field
            if 'text' in response:
                print(f"Has text field (length: {len(response['text'])})")
            if 'keywords' in response:
                print(f"Has keywords field: {response['keywords']}")
    else:
        print(f"Activity not found: {activity_id}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
