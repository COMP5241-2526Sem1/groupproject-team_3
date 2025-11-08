"""
Activity Routes Module
Handles learning activity creation, management, and student participation
"""

from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from models.activity import Activity
from models.course import Course
from services.genai_service import genai_service
from bson import ObjectId
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
activity_bp = Blueprint('activity', __name__)

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

@activity_bp.route('/activity/create', methods=['GET', 'POST'])
@login_required
def create_activity():
    """
    Create learning activity
    GET: Show activity creation form
    POST: Process activity creation
    """
    if request.method == 'GET':
        # Get course list for dropdown
        courses = Course.find_by_teacher(session['user_id'])
        for course in courses:
            course['_id'] = str(course['_id'])
        return render_template('create_activity.html', courses=courses)
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        # Validate required fields
        title = data.get('title', '').strip()
        activity_type = data.get('type', '').strip()
        course_id = data.get('course_id', '').strip()
        
        if not all([title, activity_type, course_id]):
            return jsonify({
                'success': False,
                'message': 'Title, type, and course are required'
            }), 400
        
        # Verify course ownership
        course = Course.find_by_id(course_id)
        if not course or course['teacher_id'] != session['user_id']:
            return jsonify({
                'success': False,
                'message': 'Course not found or access denied'
            }), 403
        
        # Parse content based on activity type
        content = {}
        
        if activity_type == Activity.TYPE_POLL:
            # Check if this is AI-generated multi-question poll
            poll_questions = data.get('poll_questions')
            logger.info(f"Creating poll activity. poll_questions present: {poll_questions is not None}")
            
            if poll_questions:
                # Multi-question poll format (AI generated)
                logger.info(f"Multi-question poll with {len(poll_questions)} questions")
                content = {
                    'questions': poll_questions,
                    'allow_multiple': data.get('allow_multiple', False)
                }
                logger.info(f"Content structure: {content.keys()}")
            else:
                # Single question poll format (manual creation)
                logger.info("Single question poll (manual)")
                content = {
                    'question': data.get('question', '').strip(),
                    'options': data.get('options', []),
                    'allow_multiple': data.get('allow_multiple', False)
                }
                
                if not content['question'] or len(content['options']) < 2:
                    return jsonify({
                        'success': False,
                        'message': 'Poll must have a question and at least 2 options'
                    }), 400
        
        elif activity_type == Activity.TYPE_SHORT_ANSWER:
            content = {
                'question': data.get('question', '').strip(),
                'word_limit': int(data.get('word_limit', 200)),
                'key_points': data.get('key_points', [])
            }
            
            if not content['question']:
                return jsonify({
                    'success': False,
                    'message': 'Question is required'
                }), 400
        
        elif activity_type == Activity.TYPE_WORD_CLOUD:
            content = {
                'question': data.get('question', '').strip(),
                'instructions': data.get('instructions', 'Enter keywords related to the topic')
            }
            
            if not content['question']:
                return jsonify({
                    'success': False,
                    'message': 'Question is required'
                }), 400
        
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid activity type'
            }), 400
        
        # Create activity
        activity = Activity(
            title=title,
            activity_type=activity_type,
            content=content,
            course_id=course_id,
            teacher_id=session['user_id']
        )
        
        activity_id = activity.save()
        
        # Get the saved activity to get the link
        saved_activity = Activity.find_by_id(activity_id)
        
        logger.info(f"Activity created: {title} ({activity_type}) by {session['username']}")
        
        return jsonify({
            'success': True,
            'message': 'Activity created successfully',
            'activity_id': activity_id,
            'link': saved_activity['link']
        }), 201
        
    except Exception as e:
        logger.error(f"Create activity error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to create activity'
        }), 500

