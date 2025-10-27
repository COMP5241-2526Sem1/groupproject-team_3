"""
Check activity responses structure in database
检查数据库中活动响应的数据结构
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.db_service import db_service
from models.activity import Activity
from datetime import datetime

def check_responses():
    """
    Check all activities and their response structures
    """
    print("=" * 70)
    print("🔍 Checking Activity Responses Structure")
    print("=" * 70)
    print()
    
    # Get all activities
    activities_collection = db_service.get_collection('activities')
    activities = list(activities_collection.find())
    
    print(f"Found {len(activities)} activities in database")
    print()
    
    issues_found = []
    
    for activity in activities:
        activity_id = str(activity['_id'])
        title = activity.get('title', 'Untitled')
        activity_type = activity.get('type', 'unknown')
        responses = activity.get('responses', [])
        
        print(f"📝 Activity: {title}")
        print(f"   ID: {activity_id}")
        print(f"   Type: {activity_type}")
        print(f"   Responses: {len(responses)}")
        
        if responses:
            print(f"   Checking response structure...")
            
            for i, response in enumerate(responses, 1):
                problems = []
                
                # Check common fields
                if 'student_id' not in response:
                    problems.append("Missing 'student_id'")
                
                if 'submitted_at' not in response:
                    problems.append("Missing 'submitted_at'")
                elif not isinstance(response['submitted_at'], datetime):
                    problems.append(f"'submitted_at' is {type(response['submitted_at']).__name__}, not datetime")
                
                # Check type-specific fields
                if activity_type == 'poll':
                    if 'selected_options' not in response:
                        problems.append("Poll response missing 'selected_options'")
                
                elif activity_type == 'short_answer':
                    if 'text' not in response:
                        problems.append("Short answer missing 'text'")
                
                elif activity_type == 'word_cloud':
                    if 'keywords' not in response:
                        problems.append("Word cloud missing 'keywords'")
                
                if problems:
                    print(f"   ⚠️  Response {i} has issues:")
                    for problem in problems:
                        print(f"      - {problem}")
                    print(f"      Current structure: {list(response.keys())}")
                    issues_found.append({
                        'activity_id': activity_id,
                        'activity_title': title,
                        'response_index': i,
                        'problems': problems,
                        'response': response
                    })
                else:
                    print(f"   ✅ Response {i}: OK")
        
        print()
    
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    
    if issues_found:
        print(f"❌ Found {len(issues_found)} problematic responses")
        print()
        print("Suggested fixes:")
        print("1. Add missing 'submitted_at' fields with datetime.utcnow()")
        print("2. Ensure type-specific fields exist (text, selected_options, keywords)")
        print()
        
        print("Would you like to fix these issues? (y/n)")
        # Don't auto-fix, just report
        
        print()
        print("Detailed issues:")
        for issue in issues_found:
            print(f"\nActivity: {issue['activity_title']}")
            print(f"Response #{issue['response_index']}")
            print(f"Problems: {', '.join(issue['problems'])}")
            print(f"Current data: {issue['response']}")
    
    else:
        print("✅ All responses have correct structure!")
        print("No issues found.")
    
    print()
    return len(issues_found) == 0

if __name__ == '__main__':
    try:
        all_ok = check_responses()
        if all_ok:
            print("✅ Database check completed - no issues!")
        else:
            print("⚠️  Database check completed - issues found (see above)")
    except Exception as e:
        print(f"❌ Error during check: {e}")
        import traceback
        traceback.print_exc()
