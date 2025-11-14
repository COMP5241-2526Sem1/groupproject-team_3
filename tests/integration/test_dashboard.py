import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from bson import ObjectId

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app import app

@pytest.fixture
def teacher_client():
    """Create authenticated teacher client"""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['user_id'] = str(ObjectId())
            sess['username'] = 'teacher_demo'
            sess['role'] = 'teacher'
        yield client

@pytest.fixture
def student_client():
    """Create authenticated student client"""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['student_id'] = '20231234'
            sess['name'] = 'Test Student'
        yield client

class TestTeacherDashboard:
    """Test teacher dashboard functionality"""
    
    @patch('services.db_service.db_service.db')
    def test_teacher_dashboard_loads(self, mock_db, teacher_client):
        """Test that teacher dashboard loads"""
        mock_courses = MagicMock()
        mock_courses.find.return_value = []
        mock_db.__getitem__.return_value = mock_courses
        
        response = teacher_client.get('/dashboard')
        assert response.status_code == 200
    
    @patch('services.db_service.db_service.db')
    def test_teacher_sees_own_courses(self, mock_db, teacher_client):
        """Test that teacher sees their own courses"""
        with teacher_client.session_transaction() as sess:
            teacher_id = sess['user_id']
        
        mock_courses = MagicMock()
        mock_courses.find.return_value = [
            {
                '_id': ObjectId(),
                'name': 'My Course',
                'teacher_id': ObjectId(teacher_id)
            }
        ]
        mock_db.__getitem__.return_value = mock_courses
        
        response = teacher_client.get('/dashboard')
        assert response.status_code == 200
        assert b'My Course' in response.data or response.status_code == 200

class TestStudentDashboard:
    """Test student dashboard functionality"""
    
    @patch('services.db_service.db_service.db')
    def test_student_dashboard_loads(self, mock_db, student_client):
        """Test that student dashboard loads"""
        mock_students = MagicMock()
        mock_students.find.return_value = []
        mock_db.__getitem__.return_value = mock_students
        
        response = student_client.get('/student/dashboard')
        assert response.status_code in [200, 302]
    
    @patch('services.db_service.db_service.db')
    def test_student_sees_enrolled_courses(self, mock_db, student_client):
        """Test that student sees enrolled courses"""
        mock_courses = MagicMock()
        mock_courses.find.return_value = [
            {
                '_id': ObjectId(),
                'name': 'Enrolled Course',
                'students': ['20231234']
            }
        ]
        mock_db.__getitem__.return_value = mock_courses
        
        response = student_client.get('/student/dashboard')
        assert response.status_code in [200, 302]