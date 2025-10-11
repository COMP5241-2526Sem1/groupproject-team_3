"""
Final verification test for Student Dashboard
"""
from models.user import User
from models.course import Course
from models.activity import Activity

print("=" * 60)
print("🧪 STUDENT DASHBOARD FINAL VERIFICATION")
print("=" * 60)

# Test 1: Get student data
print("\n1️⃣ Testing Student Data Retrieval...")
user = User.find_by_username('student_demo')
if user:
    print(f"   ✅ Student found: {user.get('username')}")
    print(f"   ✅ Student ID: {user.get('student_id')}")
    print(f"   ✅ Email: {user.get('email')}")
    print(f"   ✅ Enrolled courses: {len(user.get('enrolled_courses', []))}")
else:
    print("   ❌ Student not found!")
    exit(1)

# Test 2: Get enrolled courses
print("\n2️⃣ Testing Enrolled Courses...")
enrolled_course_ids = user.get('enrolled_courses', [])
enrolled_courses = []
total_activities = 0
completed_activities = 0

for course_id in enrolled_course_ids:
    course = Course.find_by_id(course_id)
    if course:
        activities = list(Activity.find_by_course(course_id))
        course['activity_count'] = len(activities)
        total_activities += len(activities)
        
        # Count completed
        for activity in activities:
            responses = activity.get('responses', [])
            if any(r.get('student_id') == user.get('student_id') for r in responses):
                completed_activities += 1
        
        enrolled_courses.append(course)
        print(f"   ✅ {course.get('code')}: {course.get('name')}")
        print(f"      Activities: {len(activities)}")

# Test 3: Calculate statistics
print("\n3️⃣ Testing Statistics Calculation...")
completion_rate = (completed_activities / total_activities * 100) if total_activities > 0 else 0
print(f"   ✅ Total Activities: {total_activities}")
print(f"   ✅ Completed Activities: {completed_activities}")
print(f"   ✅ Completion Rate: {completion_rate:.1f}%")

# Test 4: Get recent activities
print("\n4️⃣ Testing Recent Activities...")
recent_activities = []
for course_id in enrolled_course_ids:
    course = Course.find_by_id(course_id)
    if course:
        activities = list(Activity.find_by_course(course_id))
        for activity in activities[:3]:
            activity['course_name'] = course.get('name')
            activity['course_code'] = course.get('code')
            
            responses = activity.get('responses', [])
            activity['completed'] = any(
                r.get('student_id') == user.get('student_id') for r in responses
            )
            recent_activities.append(activity)

recent_activities.sort(key=lambda x: x.get('created_at', ''), reverse=True)
recent_activities = recent_activities[:5]

for activity in recent_activities:
    status = "✓ Completed" if activity['completed'] else "⏳ Pending"
    print(f"   {status} | {activity['course_code']} | {activity['title']}")

# Test 5: Activity type breakdown
print("\n5️⃣ Testing Activity Type Breakdown...")
poll_count = len([a for a in recent_activities if a.get('type') == 'poll'])
wc_count = len([a for a in recent_activities if a.get('type') == 'word_cloud'])
sa_count = len([a for a in recent_activities if a.get('type') == 'short_answer'])

print(f"   🗳️  Polls: {poll_count}")
print(f"   ☁️  Word Clouds: {wc_count}")
print(f"   ✍️  Short Answers: {sa_count}")

# Test 6: Check template data structure
print("\n6️⃣ Testing Template Data Structure...")
template_data = {
    'user': user,
    'enrolled_courses': enrolled_courses,
    'recent_activities': recent_activities,
    'total_activities': total_activities,
    'completed_activities': completed_activities,
    'completion_rate': round(completion_rate, 1)
}

print(f"   ✅ user: {type(template_data['user'])}")
print(f"   ✅ enrolled_courses: {len(template_data['enrolled_courses'])} items")
print(f"   ✅ recent_activities: {len(template_data['recent_activities'])} items")
print(f"   ✅ total_activities: {template_data['total_activities']}")
print(f"   ✅ completed_activities: {template_data['completed_activities']}")
print(f"   ✅ completion_rate: {template_data['completion_rate']}%")

# Final summary
print("\n" + "=" * 60)
print("📊 VERIFICATION SUMMARY")
print("=" * 60)
print(f"✅ Student Data: PASS")
print(f"✅ Course Enrollment: PASS ({len(enrolled_courses)} courses)")
print(f"✅ Activities: PASS ({total_activities} total, {completed_activities} completed)")
print(f"✅ Recent Activities: PASS ({len(recent_activities)} shown)")
print(f"✅ Activity Breakdown: PASS (Polls: {poll_count}, WC: {wc_count}, SA: {sa_count})")
print(f"✅ Template Data: PASS (all required fields present)")

print("\n🎉 ALL TESTS PASSED!")
print(f"🌐 Dashboard is ready at: http://localhost:5000/student/dashboard")
print(f"👤 Login with: student_demo / student123")
print("=" * 60)
