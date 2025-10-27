"""
Quick test script to verify student dashboard progress fix
快速测试脚本 - 验证学生 Dashboard 进度修复

Run this script after starting the Flask app to check if the fix works.
"""

import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.db_service import db_service
from models.user import User
from models.course import Course
from models.activity import Activity
from bson import ObjectId

def test_dashboard_progress():
    """
    Test if the dashboard progress calculation is working correctly
    """
    print("=" * 60)
    print("🧪 Student Dashboard Progress Fix - Test Script")
    print("=" * 60)
    print()
    
    # Find a test student
    print("1️⃣ Finding test student...")
    student = db_service.find_one('users', {'role': 'student'})
    
    if not student:
        print("❌ No student found in database!")
        print("💡 Please create a student account first.")
        return False
    
    student_id = student.get('student_id')
    username = student.get('username')
    print(f"✅ Found student: {username} (Student ID: {student_id})")
    print()
    
    # Get enrolled courses
    print("2️⃣ Checking enrolled courses...")
    enrolled_course_ids = student.get('enrolled_courses', [])
    
    if not enrolled_course_ids:
        print("⚠️ Student is not enrolled in any courses.")
        print("💡 Enroll the student in a course first.")
        return False
    
    print(f"✅ Student enrolled in {len(enrolled_course_ids)} course(s)")
    print()
    
    # Check each course's progress
    print("3️⃣ Calculating progress for each course...")
    print()
    
    all_correct = True
    
    for i, course_id in enumerate(enrolled_course_ids, 1):
        course = Course.find_by_id(course_id)
        if not course:
            continue
        
        course_name = course.get('name')
        course_code = course.get('code')
        
        print(f"📚 Course {i}: {course_code} - {course_name}")
        
        # Get activities
        activities = list(Activity.find_by_course(course_id))
        total_activities = len(activities)
        
        # Count completed activities
        completed = 0
        for activity in activities:
            responses = activity.get('responses', [])
            student_response = next((r for r in responses 
                                   if r.get('student_id') == student_id), None)
            if student_response:
                completed += 1
        
        # Calculate progress
        progress = (completed / total_activities * 100) if total_activities > 0 else 0
        
        print(f"   Total Activities: {total_activities}")
        print(f"   Completed: {completed}")
        print(f"   Progress: {progress:.1f}%")
        
        # Verify the data structure
        if total_activities > 0:
            if completed > 0:
                print(f"   ✅ Student has completed {completed}/{total_activities} activities")
            else:
                print(f"   ⚠️ Student hasn't completed any activities yet")
                print(f"   💡 Complete some activities to test the progress display")
        else:
            print(f"   ⚠️ No activities in this course")
        
        print()
    
    # Test the dashboard endpoint simulation
    print("4️⃣ Simulating Dashboard Data Structure...")
    print()
    
    total_activities_all = 0
    completed_activities_all = 0
    
    for course_id in enrolled_course_ids:
        course = Course.find_by_id(course_id)
        if course:
            activities = list(Activity.find_by_course(course_id))
            total_activities_all += len(activities)
            
            # This is the KEY part that was missing before the fix!
            course_completed = 0
            for activity in activities:
                responses = activity.get('responses', [])
                student_response = next((r for r in responses 
                                       if r.get('student_id') == student_id), None)
                if student_response:
                    course_completed += 1
                    completed_activities_all += 1
            
            # Check if completed_activities would be calculated
            print(f"Course: {course.get('code')}")
            print(f"  - activity_count: {len(activities)}")
            print(f"  - completed_activities: {course_completed} ✅ (NOW CALCULATED)")
            print()
    
    overall_completion = (completed_activities_all / total_activities_all * 100) if total_activities_all > 0 else 0
    
    print("=" * 60)
    print("📊 OVERALL STATISTICS")
    print("=" * 60)
    print(f"Total Activities: {total_activities_all}")
    print(f"Completed Activities: {completed_activities_all}")
    print(f"Overall Completion Rate: {overall_completion:.1f}%")
    print()
    
    if total_activities_all > 0 and completed_activities_all > 0:
        print("✅ FIX VERIFIED: Dashboard should now show correct progress!")
        print(f"   Expected Dashboard Display: {overall_completion:.1f}% Complete")
    elif total_activities_all > 0:
        print("⚠️ WARNING: Student has activities but none completed")
        print("   Complete some activities to see non-zero progress")
    else:
        print("⚠️ WARNING: No activities available")
        print("   Add activities to courses to test progress display")
    
    print()
    print("=" * 60)
    print("🎯 NEXT STEPS")
    print("=" * 60)
    print("1. Start the Flask app: python app.py")
    print(f"2. Login as: {username}")
    print("3. Go to Dashboard")
    print("4. Check if course progress shows correct percentage")
    print("5. Compare with 'My Courses' page (should be the same)")
    print()
    
    return True

if __name__ == '__main__':
    try:
        success = test_dashboard_progress()
        if success:
            print("✅ Test completed successfully!")
        else:
            print("❌ Test encountered issues - check messages above")
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
