"""
Course Model Module
Defines course data structure and operations
"""

from datetime import datetime
from bson import ObjectId
from services.db_service import db_service
from utils.time_utils import get_hk_time

class Course:
    """
    Course model for managing university courses
    """
    
    COLLECTION_NAME = 'courses'
    
    def __init__(self, name, code, teacher_id, description=''):
        """
        Initialize course object
        
        Args:
            name (str): Course name
            code (str): Course code
            teacher_id (str): ID of the teacher who created the course
            description (str): Course description
        """
        self.name = name
        self.code = code
        self.teacher_id = teacher_id
        self.description = description
        self.students = []
        self.created_at = get_hk_time()
        self.updated_at = get_hk_time()
        self.active = True
    
    def to_dict(self):
        """Convert course object to dictionary"""
        return {
            'name': self.name,
            'code': self.code,
            'teacher_id': self.teacher_id,
            'description': self.description,
            'students': self.students,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'active': self.active
        }
    
    def save(self):
        """
        Save course to database
        
        Returns:
            str: Inserted course ID
        """
        result = db_service.insert_one(Course.COLLECTION_NAME, self.to_dict())
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_id(course_id):
        """
        Find course by ID
        
        Args:
            course_id (str or ObjectId): Course ID
            
        Returns:
            dict: Course document or None
        """
        # Convert to ObjectId if it's a string
        if isinstance(course_id, str):
            try:
                course_id = ObjectId(course_id)
            except:
                return None
        return db_service.find_one(Course.COLLECTION_NAME, {'_id': course_id})
    
    @staticmethod
    def find_by_teacher(teacher_id):
        """
        Find all courses by teacher
        
        Args:
            teacher_id (str): Teacher ID
            
        Returns:
            list: List of course documents
        """
        return db_service.find_many(
            Course.COLLECTION_NAME,
            {'teacher_id': teacher_id, 'active': True},
            sort=[('created_at', -1)]
        )
    
    @staticmethod
    def find_by_code(code):
        """
        Find course by course code
        
        Args:
            code (str): Course code
            
        Returns:
            dict: Course document or None
        """
        return db_service.find_one(Course.COLLECTION_NAME, {'code': code})
    
    @staticmethod
    def update_course(course_id, update_data):
        """
        Update course information
        
        Args:
            course_id (str): Course ID
            update_data (dict): Data to update
            
        Returns:
            bool: True if successful
        """
        update_data['updated_at'] = get_hk_time()
        result = db_service.update_one(
            Course.COLLECTION_NAME,
            {'_id': ObjectId(course_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def add_student(course_id, student_id):
        """
        Add student to course
        
        Args:
            course_id (str): Course ID
            student_id (str): Student ID to add
            
        Returns:
            bool: True if successful
        """
        result = db_service.update_one(
            Course.COLLECTION_NAME,
            {'_id': ObjectId(course_id)},
            {'$addToSet': {'students': student_id}}
        )
        return result.modified_count > 0
    
    @staticmethod
    def remove_student(course_id, student_id):
        """
        Remove student from course
        
        Args:
            course_id (str): Course ID
            student_id (str): Student ID to remove
            
        Returns:
            bool: True if successful
        """
        result = db_service.update_one(
            Course.COLLECTION_NAME,
            {'_id': ObjectId(course_id)},
            {'$pull': {'students': student_id}}
        )
        return result.modified_count > 0
    
    @staticmethod
    def get_student_count(course_id):
        """
        Get number of students in course
        
        Args:
            course_id (str): Course ID
            
        Returns:
            int: Number of students
        """
        course = Course.find_by_id(course_id)
        if course:
            return len(course.get('students', []))
        return 0
    
    @staticmethod
    def delete_course(course_id):
        """
        Soft delete course (mark as inactive)
        
        Args:
            course_id (str): Course ID
            
        Returns:
            bool: True if successful
        """
        return Course.update_course(course_id, {'active': False})
    
    @staticmethod
    def get_all():
        """
        Get all active courses
        
        Returns:
            list: List of all active course documents
        """
        return db_service.find_many(
            Course.COLLECTION_NAME,
            {'active': True},
            sort=[('created_at', -1)]
        )
    
    @staticmethod
    def find_all():
        """
        Get all courses (including inactive) - for admin use
        
        Returns:
            list: List of all course documents
        """
        return db_service.find_many(
            Course.COLLECTION_NAME,
            {},
            sort=[('created_at', -1)]
        )
    
    @staticmethod
    def update(course_id, update_data):
        """
        Update course - wrapper for update_course
        
        Args:
            course_id (str): Course ID
            update_data (dict): Data to update
            
        Returns:
            bool: True if successful
        """
        return Course.update_course(course_id, update_data)
    
    @staticmethod
    def delete(course_id):
        """
        Hard delete course - for admin use
        
        Args:
            course_id (str): Course ID
            
        Returns:
            bool: True if successful
        """
        result = db_service.delete_one(
            Course.COLLECTION_NAME,
            {'_id': ObjectId(course_id)}
        )
        return result.deleted_count > 0
