"""
Admin Routes Module
Handles administrative dashboard and system statistics
"""

from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from models.user import User
from models.course import Course
from models.activity import Activity
from models.student import Student
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to require admin role"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Not authenticated'}), 401
            return redirect(url_for('auth.login'))
        
        if session.get('role') != 'admin':
            if request.is_json:
                return jsonify({'success': False, 'message': 'Admin access required'}), 403
            return "Access Denied - Admin Only", 403
        
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin')
@admin_required
def admin_dashboard():
    """
    Admin dashboard
    Shows system statistics and overview
    """
    try:
        # Get statistics
        stats = {
            'total_teachers': User.count_teachers(),
            'total_activities': Activity.count_all(),
            'total_students': Student.count_by_course(None) if hasattr(Student, 'count_by_course') else 0
        }
        
        # Get activity type breakdown
        stats['poll_count'] = Activity.count_by_type(Activity.TYPE_POLL)
        stats['short_answer_count'] = Activity.count_by_type(Activity.TYPE_SHORT_ANSWER)
        stats['word_cloud_count'] = Activity.count_by_type(Activity.TYPE_WORD_CLOUD)
        
        # Get recent teachers
        recent_teachers = User.get_all_teachers()
        for teacher in recent_teachers:
            teacher['_id'] = str(teacher['_id'])
            # Get teacher's course count
            teacher['course_count'] = len(Course.find_by_teacher(teacher['_id']))
        
        # Sort by created_at and limit to 10
        recent_teachers.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        recent_teachers = recent_teachers[:10]
        
        return render_template(
            'admin.html',
            stats=stats,
            recent_teachers=recent_teachers,
            username=session.get('username')
        )
        
    except Exception as e:
        logger.error(f"Admin dashboard error: {e}")
        return "Error loading admin dashboard", 500

@admin_bp.route('/admin/stats')
@admin_required
def get_stats():
    """
    Get system statistics
    API endpoint for AJAX requests
    """
    try:
        stats = {
            'total_teachers': User.count_teachers(),
            'total_activities': Activity.count_all(),
            'poll_count': Activity.count_by_type(Activity.TYPE_POLL),
            'short_answer_count': Activity.count_by_type(Activity.TYPE_SHORT_ANSWER),
            'word_cloud_count': Activity.count_by_type(Activity.TYPE_WORD_CLOUD)
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
        
    except Exception as e:
        logger.error(f"Get stats error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to fetch statistics'
        }), 500

@admin_bp.route('/admin/teachers')
@admin_required
def get_teachers():
    """
    Get list of all teachers
    API endpoint for admin management
    """
    try:
        teachers = User.get_all_teachers()
        
        # Add course count for each teacher
        for teacher in teachers:
            teacher['_id'] = str(teacher['_id'])
            teacher['course_count'] = len(Course.find_by_teacher(teacher['_id']))
            # Remove password field
            if 'password' in teacher:
                del teacher['password']
        
        return jsonify({
            'success': True,
            'teachers': teachers
        }), 200
        
    except Exception as e:
        logger.error(f"Get teachers error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to fetch teachers'
        }), 500

@admin_bp.route('/admin/activities')
@admin_required
def get_all_activities():
    """
    Get list of all activities
    API endpoint for admin management
    """
    try:
        # Get all activities (not filtered by teacher)
        from services.db_service import db_service
        activities = db_service.find_many(
            Activity.COLLECTION_NAME,
            {'active': True},
            sort=[('created_at', -1)],
            limit=100
        )
        
        # Add teacher and course info
        for activity in activities:
            activity['_id'] = str(activity['_id'])
            activity['response_count'] = len(activity.get('responses', []))
            
            # Get teacher info
            teacher = User.find_by_id(activity['teacher_id'])
            activity['teacher_name'] = teacher['username'] if teacher else 'Unknown'
            
            # Get course info
            course = Course.find_by_id(activity['course_id'])
            activity['course_name'] = course['name'] if course else 'Unknown'
        
        return jsonify({
            'success': True,
            'activities': activities
        }), 200
        
    except Exception as e:
        logger.error(f"Get all activities error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to fetch activities'
        }), 500

# User Management Routes
@admin_bp.route('/admin/users')
@admin_required
def users_page():
    """User management page"""
    return render_template('admin_users.html', username=session.get('username'))

@admin_bp.route('/admin/api/users')
@admin_required
def get_all_users():
    """Get all users (teachers, students, admins)"""
    try:
        from services.db_service import db_service
        users = list(db_service.find_many(User.COLLECTION_NAME, {}, limit=500))
        
        for user in users:
            user['_id'] = str(user['_id'])
            if 'password' in user:
                del user['password']
            
            # Add additional stats
            if user['role'] == 'teacher':
                courses = Course.find_by_teacher(user['_id'])
                user['course_count'] = len(courses)
            elif user['role'] == 'student':
                user['enrolled_count'] = len(user.get('enrolled_courses', []))
        
        return jsonify({'success': True, 'users': users}), 200
    except Exception as e:
        logger.error(f"Get all users error: {e}")
        return jsonify({'success': False, 'message': 'Failed to fetch users'}), 500

