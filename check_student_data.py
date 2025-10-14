"""
Check student data structure
"""
from services.db_service import db_service
from models.course import Course
from models.activity import Activity
import json

# Connect to database
db = db_service.db

# Find student_demo
student = db.users.find_one({'username': 'student_demo'})

print("=== Student Data ===")
print(json.dumps({
    '_id': str(student['_id']),
    'username': student.get('username'),
    'email': student.get('email'),
    'role': student.get('role'),
    'student_id': student.get('student_id'),
    'enrolled_courses': [str(c) for c in student.get('enrolled_courses', [])]
}, indent=2))

# Check if any course exists
course_count = db.courses.count_documents({})
print(f"\n=== Total Courses in Database: {course_count} ===")

# Check enrolled courses using fixed Course model
enrolled = student.get('enrolled_courses', [])
print(f"\n=== Enrolled Courses: {len(enrolled)} ===")
for course_id in enrolled:
    # Use the fixed Course.find_by_id method
    course = Course.find_by_id(course_id)
    if course:
        print(f"✅ Course: {course.get('name')} (ID: {course_id})")
        # Count activities using fixed Activity model
        activities = list(Activity.find_by_course(course_id))
        print(f"   Activities: {len(activities)}")
    else:
        print(f"❌ Course not found: {course_id}")
