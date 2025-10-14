"""
User Model Module
Defines user data structure and operations
"""

from datetime import datetime
from bson import ObjectId
from services.db_service import db_service

class User:
    """
    User model for teachers, students, and administrators
    Supports three roles: teacher, student, admin
    """
    
    COLLECTION_NAME = 'users'
    
    def __init__(self, username, email, role='teacher', institution='', password=None, student_id=None):
        """
        Initialize user object
        
        Args:
            username (str): Username
            email (str): Email address
            role (str): User role (teacher/student/admin)
            institution (str): Institution name
            password (str): Hashed password
            student_id (str): Student ID (for student role)
        """
        self.username = username
        self.email = email
        self.role = role  # teacher, student, or admin
        self.institution = institution
        self.password = password
        self.student_id = student_id  # Only for students
        self.created_at = datetime.utcnow()
        self.last_login = None
        self.active = True
        self.enrolled_courses = []  # List of course IDs (for students)
    
    def to_dict(self):
        """Convert user object to dictionary"""
        user_dict = {
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'institution': self.institution,
            'password': self.password,
            'created_at': self.created_at,
            'last_login': self.last_login,
            'active': self.active,
            'enrolled_courses': getattr(self, 'enrolled_courses', [])
        }
        
        # Add student_id only for student role
        if self.role == 'student' and hasattr(self, 'student_id'):
            user_dict['student_id'] = self.student_id
            
        return user_dict
    
    @staticmethod
    def find_by_username(username):
        """
        Find user by username
        
        Args:
            username (str): Username to search
            
        Returns:
            dict: User document or None
        """
        return db_service.find_one(User.COLLECTION_NAME, {'username': username})
    
    @staticmethod
    def find_by_id(user_id):
        """
        Find user by ID
        
        Args:
            user_id (str or ObjectId): User ID
            
        Returns:
            dict: User document or None
        """
        # Convert to ObjectId if it's a string
        if isinstance(user_id, str):
            try:
                user_id = ObjectId(user_id)
            except:
                return None
        return db_service.find_one(User.COLLECTION_NAME, {'_id': user_id})
    
    @staticmethod
    def find_by_email(email):
        """
        Find user by email
        
        Args:
            email (str): Email address
            
        Returns:
            dict: User document or None
        """
        return db_service.find_one(User.COLLECTION_NAME, {'email': email})
    
    @staticmethod
    def get_all_teachers():
        """
        Get all teacher accounts
        
        Returns:
            list: List of teacher documents
        """
        return db_service.find_many(User.COLLECTION_NAME, {'role': 'teacher'})
    
    @staticmethod
    def get_all_students():
        """
        Get all student accounts
        
        Returns:
            list: List of student documents
        """
        return db_service.find_many(User.COLLECTION_NAME, {'role': 'student'})
    
    @staticmethod
    def find_by_student_id(student_id):
        """
        Find user by student ID
        
        Args:
            student_id (str): Student ID
            
        Returns:
            dict: User document or None
        """
        return db_service.find_one(User.COLLECTION_NAME, {'student_id': student_id})
    
    @staticmethod
    def enroll_course(user_id, course_id):
        """
        Enroll student in a course
        
        Args:
            user_id (str): User ID
            course_id (str): Course ID
            
        Returns:
            bool: Success status
        """
        return db_service.update_one(
            User.COLLECTION_NAME,
            {'_id': ObjectId(user_id)},
            {'$addToSet': {'enrolled_courses': str(course_id)}}
        )
    
    @staticmethod
    def unenroll_course(user_id, course_id):
        """
        Unenroll student from a course
        
        Args:
            user_id (str): User ID
            course_id (str): Course ID
            
        Returns:
            bool: Success status
        """
        return db_service.update_one(
            User.COLLECTION_NAME,
            {'_id': ObjectId(user_id)},
            {'$pull': {'enrolled_courses': str(course_id)}}
        )
    
    @staticmethod
    def count_teachers():
        """
        Count total number of teachers
        
        Returns:
            int: Number of teachers
        """
        return db_service.count_documents(User.COLLECTION_NAME, {'role': 'teacher'})