@admin_bp.route('/admin/api/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
@admin_required
def manage_user(user_id):
    """Get, update or delete a user"""
    try:
        if request.method == 'GET':
            user = User.find_by_id(user_id)
            if not user:
                return jsonify({'success': False, 'message': 'User not found'}), 404
            
            user['_id'] = str(user['_id'])
            if 'password' in user:
                del user['password']
            
            return jsonify({'success': True, 'user': user}), 200
        
        elif request.method == 'PUT':
            data = request.get_json()
            
            # Update user
            from services.db_service import db_service
            from bson import ObjectId
            
            update_data = {}
            if 'username' in data:
                update_data['username'] = data['username'].strip()
            if 'email' in data:
                update_data['email'] = data['email'].strip()
            if 'institution' in data:
                update_data['institution'] = data['institution'].strip()
            if 'role' in data and data['role'] in ['admin', 'teacher', 'student']:
                update_data['role'] = data['role']
            
            # If changing password
            if 'password' in data and data['password'].strip():
                update_data['password'] = User.hash_password(data['password'])
            
            result = db_service.update_one(
                User.COLLECTION_NAME,
                {'_id': ObjectId(user_id)},
                {'$set': update_data}
            )
            
            if result:
                logger.info(f"User {user_id} updated by admin")
                return jsonify({'success': True, 'message': 'User updated'}), 200
            else:
                return jsonify({'success': False, 'message': 'Update failed'}), 500
        
        elif request.method == 'DELETE':
            from services.db_service import db_service
            from bson import ObjectId
            
            # Don't allow deleting self
            if user_id == session.get('user_id'):
                return jsonify({'success': False, 'message': 'Cannot delete your own account'}), 400
            
            result = db_service.delete_one(User.COLLECTION_NAME, {'_id': ObjectId(user_id)})
            
            if result:
                logger.info(f"User {user_id} deleted by admin")
                return jsonify({'success': True, 'message': 'User deleted'}), 200
            else:
                return jsonify({'success': False, 'message': 'Delete failed'}), 500
    
    except Exception as e:
        logger.error(f"Manage user error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/admin/api/users/create', methods=['POST'])
@admin_required
def create_user():
    """Create a new user (admin, teacher, or student)"""
    try:
        data = request.get_json()
        
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        email = data.get('email', '').strip()
        role = data.get('role', 'teacher').strip()
        institution = data.get('institution', '').strip()
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password required'}), 400
        
        if role not in ['admin', 'teacher', 'student']:
            return jsonify({'success': False, 'message': 'Invalid role'}), 400
        
        # Check if username exists
        if User.find_by_username(username):
            return jsonify({'success': False, 'message': 'Username already exists'}), 400
        
        # Create user
        user_data = {
            'username': username,
            'password': User.hash_password(password),
            'email': email,
            'role': role,
            'institution': institution
        }
        
        if role == 'student':
            user_data['student_id'] = data.get('student_id', username)
            user_data['enrolled_courses'] = []
        
        from services.db_service import db_service
        user_id = db_service.insert_one(User.COLLECTION_NAME, user_data)
        
        if user_id:
            logger.info(f"New {role} created by admin: {username}")
            return jsonify({'success': True, 'message': f'{role.capitalize()} created successfully', 'user_id': str(user_id)}), 201
        else:
            return jsonify({'success': False, 'message': 'Failed to create user'}), 500
    
    except Exception as e:
        logger.error(f"Create user error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

# Activity Management Routes
@admin_bp.route('/admin/activities-manage')
@admin_required
def activities_page():
    """Activity management page"""
    return render_template('admin_activities.html', username=session.get('username'))

@admin_bp.route('/admin/api/activities')
@admin_required  
def get_activities_list():
    """Get all activities for admin management"""
    try:
        from services.db_service import db_service
        activities = list(db_service.find_many(
            Activity.COLLECTION_NAME,
            {},
            sort=[('created_at', -1)],
            limit=500
        ))
        
        for activity in activities:
            activity['_id'] = str(activity['_id'])
            activity['response_count'] = len(activity.get('responses', []))
            
            # Get teacher info
            teacher = User.find_by_id(activity['teacher_id'])
            activity['teacher_name'] = teacher['username'] if teacher else 'Unknown'
            
            # Get course info
            course = Course.find_by_id(activity['course_id'])
            activity['course_name'] = course['name'] if course else 'Unknown'
            activity['course_code'] = course['code'] if course else 'N/A'
        
        return jsonify({'success': True, 'activities': activities}), 200
    except Exception as e:
        logger.error(f"Get activities list error: {e}")
        return jsonify({'success': False, 'message': 'Failed to fetch activities'}), 500

@admin_bp.route('/admin/api/activities/<activity_id>', methods=['GET', 'DELETE'])
@admin_required
def manage_activity(activity_id):
    """Get or delete an activity"""
    try:
        if request.method == 'GET':
            activity = Activity.find_by_id(activity_id)
            if not activity:
                return jsonify({'success': False, 'message': 'Activity not found'}), 404
            
            activity['_id'] = str(activity['_id'])
            return jsonify({'success': True, 'activity': activity}), 200
        
        elif request.method == 'DELETE':
            success = Activity.delete(activity_id)
            
            if success:
                logger.info(f"Activity {activity_id} deleted by admin")
                return jsonify({'success': True, 'message': 'Activity deleted'}), 200
            else:
                return jsonify({'success': False, 'message': 'Delete failed'}), 500
    
    except Exception as e:
        logger.error(f"Manage activity error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/admin/courses')
@admin_required
def courses_page():
    """Admin courses management page"""
    return render_template('admin_courses.html')

@admin_bp.route('/admin/api/courses', methods=['GET'])
@admin_required
def get_courses():
    """Get all courses with statistics"""
    try:
        courses = Course.find_all()
        
        for course in courses:
            course['_id'] = str(course['_id'])
            
            # Get teacher info
            teacher = User.find_by_id(course['teacher_id'])
            if teacher:
                course['teacher_username'] = teacher['username']
                course['teacher_email'] = teacher['email']
            
            # Get student count
            students = Student.find_by_course(course['_id'])
            course['student_count'] = len(students) if students else 0
            
            # Get activity count
            activities = Activity.find_by_course(course['_id'])
            course['activity_count'] = len(activities) if activities else 0
        
        return jsonify({'success': True, 'courses': courses}), 200
    except Exception as e:
        logger.error(f"Get courses error: {e}")
        return jsonify({'success': False, 'message': 'Failed to fetch courses'}), 500

@admin_bp.route('/admin/api/courses/<course_id>', methods=['GET', 'PUT', 'DELETE'])
@admin_required
def manage_course(course_id):
    """Get, update or delete a course"""
    try:
        if request.method == 'GET':
            course = Course.find_by_id(course_id)
            if not course:
                return jsonify({'success': False, 'message': 'Course not found'}), 404
            
            course['_id'] = str(course['_id'])
            
            # Get teacher info
            teacher = User.find_by_id(course['teacher_id'])
            if teacher:
                course['teacher_username'] = teacher['username']
                course['teacher_email'] = teacher['email']
            
            # Get student count
            students = Student.find_by_course(course_id)
            course['student_count'] = len(students) if students else 0
            
            # Get activity count
            activities = Activity.find_by_course(course_id)
            course['activity_count'] = len(activities) if activities else 0
            
            return jsonify({'success': True, 'course': course}), 200
        
        elif request.method == 'PUT':
            data = request.get_json()
            
            # Validate required fields
            if not data.get('name') or not data.get('teacher_id'):
                return jsonify({'success': False, 'message': 'Name and teacher are required'}), 400
            
            # Verify teacher exists
            teacher = User.find_by_id(data['teacher_id'])
            if not teacher or teacher['role'] != 'teacher':
                return jsonify({'success': False, 'message': 'Invalid teacher'}), 400
            
            # Update course
            update_data = {
                'name': data['name'],
                'description': data.get('description', ''),
                'teacher_id': data['teacher_id']
            }
            
            success = Course.update(course_id, update_data)
            
            if success:
                logger.info(f"Course {course_id} updated by admin")
                return jsonify({'success': True, 'message': 'Course updated'}), 200
            else:
                return jsonify({'success': False, 'message': 'Update failed'}), 500
        
        elif request.method == 'DELETE':
            # Delete all activities in this course
            activities = Activity.find_by_course(course_id)
            if activities:
                for activity in activities:
                    Activity.delete(str(activity['_id']))
            
            # Delete all student enrollments
            students = Student.find_by_course(course_id)
            if students:
                for student in students:
                    Student.unenroll(str(student['_id']), course_id)
            
            # Delete course
            success = Course.delete(course_id)
            
            if success:
                logger.info(f"Course {course_id} and related data deleted by admin")
                return jsonify({'success': True, 'message': 'Course deleted'}), 200
            else:
                return jsonify({'success': False, 'message': 'Delete failed'}), 500
    
    except Exception as e:
        logger.error(f"Manage course error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
