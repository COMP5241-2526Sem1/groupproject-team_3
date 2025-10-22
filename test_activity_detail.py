"""
Test activity detail view directly
直接测试活动详情视图
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from routes.activity_routes import activity_bp
from services.db_service import db_service
from bson import ObjectId

# Test the activity_detail function directly
def test_activity_detail():
    """
    Test activity detail rendering
    """
    print("=" * 70)
    print("🧪 Testing Activity Detail View")
    print("=" * 70)
    print()
    
    # The problematic activity ID
    activity_id = "68f8c64b6e1771d8d39209d7"
    
    print(f"Activity ID: {activity_id}")
    print()
    
    # Import the Activity model
    from models.activity import Activity
    from models.course import Course
    
    try:
        print("1️⃣ Finding activity...")
        activity = Activity.find_by_id(activity_id)
        
        if not activity:
            print("❌ Activity not found")
            return
        
        print(f"✅ Activity found: {activity.get('title')}")
        print()
        
        print("2️⃣ Finding course...")
        course_id = activity.get('course_id')
        print(f"   Course ID: {course_id}")
        
        course = Course.find_by_id(course_id)
        
        if not course:
            print(f"⚠️  Course not found with ID: {course_id}")
            print("   Creating fallback course object...")
            course = {
                'name': 'Unknown Course',
                'students': []
            }
        else:
            print(f"✅ Course found: {course.get('name')}")
            print(f"   Course has 'students' field: {'students' in course}")
            if 'students' not in course:
                print("   ⚠️  Adding empty 'students' field")
                course['students'] = []
        print()
        
        print("3️⃣ Preparing template data...")
        activity['_id'] = str(activity['_id'])
        responses = activity.get('responses', [])
        response_count = len(responses)
        
        print(f"   Activity ID (str): {activity['_id']}")
        print(f"   Response count: {response_count}")
        print(f"   Course name: {course.get('name')}")
        print(f"   Course students: {len(course.get('students', []))}")
        print()
        
        print("4️⃣ Simulating template rendering...")
        # Try to access fields like the template does
        try:
            # Template line 13
            course_name = course.get('name', 'Unknown') if course else 'Unknown'
            print(f"   ✅ Course name: {course_name}")
            
            # Template line 54-55
            if course and 'students' in course and course['students']:
                participation = ((response_count / len(course['students'])) * 100)
                print(f"   ✅ Participation rate: {participation:.0f}%")
            else:
                print(f"   ✅ Participation rate: N/A")
            
            # Template line 62
            if 'created_at' in activity:
                created = activity['created_at'].strftime('%b %d')
                print(f"   ✅ Created date: {created}")
            else:
                print(f"   ✅ Created date: N/A")
            
            print()
            print("✅ All template fields can be accessed successfully!")
            
        except Exception as e:
            print(f"   ❌ Template simulation error: {e}")
            import traceback
            traceback.print_exc()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 70)

if __name__ == '__main__':
    test_activity_detail()
