"""
Activity Model Module
Defines learning activity data structure and operations
"""

from datetime import datetime
from bson import ObjectId
from services.db_service import db_service
import secrets
import string

class Activity:
    """
    Learning activity model for polls, short answers, and word clouds
    """
    
    COLLECTION_NAME = 'activities'
    
    # Activity types
    TYPE_POLL = 'poll'
    TYPE_SHORT_ANSWER = 'short_answer'
    TYPE_WORD_CLOUD = 'word_cloud'
    
    def __init__(self, title, activity_type, content, course_id, teacher_id):
        """
        Initialize activity object
        
        Args:
            title (str): Activity title
            activity_type (str): Type of activity (poll/short_answer/word_cloud)
            content (dict): Activity content (questions, options, etc.)
            course_id (str): ID of the course
            teacher_id (str): ID of the teacher who created the activity
        """
        self.title = title
        self.type = activity_type
        self.content = content
        self.course_id = course_id
        self.teacher_id = teacher_id
        self.link = self._generate_unique_link()
        self.responses = []
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.active = True
        self.ai_generated = content.get('ai_generated', False)
    
    def _generate_unique_link(self):
        """
        Generate unique access link for activity
        
        Returns:
            str: Unique link identifier
        """
        # Generate random string for unique link
        chars = string.ascii_letters + string.digits
        return ''.join(secrets.choice(chars) for _ in range(10))
    
    def to_dict(self):
        """Convert activity object to dictionary"""
        return {
            'title': self.title,
            'type': self.type,
            'content': self.content,
            'course_id': self.course_id,
            'teacher_id': self.teacher_id,
            'link': self.link,
            'responses': self.responses,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'active': self.active,
            'ai_generated': self.ai_generated
        }
    
    def save(self):
        """
        Save activity to database
        
        Returns:
            str: Inserted activity ID
        """
        result = db_service.insert_one(Activity.COLLECTION_NAME, self.to_dict())
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_id(activity_id):
        """
        Find activity by ID
        
        Args:
            activity_id (str or ObjectId): Activity ID
            
        Returns:
            dict: Activity document or None
        """
        # Convert to ObjectId if it's a string
        if isinstance(activity_id, str):
            try:
                activity_id = ObjectId(activity_id)
            except:
                return None
        return db_service.find_one(Activity.COLLECTION_NAME, {'_id': activity_id})
    
    @staticmethod
    def find_by_link(link):
        """
        Find activity by unique link
        
        Args:
            link (str): Activity link
            
        Returns:
            dict: Activity document or None
        """
        return db_service.find_one(Activity.COLLECTION_NAME, {'link': link})
    
    @staticmethod
    def find_by_course(course_id):
        """
        Find all activities in a course
        
        Args:
            course_id (str or ObjectId): Course ID
            
        Returns:
            list: List of activity documents
        """
        # Convert to string for comparison (activities store course_id as string)
        if isinstance(course_id, ObjectId):
            course_id = str(course_id)
        return db_service.find_many(
            Activity.COLLECTION_NAME,
            {'course_id': course_id, 'active': True},
            sort=[('created_at', -1)]
        )
    
    @staticmethod
    def find_by_teacher(teacher_id):
        """
        Find all activities by teacher
        
        Args:
            teacher_id (str): Teacher ID
            
        Returns:
            list: List of activity documents
        """
        return db_service.find_many(
            Activity.COLLECTION_NAME,
            {'teacher_id': teacher_id, 'active': True},
            sort=[('created_at', -1)]
        )
    
    @staticmethod
    def add_response(activity_id, response_data):
        """
        Add student response to activity
        
        Args:
            activity_id (str): Activity ID
            response_data (dict): Response data with student info and answer
            
        Returns:
            bool: True if successful
        """
        response_data['submitted_at'] = datetime.utcnow()
        result = db_service.update_one(
            Activity.COLLECTION_NAME,
            {'_id': ObjectId(activity_id)},
            {
                '$push': {'responses': response_data},
                '$set': {'updated_at': datetime.utcnow()}
            }
        )
        return result.modified_count > 0
    
    @staticmethod
    def update_response(activity_id, student_identifier, response_data):
        """
        Update existing student response to activity
        Allows students to modify their short answer or word cloud responses
        
        Args:
            activity_id (str): Activity ID
            student_identifier (str): student_id or student_name to identify the response
            response_data (dict): Updated response data
            
        Returns:
            bool: True if successful
        """
        response_data['submitted_at'] = datetime.utcnow()
        
        # Find the activity and locate the response index
        activity = Activity.find_by_id(activity_id)
        if not activity:
            return False
        
        responses = activity.get('responses', [])
        response_index = None
        
        # Find the response by student_id or student_name
        for i, response in enumerate(responses):
            if (response.get('student_id') == student_identifier or 
                response.get('student_name') == student_identifier):
                response_index = i
                break
        
        if response_index is None:
            # Response doesn't exist, add it instead
            return Activity.add_response(activity_id, response_data)
        
        # Update the specific response
        update_fields = {}
        for key, value in response_data.items():
            update_fields[f'responses.{response_index}.{key}'] = value
        
        update_fields['updated_at'] = datetime.utcnow()
        
        result = db_service.update_one(
            Activity.COLLECTION_NAME,
            {'_id': ObjectId(activity_id)},
            {'$set': update_fields}
        )
        return result.modified_count > 0
    
    @staticmethod
    def get_responses(activity_id):
        """
        Get all responses for an activity
        
        Args:
            activity_id (str): Activity ID
            
        Returns:
            list: List of responses
        """
        activity = Activity.find_by_id(activity_id)
        if activity:
            return activity.get('responses', [])
        return []
    
    @staticmethod
    def get_response_count(activity_id):
        """
        Get number of responses for an activity
        
        Args:
            activity_id (str): Activity ID
            
        Returns:
            int: Number of responses
        """
        activity = Activity.find_by_id(activity_id)
        if activity:
            return len(activity.get('responses', []))
        return 0
    
    @staticmethod
    def update_activity(activity_id, update_data):
        """
        Update activity information
        
        Args:
            activity_id (str): Activity ID
            update_data (dict): Data to update
            
        Returns:
            bool: True if successful
        """
        update_data['updated_at'] = datetime.utcnow()
        result = db_service.update_one(
            Activity.COLLECTION_NAME,
            {'_id': ObjectId(activity_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def delete_activity(activity_id):
        """
        Soft delete activity (mark as inactive)
        
        Args:
            activity_id (str): Activity ID
            
        Returns:
            bool: True if successful
        """
        return Activity.update_activity(activity_id, {'active': False})
    
    @staticmethod
    def count_all():
        """
        Count total number of activities
        
        Returns:
            int: Number of activities
        """
        return db_service.count_documents(Activity.COLLECTION_NAME, {'active': True})
    
    @staticmethod
    def count_by_type(activity_type):
        """
        Count activities by type
        
        Args:
            activity_type (str): Activity type
            
        Returns:
            int: Number of activities
        """
        return db_service.count_documents(
            Activity.COLLECTION_NAME,
            {'type': activity_type, 'active': True}
        )
