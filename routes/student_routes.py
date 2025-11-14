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
from services.db_service import db_service
from bson import ObjectId
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
student_bp = Blueprint('student', __name__, url_prefix='/student')

def clean_mongodb_document(doc):
    """
    Clean MongoDB document to remove Undefined types and make it JSON serializable
    
    Args:
        doc: MongoDB document (dict or list)
        
    Returns:
        Cleaned document safe for JSON serialization
    """
    if doc is None:
        return None
    
    if isinstance(doc, dict):
        cleaned = {}
        for key, value in doc.items():
            # Skip any problematic types by trying to serialize
            try:
                import json
                json.dumps(value, default=str)
                # If successful, recursively clean
                if isinstance(value, (dict, list)):
                    cleaned[key] = clean_mongodb_document(value)
                else:
                    cleaned[key] = value
            except (TypeError, ValueError):
                # Skip fields that can't be serialized
                logger.warning(f"Skipping non-serializable field: {key}")
                continue
        return cleaned
    
    elif isinstance(doc, list):
        cleaned_list = []
        for item in doc:
            try:
                import json
                json.dumps(item, default=str)
                if isinstance(item, (dict, list)):
                    cleaned_list.append(clean_mongodb_document(item))
                else:
                    cleaned_list.append(item)
            except (TypeError, ValueError):
                # Skip items that can't be serialized
                continue
        return cleaned_list
    
    return doc

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
    Student dashboard - Overview of learning activities and progress
    """
    try:
        user_id = session.get('user_id')
        user = User.find_by_id(user_id)
        
        if not user:
            return redirect(url_for('auth.login'))
        
        # Get enrolled courses
        enrolled_course_ids = user.get('enrolled_courses', [])
        enrolled_courses = []
        
        # Get recent activities across all enrolled courses
        recent_activities = []
        total_activities = 0
        completed_activities = 0
        
        for course_id in enrolled_course_ids:
            course = Course.find_by_id(course_id)
            if course:
                # Get activities for this course
                activities = list(Activity.find_by_course(course_id))
                total_activities += len(activities)
                
                # Count completed activities for this specific course
                course_completed = 0
                
                # Get recent activities with course info
                for activity in activities:
                    # Check if student has completed this activity
                    responses = activity.get('responses', [])
                    student_response = next((r for r in responses 
                                           if r.get('student_id') == user.get('student_id')), None)
                    is_completed = student_response is not None
                    
                    # Check if activity is expired
                    is_expired = Activity.is_expired(activity)
                    
                    # Convert deadline to HK time for display
                    if activity.get('deadline'):
                        utc_deadline = activity['deadline']
                        hk_deadline = utc_deadline + timedelta(hours=8)
                        activity['deadline_display'] = hk_deadline
                    
                    if is_completed:
                        course_completed += 1
                        completed_activities += 1
                    
                    # Add to recent activities list (only first 3 per course)
                    if len([a for a in recent_activities if a.get('course_code') == course.get('code')]) < 3:
                        activity['course_name'] = course.get('name')
                        activity['course_code'] = course.get('code')
                        activity['completed'] = is_completed
                        activity['is_expired'] = is_expired
                        recent_activities.append(activity)
                
                course['activity_count'] = len(activities)
                course['completed_activities'] = course_completed
                enrolled_courses.append(course)
        
        # Sort recent activities by date
        recent_activities.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        recent_activities = recent_activities[:5]  # Show top 5 recent activities
        
        # Calculate completion rate
        completion_rate = (completed_activities / total_activities * 100) if total_activities > 0 else 0
        
        # Get total submissions count
        total_submissions = completed_activities
        
        return render_template('student/dashboard.html',
            user=user,
            enrolled_courses=enrolled_courses,
            recent_activities=recent_activities,
            total_activities=total_activities,
            completed_activities=completed_activities,
            completion_rate=round(completion_rate, 1),
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
            
            # Check if activity is expired and convert deadline to HK time
            activity['is_expired'] = Activity.is_expired(activity)
            if activity.get('deadline'):
                utc_deadline = activity['deadline']
                hk_deadline = utc_deadline + timedelta(hours=8)
                activity['deadline_display'] = hk_deadline
        
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
        
        # Check if activity has expired
        is_expired = Activity.is_expired(activity)
        
        # Convert deadline from UTC to Hong Kong time (UTC+8) for display
        if activity.get('deadline'):
            from datetime import timedelta
            utc_deadline = activity['deadline']
            hk_deadline = utc_deadline + timedelta(hours=8)
            activity['deadline_display'] = hk_deadline
        
        # Clean all documents FIRST before processing
        activity = clean_mongodb_document(activity)
        course = clean_mongodb_document(course)
        user = clean_mongodb_document(user)
        
        # Check if student has already responded (use cleaned activity)
        student_id = user.get('student_id')
        username = user.get('username')
        responses = activity.get('responses', [])
        student_response = next((r for r in responses 
                               if r.get('student_id') == student_id or
                                  r.get('student_name') == username), None)
        
        # Log response info
        if student_response:
            logger.info(f"Student response found for activity {activity_id}")
            if student_response and 'ai_evaluation' in student_response:
                ai_eval = student_response.get('ai_evaluation')
                logger.info(f"AI evaluation type: {type(ai_eval)}, keys: {ai_eval.keys() if isinstance(ai_eval, dict) else 'N/A'}")
        
        return render_template('student/activity.html',
            user=user,
            activity=activity,
            course=course,
            student_response=student_response,
            has_responded=student_response is not None,
            is_expired=is_expired
        )
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"Error viewing activity: {e}")
        logger.error(f"Traceback: {error_details}")
        return render_template('error.html', 
            message=f'Failed to load activity: {str(e)}'), 500

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
                        'submitted_at': student_response.get('submitted_at')
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

@student_bp.route('/my-courses')
@student_required
def my_courses():
    """
    View all enrolled courses
    """
    try:
        user_id = session.get('user_id')
        user = User.find_by_id(user_id)
        
        enrolled_course_ids = user.get('enrolled_courses', [])
        enrolled_courses = []
        
        for course_id in enrolled_course_ids:
            course = Course.find_by_id(course_id)
            if course:
                # Get statistics
                activities = list(Activity.find_by_course(course_id))
                total_activities = len(activities)
                
                # Count completed activities
                completed = 0
                for activity in activities:
                    responses = activity.get('responses', [])
                    if any(r.get('student_id') == user.get('student_id') for r in responses):
                        completed += 1
                
                course['total_activities'] = total_activities
                course['completed_activities'] = completed
                course['completion_rate'] = (completed / total_activities * 100) if total_activities > 0 else 0
                enrolled_courses.append(course)
        
        return render_template('student/my_courses.html',
            user=user,
            courses=enrolled_courses
        )
        
    except Exception as e:
        logger.error(f"Error loading my courses: {e}")
        return render_template('error.html', message='Failed to load courses'), 500

@student_bp.route('/browse-courses')
@student_required
def browse_courses():
    """
    Browse and enroll in available courses
    """
    try:
        user_id = session.get('user_id')
        user = User.find_by_id(user_id)
        
        # Get all courses
        all_courses = list(Course.get_all())
        enrolled_course_ids = [str(cid) for cid in user.get('enrolled_courses', [])]
        
        # Separate enrolled and available courses
        available_courses = []
        for course in all_courses:
            course_id_str = str(course['_id'])
            if course_id_str not in enrolled_course_ids:
                # Get course statistics
                activities = list(Activity.find_by_course(course_id_str))
                course['activity_count'] = len(activities)
                
                # Get teacher info
                teacher = User.find_by_id(course.get('teacher_id'))
                course['teacher_name'] = teacher.get('username') if teacher else 'Unknown'
                
                available_courses.append(course)
        
        return render_template('student/browse_courses.html',
            user=user,
            courses=available_courses
        )
        
    except Exception as e:
        logger.error(f"Error browsing courses: {e}")
        return render_template('error.html', message='Failed to load courses'), 500

@student_bp.route('/my-activities')
@student_required
def my_activities():
    """
    View all activities from enrolled courses
    """
    try:
        user_id = session.get('user_id')
        user = User.find_by_id(user_id)
        
        enrolled_course_ids = user.get('enrolled_courses', [])
        all_activities = []
        
        for course_id in enrolled_course_ids:
            course = Course.find_by_id(course_id)
            if not course:
                continue
            
            activities = list(Activity.find_by_course(course_id))
            
            for activity in activities:
                # Check if completed
                responses = activity.get('responses', [])
                student_response = next((r for r in responses 
                                       if r.get('student_id') == user.get('student_id')), None)
                
                # Check if expired and convert deadline to HK time
                is_expired = Activity.is_expired(activity)
                if activity.get('deadline'):
                    utc_deadline = activity['deadline']
                    hk_deadline = utc_deadline + timedelta(hours=8)
                    activity['deadline_display'] = hk_deadline
                
                activity['course_name'] = course.get('name')
                activity['course_code'] = course.get('code')
                activity['completed'] = student_response is not None
                activity['is_expired'] = is_expired
                activity['response_count'] = len(responses)
                all_activities.append(activity)
        
        # Sort by date
        all_activities.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return render_template('student/my_activities.html',
            user=user,
            activities=all_activities
        )
        
    except Exception as e:
        logger.error(f"Error loading activities: {e}")
        return render_template('error.html', message='Failed to load activities'), 500

@student_bp.route('/leaderboard')
@student_required
def leaderboard():
    """
    View leaderboard with rankings and points
    """
    try:
        user_id = session.get('user_id')
        user = User.find_by_id(user_id)
        
        if not user:
            return render_template('error.html', message='User not found'), 404
        
        # Get student information - use user.get() for consistency with other routes
        student_id = user.get('student_id')
        username = user.get('username', 'Anonymous')
        
        # Also try username as identifier if student_id doesn't exist
        student_identifier = student_id if student_id else username
        
        logger.info(f"Leaderboard: user_id={user_id}, student_id={student_id}, username={username}")
        
        # Import points service
        from services.points_service import PointsService
        
        # Get enrolled courses from user's enrolled_courses array
        course_ids = user.get('enrolled_courses', [])
        logger.info(f"Found {len(course_ids)} enrolled courses: {course_ids}")
        
        # Get leaderboards for each course
        course_leaderboards = []
        my_course_ranks = []
        
        for course_id in course_ids:
            try:
                course = Course.find_by_id(course_id)
                if course:
                    leaderboard_data = PointsService.get_course_leaderboard(course_id, limit=10)
                    
                    # Find current student's rank - use student_identifier
                    my_rank = PointsService.get_student_rank(student_identifier, course_id)
                    
                    logger.info(f"Course {course.get('name')}: {len(leaderboard_data)} students, my rank: {my_rank}")
                    
                    course_leaderboards.append({
                        'course': course,
                        'leaderboard': leaderboard_data,
                        'my_rank': my_rank
                    })
                    
                    my_course_ranks.append({
                        'course_name': course.get('name', 'Unknown Course'),
                        'rank': my_rank.get('rank'),
                        'total': my_rank.get('total_students', 0),
                        'points': my_rank.get('points', 0)
                    })
            except Exception as course_error:
                logger.error(f"Error processing course {course_id}: {course_error}")
                continue
        
        # Get global leaderboard
        try:
            global_leaderboard = PointsService.get_global_leaderboard(limit=50)
            logger.info(f"Global leaderboard: {len(global_leaderboard)} students")
        except Exception as e:
            logger.error(f"Error getting global leaderboard: {e}")
            global_leaderboard = []
        
        # Calculate student's overall points and achievements - use student_identifier
        try:
            overall_points = PointsService.calculate_student_points(student_identifier)
            logger.info(f"Overall points for {student_identifier}: {overall_points}")
        except Exception as e:
            logger.error(f"Error calculating points: {e}")
            overall_points = {
                'poll_responses': 0,
                'short_answer_responses': 0,
                'word_cloud_responses': 0,
                'correct_answers': 0,
                'early_submissions': 0,
                'feedback_received': 0,
                'total': 0
            }
        
        try:
            achievements = PointsService.get_achievements(student_identifier)
        except Exception as e:
            logger.error(f"Error getting achievements: {e}")
            achievements = []
        
        # Find student's global rank and points - use student_identifier
        my_global_rank = None
        global_my_points = 0
        try:
            for i, entry in enumerate(global_leaderboard):
                if entry.get('student_id') == student_identifier:
                    my_global_rank = i + 1
                    global_my_points = entry.get('points', 0)
                    break
        except Exception as e:
            logger.error(f"Error finding global rank: {e}")
        
        return render_template('student/leaderboard.html',
            user=user,
            student_id=student_identifier,
            course_leaderboards=course_leaderboards,
            global_leaderboard=global_leaderboard,
            my_course_ranks=my_course_ranks,
            my_global_rank=my_global_rank,
            global_my_points=global_my_points,
            overall_points=overall_points,
            achievements=achievements
        )
        
    except Exception as e:
        logger.error(f"Error loading leaderboard: {e}")
        import traceback
        traceback.print_exc()
        return render_template('error.html', message=f'Failed to load leaderboard: {str(e)}'), 500

@student_bp.route('/profile')
@student_required
def profile():
    """
    View and edit student profile
    """
    try:
        user_id = session.get('user_id')
        user = User.find_by_id(user_id)
        
        if not user:
            return render_template('error.html', message='User not found'), 404
        
        # Get student stats
        student_id = user.get('student_id', user.get('username'))
        
        from services.points_service import PointsService
        overall_points = PointsService.calculate_student_points(student_id)
        achievements = PointsService.get_achievements(student_id)
        activities_count = PointsService.count_student_activities(student_id)
        
        # Get enrolled courses count
        enrollments = db_service.find_many('enrollments', {'student_id': student_id})
        
        return render_template('student/profile.html',
            user=user,
            overall_points=overall_points,
            achievements=achievements,
            activities_count=activities_count,
            courses_count=len(enrollments)
        )
        
    except Exception as e:
        logger.error(f"Error loading profile: {e}")
        return render_template('error.html', message='Failed to load profile'), 500

@student_bp.route('/update-profile', methods=['POST'])
@student_required
def update_profile():
    """
    Update student profile information
    """
    try:
        user_id = session.get('user_id')
        data = request.get_json() if request.is_json else request.form
        
        # Update user information
        update_data = {}
        
        if data.get('email'):
            update_data['email'] = data.get('email').strip()
        
        if data.get('student_id'):
            update_data['student_id'] = data.get('student_id').strip()
        
        if update_data:
            from models.user import User
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
        logger.error(f"Update profile error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to update profile'
        }), 500
