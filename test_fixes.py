"""
Test dashboard and course detail after fixes
"""
from models.user import User
from models.course import Course
from models.activity import Activity

print("=" * 60)
print("🧪 TESTING DASHBOARD & COURSE DETAIL FIXES")
print("=" * 60)

# Test 1: Verify dashboard data
print("\n1️⃣ Testing Dashboard Data Structure...")
user = User.find_by_username('student_demo')
enrolled_course_ids = user.get('enrolled_courses', [])
enrolled_courses = []

for course_id in enrolled_course_ids[:3]:
    course = Course.find_by_id(course_id)
    if course:
        activities = list(Activity.find_by_course(course_id))
        course['activity_count'] = len(activities)
        enrolled_courses.append(course)
        print(f"   ✅ {course.get('code')}: {len(activities)} activities")

# Test 2: Check activity content structure
print("\n2️⃣ Testing Activity Content Structure...")
test_course_id = enrolled_course_ids[0]
activities = list(Activity.find_by_course(test_course_id))

for i, activity in enumerate(activities[:3], 1):
    print(f"\n   Activity {i}: {activity.get('title')}")
    print(f"   Type: {activity.get('type')}")
    
    content = activity.get('content', {})
    print(f"   Content keys: {list(content.keys())}")
    
    # Check for question or prompt
    if 'question' in content:
        q = content['question']
        print(f"   Question: {q[:80] if len(q) > 80 else q}...")
    elif 'prompt' in content:
        p = content['prompt']
        print(f"   Prompt: {p[:80] if len(p) > 80 else p}...")
    else:
        print(f"   ⚠️  No question/prompt found")

print("\n" + "=" * 60)
print("✅ Tests completed! Check results above.")
print("=" * 60)