@activity_bp.route('/activity/ai-generate', methods=['POST'])
@login_required
def ai_generate_activity():
    """
    Generate activity using AI
    Uses GPT-4 to create activity based on teaching content
    """
    try:
        data = request.get_json() if request.is_json else request.form
        
        teaching_content = data.get('teaching_content', '').strip()
        activity_type = data.get('type', 'short_answer').strip()
        course_id = data.get('course_id', '').strip()
        num_questions = int(data.get('num_questions', 1))
        
        if not teaching_content:
            return jsonify({
                'success': False,
                'message': 'Teaching content is required'
            }), 400
        
        if not course_id:
            return jsonify({
                'success': False,
                'message': 'Course is required'
            }), 400
        
        # Verify course ownership
        course = Course.find_by_id(course_id)
        if not course or course['teacher_id'] != session['user_id']:
            return jsonify({
                'success': False,
                'message': 'Course not found or access denied'
            }), 403
        
        # Generate activity using AI
        logger.info(f"Generating AI activity for: {teaching_content} ({activity_type}, {num_questions} questions)")
        generated = genai_service.generate_activity(teaching_content, activity_type, num_questions)
        
        # Mark as AI generated
        generated['ai_generated'] = True
        
        logger.info(f"AI activity generated for {session['username']}")
        
        return jsonify({
            'success': True,
            'message': 'Activity generated successfully',
            'generated_content': generated
        }), 200
        
    except Exception as e:
        logger.error(f"AI generate activity error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to generate activity. Please try again.'
        }), 500

@activity_bp.route('/activity/<activity_id>')
@login_required
def activity_detail(activity_id):
    """
    Activity detail page for teachers
    Shows activity info and responses
    """
    try:
        print(f"\n{'='*60}")
        print(f"DEBUG: activity_detail called with ID: {activity_id}")
        print(f"DEBUG: Session user_id: {session.get('user_id')}")
        print(f"DEBUG: Session role: {session.get('role')}")
        print(f"{'='*60}\n")
        
        activity = Activity.find_by_id(activity_id)
        print(f"DEBUG: Activity found: {activity is not None}")
        
        if not activity:
            print("DEBUG: Returning 404 - Activity not found")
            return "Activity not found", 404
        
        print(f"DEBUG: Activity teacher_id: {activity.get('teacher_id')} (type: {type(activity.get('teacher_id'))})")
        print(f"DEBUG: Session user_id: {session.get('user_id')} (type: {type(session.get('user_id'))})")
        
        # Check if user owns this activity
        if str(activity.get('teacher_id')) != str(session.get('user_id')):
            print("DEBUG: Returning 403 - Access denied")
            return "Access denied", 403
        
        print("DEBUG: Ownership check passed")
        activity['_id'] = str(activity['_id'])
        
        # Get course info
        print(f"DEBUG: Getting course {activity.get('course_id')}")
        course = Course.find_by_id(activity['course_id'])
        print(f"DEBUG: Course found: {course is not None}")
        
        if not course:
            logger.warning(f"Course not found for activity {activity_id}: {activity.get('course_id')}")
            # Create a minimal course object to prevent template errors
            course = {
                'name': 'Unknown Course',
                'students': []
            }
            print("DEBUG: Using fallback course")
        else:
            print(f"DEBUG: Course name: {course.get('name')}")
        
        # Calculate response statistics
        responses = activity.get('responses', [])
        response_count = len(responses)
        print(f"DEBUG: {response_count} responses found")
        print(f"DEBUG: Activity type: {activity.get('type')}")
        
        # Get enrolled student count from students collection (more reliable than course.students)
        from models.student import Student
        enrolled_students = list(Student.find_by_course(activity['course_id']))
        enrolled_count = len(enrolled_students)
        print(f"DEBUG: {enrolled_count} students enrolled in course")
        
        # Calculate participation rate
        participation_rate = None
        if enrolled_count > 0:
            participation_rate = round((response_count / enrolled_count) * 100)
        print(f"DEBUG: Participation rate: {participation_rate}%")
        
        # Get grouped answers if short answer type
        grouped_answers = None
        if activity['type'] == Activity.TYPE_SHORT_ANSWER and responses:
            print("DEBUG: Processing short answer grouping...")
            # Check if already grouped
            if 'grouped_answers' not in activity:
                print("DEBUG: Calling AI to group answers...")
                # Group answers using AI
                grouped_answers = genai_service.group_answers(responses, activity['content']['question'])
                # Save grouped answers
                Activity.update_activity(activity_id, {'grouped_answers': grouped_answers})
                print("DEBUG: Grouped answers saved")
            else:
                grouped_answers = activity['grouped_answers']
                print("DEBUG: Using cached grouped answers")
        
        print("DEBUG: Rendering template...")
        return render_template(
            'activity_detail.html',
            activity=activity,
            course=course,
            response_count=response_count,
            enrolled_count=enrolled_count,
            participation_rate=participation_rate,
            grouped_answers=grouped_answers
        )
        
    except Exception as e:
        print(f"\n{'!'*60}")
        print(f"ERROR in activity_detail: {type(e).__name__}: {e}")
        print(f"{'!'*60}\n")
        logger.error(f"Activity detail error: {e}")
        import traceback
        traceback.print_exc()
        return "Error loading activity", 500

