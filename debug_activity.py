"""
Debug specific activity error
调试特定活动的错误
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.db_service import db_service
from bson import ObjectId

def debug_activity(activity_id):
    """
    Debug a specific activity to find the error
    """
    print("=" * 70)
    print(f"🔍 Debugging Activity: {activity_id}")
    print("=" * 70)
    print()
    
    activities_collection = db_service.get_collection('activities')
    
    try:
        # Try to find the activity
        activity = activities_collection.find_one({'_id': ObjectId(activity_id)})
        
        if not activity:
            print(f"❌ Activity not found with ID: {activity_id}")
            return
        
        print("✅ Activity found!")
        print()
        print("📋 Activity Details:")
        print(f"   Title: {activity.get('title', 'N/A')}")
        print(f"   Type: {activity.get('type', 'N/A')}")
        print(f"   Course ID: {activity.get('course_id', 'N/A')}")
        print(f"   Teacher ID: {activity.get('teacher_id', 'N/A')}")
        print(f"   Link: {activity.get('link', 'N/A')}")
        print(f"   Active: {activity.get('active', True)}")
        print(f"   AI Generated: {activity.get('ai_generated', False)}")
        print()
        
        # Check content structure
        print("📝 Content Structure:")
        content = activity.get('content', {})
        if content:
            for key, value in content.items():
                print(f"   {key}: {type(value).__name__} = {str(value)[:100]}")
        else:
            print("   ⚠️  Content is empty or missing!")
        print()
        
        # Check responses
        responses = activity.get('responses', [])
        print(f"📨 Responses: {len(responses)}")
        if responses:
            print("   Checking response structure...")
            for i, response in enumerate(responses, 1):
                print(f"   Response {i}:")
                for key, value in response.items():
                    print(f"      {key}: {type(value).__name__}")
        print()
        
        # Check if course exists
        print("🔗 Checking Course Reference:")
        courses_collection = db_service.get_collection('courses')
        course_id = activity.get('course_id')
        
        if course_id:
            try:
                course = courses_collection.find_one({'_id': ObjectId(course_id)})
                if course:
                    print(f"   ✅ Course found: {course.get('name', 'N/A')}")
                else:
                    print(f"   ❌ Course not found with ID: {course_id}")
            except Exception as e:
                print(f"   ❌ Error finding course: {e}")
        else:
            print("   ⚠️  No course_id in activity!")
        print()
        
        # Check all fields
        print("🔍 All Activity Fields:")
        for key in activity.keys():
            value = activity[key]
            print(f"   {key}: {type(value).__name__}")
        print()
        
        # Simulate template rendering
        print("🎨 Simulating Template Rendering:")
        try:
            # Check if we can access expected fields
            title = activity.get('title', 'No title')
            activity_type = activity.get('type', 'unknown')
            content = activity.get('content', {})
            
            print(f"   ✅ Title: {title}")
            print(f"   ✅ Type: {activity_type}")
            
            if 'question' in content:
                print(f"   ✅ Question: {content['question'][:50]}...")
            else:
                print(f"   ⚠️  No 'question' in content!")
            
            if activity_type == 'poll' and 'options' in content:
                print(f"   ✅ Options: {len(content['options'])} options")
            elif activity_type == 'poll':
                print(f"   ⚠️  Poll type but no 'options' in content!")
            
            # Check created_at
            if 'created_at' in activity:
                created_at = activity['created_at']
                print(f"   ✅ Created at: {created_at}")
                try:
                    formatted = created_at.strftime('%b %d')
                    print(f"   ✅ Can format date: {formatted}")
                except Exception as e:
                    print(f"   ❌ Cannot format date: {e}")
            else:
                print(f"   ⚠️  No 'created_at' field!")
            
        except Exception as e:
            print(f"   ❌ Template simulation error: {e}")
            import traceback
            traceback.print_exc()
        
        print()
        print("=" * 70)
        print("💡 Recommendations:")
        
        # Give specific recommendations
        issues = []
        
        if not content:
            issues.append("Content is empty - activity may not be fully created")
        
        if 'question' not in content:
            issues.append("Missing 'question' field in content")
        
        if activity_type == 'poll' and 'options' not in content:
            issues.append("Poll activity missing 'options' in content")
        
        if 'created_at' not in activity:
            issues.append("Missing 'created_at' timestamp")
        
        if issues:
            print("❌ Issues found:")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print("✅ No obvious issues detected")
        
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Error during debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    # The activity ID from the error URL
    activity_id = "68f8c64b6e1771d8d39209d7"
    debug_activity(activity_id)
