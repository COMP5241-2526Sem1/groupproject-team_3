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
def client():
    """Create authenticated test client"""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['user_id'] = str(ObjectId())
            sess['username'] = 'teacher_demo'
            sess['role'] = 'teacher'
        yield client

class TestCourseCreation:
    """Test course creation workflow"""
    
    @patch('services.db_service.db_service.db')
    def test_create_course_page_loads(self, mock_db, client):
        """Test create course page loads"""
        response = client.get('/courses/create')
        assert response.status_code in [200, 302]
    
    @patch('services.db_service.db_service.db')
    def test_create_course_with_valid_data(self, mock_db, client):
        """Test creating a course with valid data"""
        mock_courses = MagicMock()
        mock_courses.insert_one.return_value.inserted_id = ObjectId()
        mock_db.__getitem__.return_value = mock_courses
        
        response = client.post('/courses/create', data={
            'name': 'Test Course',
            'code': 'TEST101',
            'description': 'A test course'
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    @patch('services.db_service.db_service.db')
    def test_create_course_missing_fields(self, mock_db, client):
        """Test creating course with missing required fields"""
        response = client.post('/courses/create', data={
            'name': 'Test Course'
            # Missing code
        })
        
        # Should show error or stay on page
        assert response.status_code in [200, 400]

class TestCourseViewing:
    """Test viewing courses"""
    
    @patch('services.db_service.db_service.db')
    def test_view_all_courses(self, mock_db, client):
        """Test viewing all courses"""
        mock_courses = MagicMock()
        mock_courses.find.return_value = [
            {
                '_id': ObjectId(),
                'name': 'Course 1',
                'code': 'C101',
                'teacher_id': ObjectId()
            }
        ]
        mock_db.__getitem__.return_value = mock_courses
        
        response = client.get('/courses')
        assert response.status_code == 200
    
    @patch('services.db_service.db_service.db')
    def test_view_single_course(self, mock_db, client):
        """Test viewing a single course detail"""
        course_id = str(ObjectId())
        
        mock_courses = MagicMock()
        mock_courses.find_one.return_value = {
            '_id': ObjectId(course_id),
            'name': 'Test Course',
            'code': 'TEST101',
            'teacher_id': ObjectId()
        }
        mock_db.__getitem__.return_value = mock_courses
        
        response = client.get(f'/courses/{course_id}')
        assert response.status_code in [200, 404]

class TestCourseEnrollment:
    """Test student enrollment in courses"""
    
    @patch('services.db_service.db_service.db')
    def test_enroll_student_in_course(self, mock_db, client):
        """Test enrolling a student in a course"""
        course_id = str(ObjectId())
        
        mock_courses = MagicMock()
        mock_courses.update_one.return_value.modified_count = 1
        mock_db.__getitem__.return_value = mock_courses
        
        response = client.post(f'/courses/{course_id}/enroll', data={
            'student_id': '20231234',
            'student_name': 'Test Student'
        }, follow_redirects=True)
        
        assert response.status_code == 200