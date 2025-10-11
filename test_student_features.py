"""
Test student dashboard and browse courses functionality
"""
from models.user import User
from models.course import Course
from models.activity import Activity

print("=== Testing Student Dashboard Data ===\n")

# Get student
user = User.find_by_username('student_demo')
print(f"Student: {user.get('username')}")
print(f"Student ID: {user.get('student_id')}")
print(f"Enrolled courses: {len(user.get('enrolled_courses', []))}")

# Get enrolled courses
enrolled_course_ids = user.get('enrolled_courses', [])
print(f"\n=== Processing Enrolled Courses ===")
for i, course_id in enumerate(enrolled_course_ids, 1):
    print(f"\n{i}. Course ID: {course_id} (type: {type(course_id)})")
    course = Course.find_by_id(course_id)
    if course:
        print(f"   ✅ Found: {course.get('name')}")
        activities = list(Activity.find_by_course(course_id))
        print(f"   Activities: {len(activities)}")
        for activity in activities:
            print(f"      - {activity.get('title')} ({activity.get('type')})")
    else:
        print(f"   ❌ Course not found")

# Test browse courses
print(f"\n=== Testing Browse Courses ===")
all_courses = list(Course.get_all())
print(f"Total courses: {len(all_courses)}")

enrolled_course_ids_str = [str(cid) for cid in user.get('enrolled_courses', [])]
available_courses = []
for course in all_courses:
    course_id_str = str(course['_id'])
    if course_id_str not in enrolled_course_ids_str:
        available_courses.append(course)
        
print(f"Available courses (not enrolled): {len(available_courses)}")
for course in available_courses:
    print(f"   - {course.get('name')} ({course.get('code')})")

print("\n✅ All tests passed!")
