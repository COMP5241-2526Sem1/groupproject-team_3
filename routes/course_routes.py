"""
Course Routes Module
Handles course management and student import endpoints
"""

from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from models.course import Course
from models.student import Student
from models.activity import Activity
from bson import ObjectId
from datetime import datetime, timedelta
import csv
import io
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
course_bp = Blueprint('course', __name__)

def login_required(f):
    """Decorator to require login"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Not authenticated'}), 401
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@course_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Teacher dashboard
    Shows all courses and activities
    """
    teacher_id = session['user_id']
    
    # Get teacher's courses
    courses = Course.find_by_teacher(teacher_id)
    
    # Add student count and activity count to each course
    for course in courses:
        course['_id'] = str(course['_id'])
        course['student_count'] = Student.count_by_course(course['_id'])
        activities = Activity.find_by_course(course['_id'])
        course['activity_count'] = len(activities)
    
    return render_template('dashboard.html', courses=courses, username=session.get('username'))

@course_bp.route('/course/create', methods=['GET', 'POST'])
@login_required
def create_course():
    """
    Create new course
    GET: Show course creation form
    POST: Process course creation
    """
    if request.method == 'GET':
        return render_template('create_course.html')
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        # Validate required fields
        name = data.get('name', '').strip()
        code = data.get('code', '').strip()
        description = data.get('description', '').strip()
        
        if not name or not code:
            return jsonify({
                'success': False,
                'message': 'Course name and code are required'
            }), 400
        
        # Check if course code already exists
        existing_course = Course.find_by_code(code)
        if existing_course:
            return jsonify({
                'success': False,
                'message': 'Course code already exists'
            }), 400
        
        # Create course
        course = Course(
            name=name,
            code=code,
            teacher_id=session['user_id'],
            description=description
        )
        
        course_id = course.save()
        
        logger.info(f"Course created: {name} ({code}) by {session['username']}")
        
        return jsonify({
            'success': True,
            'message': 'Course created successfully',
            'course_id': course_id
        }), 201
        
    except Exception as e:
        logger.error(f"Create course error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to create course'
        }), 500

@course_bp.route('/course/<course_id>')
@login_required
def course_detail(course_id):
    """
    Course detail page
    Shows course info, students, and activities
    """
    try:
        course = Course.find_by_id(course_id)
        
        if not course:
            return "Course not found", 404
        
        # Check if user owns this course
        if course['teacher_id'] != session['user_id']:
            return "Access denied", 403
        
        course['_id'] = str(course['_id'])
        
        # Get students
        students = Student.find_by_course(course_id)
        for student in students:
            student['_id'] = str(student['_id'])
        
        # Get activities
        activities = Activity.find_by_course(course_id)
        for activity in activities:
            activity['_id'] = str(activity['_id'])
            activity['response_count'] = len(activity.get('responses', []))
            
            # Add deadline info for teacher (info only, doesn't restrict access)
            activity['is_expired'] = Activity.is_expired(activity)
            if activity.get('deadline'):
                utc_deadline = activity['deadline']
                hk_deadline = utc_deadline + timedelta(hours=8)
                activity['deadline_display'] = hk_deadline
        
        return render_template(
            'course_detail.html',
            course=course,
            students=students,
            activities=activities
        )
        
    except Exception as e:
        logger.error(f"Course detail error: {e}")
        return "Error loading course", 500

@course_bp.route('/course/<course_id>/import-students', methods=['POST'])
@login_required
def import_students(course_id):
    """
    Import students to course
    Supports manual input and CSV file upload
    """
    try:
        # Verify course ownership
        course = Course.find_by_id(course_id)
        if not course or course['teacher_id'] != session['user_id']:
            return jsonify({
                'success': False,
                'message': 'Course not found or access denied'
            }), 403
        
        students_added = 0
        
        # Check if CSV file uploaded
        if 'file' in request.files:
            file = request.files['file']
            
            if file.filename == '':
                return jsonify({
                    'success': False,
                    'message': 'No file selected'
                }), 400
            
            if not file.filename.endswith('.csv'):
                return jsonify({
                    'success': False,
                    'message': 'Only CSV files are allowed'
                }), 400
            
            # Read CSV file
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_reader = csv.DictReader(stream)
            
            students_to_insert = []
            
            for row in csv_reader:
                student_id = row.get('student_id', '').strip()
                name = row.get('name', '').strip()
                email = row.get('email', '').strip()
                
                if not student_id or not name:
                    continue
                
                # Check if student already exists in this course
                existing = Student.find_by_student_id(student_id, course_id)
                if existing:
                    continue
                
                student = Student(student_id, name, course_id, email)
                students_to_insert.append(student.to_dict())
            
            if students_to_insert:
                students_added = Student.bulk_insert(students_to_insert)
                logger.info(f"Imported {students_added} students via CSV to course {course_id}")
        
        # Check for manual input
        else:
            data = request.get_json() if request.is_json else request.form
            student_id = data.get('student_id', '').strip()
            name = data.get('name', '').strip()
            email = data.get('email', '').strip()
            
            if not student_id or not name:
                return jsonify({
                    'success': False,
                    'message': 'Student ID and name are required'
                }), 400
            
            # Check if student already exists
            existing = Student.find_by_student_id(student_id, course_id)
            if existing:
                return jsonify({
                    'success': False,
                    'message': 'Student already exists in this course'
                }), 400
            
            # Create student
            student = Student(student_id, name, course_id, email)
            student.save()
            students_added = 1
            
            logger.info(f"Added student {name} ({student_id}) to course {course_id}")
        
        return jsonify({
            'success': True,
            'message': f'{students_added} student(s) added successfully',
            'count': students_added
        }), 201
        
    except Exception as e:
        logger.error(f"Import students error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to import students'
        }), 500

