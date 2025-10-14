"""
Check course ID format
"""
from services.db_service import db_service
from bson import ObjectId

db = db_service.db

# Check all courses
print("=== All Courses ===")
for course in db.courses.find():
    print(f"ID Type: {type(course['_id'])} | ID: {course['_id']} | Name: {course.get('name')}")

# Check student's enrolled courses
student = db.users.find_one({'username': 'student_demo'})
enrolled = student.get('enrolled_courses', [])

print(f"\n=== Student's Enrolled Course IDs ===")
for cid in enrolled:
    print(f"Type: {type(cid)} | Value: {cid}")

print(f"\n=== Trying to find with string ID ===")
test_id = enrolled[0] if enrolled else None
if test_id:
    # Try string
    course1 = db.courses.find_one({'_id': test_id})
    print(f"String lookup: {course1}")
    
    # Try ObjectId
    course2 = db.courses.find_one({'_id': ObjectId(test_id)})
    print(f"ObjectId lookup: {course2 is not None}")