@activity_bp.route('/a/<link>')
def student_activity(link):
    """
    Student activity participation page
    No login required - accessible via unique link
    """
    try:
        activity = Activity.find_by_link(link)
        
        if not activity:
            return "Activity not found", 404
        
        if not activity.get('active', True):
            return "This activity is no longer active", 410
        
        activity['_id'] = str(activity['_id'])
        
        # Debug logging
        logger.info(f"Student accessing activity: {activity.get('title')}")
        logger.info(f"Activity type: {activity.get('type')}")
        logger.info(f"Content keys: {activity.get('content', {}).keys()}")
        if activity.get('type') == 'poll':
            has_questions = 'questions' in activity.get('content', {})
            logger.info(f"Has 'questions' field: {has_questions}")
            if has_questions:
                logger.info(f"Number of questions: {len(activity['content']['questions'])}")
        
        # Get course info
        course = Course.find_by_id(activity['course_id'])
        
        return render_template(
            'student_activity.html',
            activity=activity,
            course=course
        )
        
    except Exception as e:
        logger.error(f"Student activity error: {e}")
        return "Error loading activity", 500

@activity_bp.route('/activity/<activity_id>/submit', methods=['POST'])
def submit_response(activity_id):
    """
    Submit student response to activity
    No authentication required
    """
    try:
        activity = Activity.find_by_id(activity_id)
        
        if not activity:
            return jsonify({
                'success': False,
                'message': 'Activity not found'
            }), 404
        
        if not activity.get('active', True):
            return jsonify({
                'success': False,
                'message': 'Activity is no longer active'
            }), 410
        
        data = request.get_json() if request.is_json else request.form
        
        # Prepare response data
        response_data = {
            'student_id': data.get('student_id', 'Anonymous'),
            'student_name': data.get('student_name', 'Anonymous')
        }
        
        # Parse response based on activity type
        if activity['type'] == Activity.TYPE_POLL:
            # Check if this is multi-question poll
            poll_questions = activity['content'].get('questions')
            
            if poll_questions:
                # Multi-question poll - evaluate answers
                student_answers = data.get('answers', {})  # {question_index: selected_option}
                
                if not student_answers:
                    return jsonify({
                        'success': False,
                        'message': 'Please answer all questions'
                    }), 400
                
                # Evaluate each answer
                results = []
                correct_count = 0
                
                for i, question in enumerate(poll_questions):
                    student_answer = student_answers.get(str(i))
                    correct_answer = question.get('correct_answer')
                    
                    is_correct = student_answer == correct_answer
                    if is_correct:
                        correct_count += 1
                    
                    results.append({
                        'question_index': i,
                        'student_answer': student_answer,
                        'correct_answer': correct_answer,
                        'is_correct': is_correct,
                        'explanation': question.get('explanation', '')
                    })
                
                response_data['answers'] = results
                response_data['score'] = correct_count
                response_data['total'] = len(poll_questions)
                response_data['percentage'] = round((correct_count / len(poll_questions)) * 100, 1)
            else:
                # Single question poll (original format)
                response_data['selected_options'] = data.get('selected_options', [])
                if not response_data['selected_options']:
                    return jsonify({
                        'success': False,
                        'message': 'Please select at least one option'
                    }), 400
        
        elif activity['type'] == Activity.TYPE_SHORT_ANSWER:
            response_data['text'] = data.get('text', '').strip()
            if not response_data['text']:
                return jsonify({
                    'success': False,
                    'message': 'Please enter your answer'
                }), 400
        
        elif activity['type'] == Activity.TYPE_WORD_CLOUD:
            response_data['keywords'] = data.get('keywords', [])
            if not response_data['keywords']:
                return jsonify({
                    'success': False,
                    'message': 'Please enter at least one keyword'
                }), 400
        
        # Check if this is an update (for short_answer and word_cloud)
        is_update = data.get('is_update', False)
        student_identifier = response_data['student_id']
        
        # For short answer and word cloud, allow updates
        if is_update and activity['type'] in [Activity.TYPE_SHORT_ANSWER, Activity.TYPE_WORD_CLOUD]:
            success = Activity.update_response(activity_id, student_identifier, response_data)
            action = 'updated'
        else:
            # Add new response (for poll, or first submission for short_answer/word_cloud)
            success = Activity.add_response(activity_id, response_data)
            action = 'submitted'
        
        if success:
            logger.info(f"Response {action} for activity {activity_id}")
            
            # Prepare result message
            result = {
                'success': True,
                'message': f'Response {action} successfully'
            }
            
            # For multi-question polls, include evaluation results
            if activity['type'] == Activity.TYPE_POLL and 'score' in response_data:
                result['evaluation'] = {
                    'score': response_data['score'],
                    'total': response_data['total'],
                    'percentage': response_data['percentage'],
                    'answers': response_data['answers']
                }
            
            return jsonify(result), 201
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to submit response'
            }), 500
        
    except Exception as e:
        logger.error(f"Submit response error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to submit response'
        }), 500

