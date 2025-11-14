"""
Student Model Module
Defines student data structure and operations
"""

from datetime import datetime
from bson import ObjectId
from services.db_service import db_service
from utils.time_utils import get_hk_time

class Student:
    """
    Student model for managing student information
    """
    
    COLLECTION_NAME = 'students'
    
    def __init__(self, student_id, name, course_id, email=''):
        """
        Initialize student object
        
        Args:
            student_id (str): Student ID number
            name (str): Student name
            course_id (str): ID of the course
            email (str): Student email (optional)
        """
        self.student_id = student_id
        self.name = name
        self.course_id = course_id
        self.email = email
        self.created_at = get_hk_time()
    
    def to_dict(self):
        """Convert student object to dictionary"""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'course_id': self.course_id,
            'email': self.email,
            'created_at': self.created_at
        }
    
    def save(self):
        """
        Save student to database
        
        Returns:
            str: Inserted student ID
        """
        result = db_service.insert_one(Student.COLLECTION_NAME, self.to_dict())
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_id(student_id):
        """
        Find student by database ID
        
        Args:
            student_id (str): Student database ID
            
        Returns:
            dict: Student document or None
        """
        return db_service.find_one(Student.COLLECTION_NAME, {'_id': ObjectId(student_id)})
    
    @staticmethod
    def find_by_student_id(student_id, course_id=None):
        """
        Find student by student ID number
        
        Args:
            student_id (str): Student ID number
            course_id (str): Course ID (optional)
            
        Returns:
            dict: Student document or None
        """
        query = {'student_id': student_id}
        if course_id:
            query['course_id'] = course_id
        return db_service.find_one(Student.COLLECTION_NAME, query)
    
    @staticmethod
    def find_by_course(course_id):
        """
        Find all students in a course
        
        Args:
            course_id (str): Course ID
            
        Returns:
            list: List of student documents
        """
        return db_service.find_many(
            Student.COLLECTION_NAME,
            {'course_id': course_id},
            sort=[('name', 1)]
        )
    
    @staticmethod
    def create(student_data):
        """
        Create a new student record
        
        Args:
            student_data (dict): Student data containing student_id, name, email, course_id
            
        Returns:
            str: Inserted student ID or None if already exists
        """
        # Check if student already exists in this course
        existing = db_service.find_one(
            Student.COLLECTION_NAME,
            {
                'student_id': student_data.get('student_id'),
                'course_id': student_data.get('course_id')
            }
        )
        
        if existing:
            return None  # Student already enrolled in this course
        
        # Add timestamp
        student_data['created_at'] = get_hk_time()
        
        # Insert new student
        result = db_service.insert_one(Student.COLLECTION_NAME, student_data)
        return str(result.inserted_id) if result.inserted_id else None
    
    @staticmethod
    def count_by_course(course_id):
        """
        Count students in a course
        
        Args:
            course_id (str): Course ID
            
        Returns:
            int: Number of students
        """
        return db_service.count_documents(Student.COLLECTION_NAME, {'course_id': course_id})
    
    @staticmethod
    def bulk_insert(students_data):
        """
        Insert multiple students at once
        
        Args:
            students_data (list): List of student dictionaries
            
        Returns:
            int: Number of students inserted
        """
        if not students_data:
            return 0
        
        collection = db_service.get_collection(Student.COLLECTION_NAME)
        result = collection.insert_many(students_data)
        return len(result.inserted_ids)
    
    @staticmethod
    def update_student(student_id, update_data):
        """
        Update student information
        
        Args:
            student_id (str): Student database ID
            update_data (dict): Data to update
            
        Returns:
            bool: True if successful
        """
        result = db_service.update_one(
            Student.COLLECTION_NAME,
            {'_id': ObjectId(student_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def delete_student(student_id):
        """
        Delete student from database
        
        Args:
            student_id (str): Student database ID
            
        Returns:
            bool: True if successful
        """
        result = db_service.delete_one(
            Student.COLLECTION_NAME,
            {'_id': ObjectId(student_id)}
        )
        return result.deleted_count > 0
    
    @staticmethod
    def unenroll(student_id, course_id):
        """
        Unenroll student from a course (delete enrollment record)
        For admin use when deleting courses
        
        Args:
            student_id (str): Student database ID
            course_id (str): Course ID to unenroll from
            
        Returns:
            bool: True if successful
        """
        result = db_service.delete_one(
            Student.COLLECTION_NAME,
            {
                '_id': ObjectId(student_id),
                'course_id': course_id
            }
        )
        return result.deleted_count > 0
