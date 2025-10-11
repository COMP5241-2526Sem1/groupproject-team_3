"""
Student Routes Module
Handles student-specific routes and functionality
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
from models.user import User
from models.course import Course
from models.activity import Activity
from models.student import Student
from bson import ObjectId
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
student_bp = Blueprint('student', __name__, url_prefix='/student')

def student_required(f):
    """Decorator to ensure user is logged in as student"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        if session.get('role') != 'student':
            return render_template('error.html', 
                message='Access denied. Students only.'), 403
        return f(*args, **kwargs)
    return decorated_function

@student_bp.route('/dashboard')
@student_required
def dashboard():
    """
    Student dashboard
    Shows enrolled courses and available activities
    """
    try:
        user_id = session.get('user_id')
        user = User.find_by_id(user_id)
        
        if not user:
            return redirect(url_for('auth.login'))
        
        # Get enrolled courses
        enrolled_course_ids = user.get('enrolled_courses', [])
        enrolled_courses = []
        
        for course_id in enrolled_course_ids:
            course = Course.find_by_id(course_id)
            if course:
                # Get activities for this course
                activities = Activity.find_by_course(course_id)
                course['activities'] = list(activities)
                course['activity_count'] = len(course['activities'])
                enrolled_courses.append(course)
        
        # Get all available courses for enrollment
        all_courses = list(Course.get_all())
        available_courses = [c for c in all_courses 
                           if str(c['_id']) not in enrolled_course_ids]
        
        # Get student's submission statistics
        total_submissions = 0
        for course in enrolled_courses:
            for activity in course.get('activities', []):
                responses = activity.get('responses', [])
                # Count responses from this student
                student_responses = [r for r in responses 
                                   if r.get('student_id') == user.get('student_id') or
                                      r.get('student_name') == user.get('username')]
                total_submissions += len(student_responses)
        
        return render_template('student/dashboard.html',
            user=user,
            enrolled_courses=enrolled_courses,
            available_courses=available_courses,
            total_submissions=total_submissions
        )
        
    except Exception as e:
        logger.error(f"Error in student dashboard: {e}")
        return render_template('error.html', 
            message='Failed to load dashboard'), 500

@student_bp.route('/course/<course_id>')
@student_required
def course_detail(course_id):
    """
    View course details and activities
    """
    try:
        user_id = session.get('user_id')
        user = User.find_by_id(user_id)
        course = Course.find_by_id(course_id)
        
        if not course:
            return render_template('error.html', 
                message='Course not found'), 404
        
        # Check if student is enrolled
        enrolled_course_ids = user.get('enrolled_courses', [])
        is_enrolled = str(course_id) in enrolled_course_ids
        
        if not is_enrolled:
            return render_template('error.html', 
                message='You are not enrolled in this course'), 403
        
        # Get activities
        activities = list(Activity.find_by_course(course_id))
        
        # Get student's responses for each activity
        student_id = user.get('student_id')
        username = user.get('username')
        
        for activity in activities:
            responses = activity.get('responses', [])
            # Find student's response
            student_response = next((r for r in responses 
                                   if r.get('student_id') == student_id or
                                      r.get('student_name') == username), None)
            activity['student_response'] = student_response
            activity['has_responded'] = student_response is not None
        
        # Get teacher info
        teacher = User.find_by_id(course.get('teacher_id'))
        
        return render_template('student/course_detail.html',
            user=user,
            course=course,
            activities=activities,
            teacher=teacher
        )
        
    except Exception as e:
        logger.error(f"Error in course detail: {e}")
        return render_template('error.html', 
            message='Failed to load course'), 500