@activity_bp.route('/activity/<activity_id>/group-answers', methods=['POST'])
@login_required
def group_answers(activity_id):
    """
    Manually trigger AI answer grouping
    For short answer activities
    """
    try:
        activity = Activity.find_by_id(activity_id)
        
        if not activity:
            return jsonify({
                'success': False,
                'message': 'Activity not found'
            }), 404
        
        # Check ownership
        if activity['teacher_id'] != session['user_id']:
            return jsonify({
                'success': False,
                'message': 'Access denied'
            }), 403
        
        if activity['type'] != Activity.TYPE_SHORT_ANSWER:
            return jsonify({
                'success': False,
                'message': 'Only short answer activities can be grouped'
            }), 400
        
        responses = activity.get('responses', [])
        
        if not responses:
            return jsonify({
                'success': False,
                'message': 'No responses to group'
            }), 400
        
        # Group answers using AI
        logger.info(f"Grouping answers for activity {activity_id}")
        grouped = genai_service.group_answers(responses, activity['content']['question'])
        
        # Save grouped answers
        Activity.update_activity(activity_id, {'grouped_answers': grouped})
        
        logger.info(f"Answers grouped for activity {activity_id}")
        
        return jsonify({
            'success': True,
            'message': 'Answers grouped successfully',
            'grouped_answers': grouped
        }), 200
        
    except Exception as e:
        logger.error(f"Group answers error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to group answers'
        }), 500

@activity_bp.route('/activity/<activity_id>/delete', methods=['DELETE', 'POST'])
@login_required
def delete_activity(activity_id):
    """
    Delete activity (soft delete)
    """
    try:
        activity = Activity.find_by_id(activity_id)
        
        if not activity:
            return jsonify({
                'success': False,
                'message': 'Activity not found'
            }), 404
        
        # Check ownership
        if activity['teacher_id'] != session['user_id']:
            return jsonify({
                'success': False,
                'message': 'Access denied'
            }), 403
        
        # Soft delete
        success = Activity.delete_activity(activity_id)
        
        if success:
            logger.info(f"Activity deleted: {activity_id}")
            return jsonify({
                'success': True,
                'message': 'Activity deleted successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to delete activity'
            }), 400
        
    except Exception as e:
        logger.error(f"Delete activity error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to delete activity'
        }), 500