@course_bp.route('/course/<course_id>/students')
@login_required
def get_students(course_id):
    """
    Get list of students in course
    API endpoint for AJAX requests
    """
    try:
        # Verify course ownership
        course = Course.find_by_id(course_id)
        if not course or course['teacher_id'] != session['user_id']:
            return jsonify({
                'success': False,
                'message': 'Course not found or access denied'
            }), 403
        
        students = Student.find_by_course(course_id)
        
        # Convert ObjectId to string
        for student in students:
            student['_id'] = str(student['_id'])
        
        return jsonify({
            'success': True,
            'students': students
        }), 200
        
    except Exception as e:
        logger.error(f"Get students error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to fetch students'
        }), 500

@course_bp.route('/course/<course_id>/update', methods=['PUT', 'POST'])
@login_required
def update_course(course_id):
    """
    Update course information
    """
    try:
        # Verify course ownership
        course = Course.find_by_id(course_id)
        if not course or course['teacher_id'] != session['user_id']:
            return jsonify({
                'success': False,
                'message': 'Course not found or access denied'
            }), 403
        
        data = request.get_json() if request.is_json else request.form
        
        # Prepare update data
        update_data = {}
        if 'name' in data and data['name'].strip():
            update_data['name'] = data['name'].strip()
        if 'description' in data:
            update_data['description'] = data['description'].strip()
        
        if not update_data:
            return jsonify({
                'success': False,
                'message': 'No data to update'
            }), 400
        
        # Update course
        success = Course.update_course(course_id, update_data)
        
        if success:
            logger.info(f"Course updated: {course_id}")
            return jsonify({
                'success': True,
                'message': 'Course updated successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'No changes made'
            }), 400
        
    except Exception as e:
        logger.error(f"Update course error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to update course'
        }), 500

@course_bp.route('/course/<course_id>/delete', methods=['DELETE', 'POST'])
@login_required
def delete_course(course_id):
    """
    Delete course (soft delete)
    """
    try:
        # Verify course ownership
        course = Course.find_by_id(course_id)
        if not course or course['teacher_id'] != session['user_id']:
            return jsonify({
                'success': False,
                'message': 'Course not found or access denied'
            }), 403
        
        # Soft delete course
        success = Course.delete_course(course_id)
        
        if success:
            logger.info(f"Course deleted: {course_id}")
            return jsonify({
                'success': True,
                'message': 'Course deleted successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to delete course'
            }), 400
        
    except Exception as e:
        logger.error(f"Delete course error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to delete course'
        }), 500

@course_bp.route('/profile')
@login_required
def teacher_profile():
    """
    View and edit teacher profile (settings page)
    """
    try:
        from models.user import User
        user_id = session.get('user_id')
        user = User.find_by_id(user_id)
        
        if not user:
            return render_template('error.html', message='User not found'), 404
        
        return render_template('teacher/profile.html', user=user)
        
    except Exception as e:
        logger.error(f"Error loading teacher profile: {e}")
        return render_template('error.html', message='Failed to load profile'), 500

@course_bp.route('/update-profile', methods=['POST'])
@login_required
def update_teacher_profile():
    """
    Update teacher profile information
    """
    try:
        from models.user import User
        user_id = session.get('user_id')
        data = request.get_json() if request.is_json else request.form
        
        # Update user information
        update_data = {}
        
        if data.get('email'):
            update_data['email'] = data.get('email').strip()
        
        if data.get('name'):
            update_data['name'] = data.get('name').strip()
        
        if update_data:
            User.update_user(user_id, update_data)
            
            return jsonify({
                'success': True,
                'message': 'Profile updated successfully'
            }), 200
        
        return jsonify({
            'success': False,
            'message': 'No data to update'
        }), 400
        
    except Exception as e:
        logger.error(f"Update teacher profile error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to update profile'
        }), 500