@student_bp.route('/enroll/<course_id>', methods=['POST'])
@student_required
def enroll_course(course_id):
    """
    Enroll in a course
    """
    try:
        user_id = session.get('user_id')
        user = User.find_by_id(user_id)
        course = Course.find_by_id(course_id)
        
        if not course:
            return jsonify({
                'success': False,
                'message': 'Course not found'
            }), 404
        
        # Check if already enrolled
        enrolled_course_ids = user.get('enrolled_courses', [])
        if str(course_id) in enrolled_course_ids:
            return jsonify({
                'success': False,
                'message': 'Already enrolled in this course'
            })
        
        # Enroll student
        success = User.enroll_course(user_id, course_id)
        
        if success:
            # Also add to course's students list if using Student model
            student_data = {
                'student_id': user.get('student_id'),
                'name': user.get('username'),
                'email': user.get('email'),
                'course_id': str(course_id)
            }
            Student.create(student_data)
            
            logger.info(f"Student {user.get('username')} enrolled in course {course_id}")
            
            return jsonify({
                'success': True,
                'message': 'Successfully enrolled in course'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to enroll'
            })
        
    except Exception as e:
        logger.error(f"Error enrolling in course: {e}")
        return jsonify({
            'success': False,
            'message': 'An error occurred'
        }), 500

@student_bp.route('/unenroll/<course_id>', methods=['POST'])
@student_required
def unenroll_course(course_id):
    """
    Unenroll from a course
    """
    try:
        user_id = session.get('user_id')
        
        success = User.unenroll_course(user_id, course_id)
        
        if success:
            logger.info(f"Student {user_id} unenrolled from course {course_id}")
            
            return jsonify({
                'success': True,
                'message': 'Successfully unenrolled from course'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to unenroll'
            })
        
    except Exception as e:
        logger.error(f"Error unenrolling from course: {e}")
        return jsonify({
            'success': False,
            'message': 'An error occurred'
        }), 500

@student_bp.route('/activity/<activity_id>')
@student_required
def view_activity(activity_id):
    """
    View activity and submit response
    """
    try:
        user_id = session.get('user_id')
        user = User.find_by_id(user_id)
        activity = Activity.find_by_id(activity_id)
        
        if not activity:
            return render_template('error.html', 
                message='Activity not found'), 404
        
        course = Course.find_by_id(activity.get('course_id'))
        
        # Check if student is enrolled in the course
        enrolled_course_ids = user.get('enrolled_courses', [])
        if str(activity.get('course_id')) not in enrolled_course_ids:
            return render_template('error.html', 
                message='You must be enrolled in the course to access this activity'), 403
        
        # Check if student has already responded
        student_id = user.get('student_id')
        username = user.get('username')
        responses = activity.get('responses', [])
        student_response = next((r for r in responses 
                               if r.get('student_id') == student_id or
                                  r.get('student_name') == username), None)
        
        return render_template('student/activity.html',
            user=user,
            activity=activity,
            course=course,
            student_response=student_response,
            has_responded=student_response is not None
        )
        
    except Exception as e:
        logger.error(f"Error viewing activity: {e}")
        return render_template('error.html', 
            message='Failed to load activity'), 500

@student_bp.route('/my-responses')
@student_required
def my_responses():
    """
    View all student's responses
    """
    try:
        user_id = session.get('user_id')
        user = User.find_by_id(user_id)
        student_id = user.get('student_id')
        username = user.get('username')
        
        # Get all enrolled courses
        enrolled_course_ids = user.get('enrolled_courses', [])
        
        all_responses = []
        
        for course_id in enrolled_course_ids:
            course = Course.find_by_id(course_id)
            if not course:
                continue
                
            activities = Activity.find_by_course(course_id)
            
            for activity in activities:
                responses = activity.get('responses', [])
                # Find student's response
                student_response = next((r for r in responses 
                                       if r.get('student_id') == student_id or
                                          r.get('student_name') == username), None)
                
                if student_response:
                    all_responses.append({
                        'activity': activity,
                        'course': course,
                        'response': student_response,
                        'submitted_at': student_response.get('timestamp')
                    })
        
        # Sort by submission time
        all_responses.sort(key=lambda x: x.get('submitted_at', ''), reverse=True)
        
        return render_template('student/my_responses.html',
            user=user,
            responses=all_responses
        )
        
    except Exception as e:
        logger.error(f"Error loading responses: {e}")
        return render_template('error.html', 
            message='Failed to load responses'), 500
