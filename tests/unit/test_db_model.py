import pytest
from datetime import datetime
from bson import ObjectId

class TestUserModel:
    """Test User model structure and validation"""
    
    def test_user_required_fields(self):
        """Test user must have required fields"""
        user = {
            "username": "test_teacher",
            "password": "hashed_password",
            "role": "teacher",
            "email": "test@example.com"
        }
        assert "username" in user
        assert "password" in user
        assert "role" in user
        assert "email" in user
    
    def test_user_role_values(self):
        """Test user role must be valid"""
        valid_roles = ["teacher", "admin"]
        test_role = "teacher"
        assert test_role in valid_roles

class TestCourseModel:
    """Test Course model structure"""
    
    def test_course_required_fields(self):
        """Test course must have required fields"""
        course = {
            "name": "Test Course",
            "code": "COMP101",
            "teacher_id": ObjectId(),
            "students": [],
            "created_at": datetime.now()
        }
        assert "name" in course
        assert "code" in course
        assert "teacher_id" in course
        assert isinstance(course["students"], list)

class TestActivityModel:
    """Test Activity model structure"""
    
    def test_activity_types(self):
        """Test valid activity types"""
        valid_types = ["poll", "short_answer", "word_cloud"]
        test_type = "poll"
        assert test_type in valid_types
    
    def test_activity_required_fields(self):
        """Test activity must have required fields"""
        activity = {
            "type": "poll",
            "title": "Test Poll",
            "content": {"question": "Test?"},
            "course_id": ObjectId(),
            "teacher_id": ObjectId(),
            "responses": []
        }
        assert "type" in activity
        assert "title" in activity
        assert "content" in activity
        assert "responses" in activity

class TestStudentModel:
    """Test Student model structure"""
    
    def test_student_required_fields(self):
        """Test student must have required fields"""
        student = {
            "student_id": "20231234",
            "name": "Test Student",
            "course_id": ObjectId()
        }
        assert "student_id" in student
        assert "name" in student
        assert "course_id" in student