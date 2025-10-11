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
