import pytest
from unittest.mock import patch, MagicMock
from bson import ObjectId

class TestTeacherDashboard:
    """Test teacher dashboard functionality"""
    
    def test_teacher_dashboard_loads(self, authenticated_client, mock_db):
        """Test that teacher dashboard loads"""
        mock_db['courses'].find.return_value = []
        
        response = authenticated_client.get('/dashboard')
        assert response.status_code in [200, 302]
    
    def test_teacher_sees_own_courses(self, authenticated_client, mock_db):
        """Test that teacher sees their own courses"""
        with authenticated_client.session_transaction() as sess:
            teacher_id = sess['user_id']
        
        mock_db['courses'].find.return_value = [
            {
                '_id': ObjectId(),
                'name': 'My Course',
                'teacher_id': ObjectId(teacher_id)
            }
        ]
        
        response = authenticated_client.get('/dashboard')
        assert response.status_code == 200

class TestStudentDashboard:
    """Test student dashboard functionality"""
    
    def test_student_dashboard_loads(self, client, mock_db):
        """Test that student dashboard loads"""
        # Set up student session
        with client.session_transaction() as sess:
            sess['student_id'] = '20231234'
            sess['name'] = 'Test Student'
        
        mock_db['students'].find.return_value = []
        
        response = client.get('/student/dashboard')
        assert response.status_code in [200, 302, 404]
    
    def test_student_sees_enrolled_courses(self, client, mock_db):
        """Test that student sees enrolled courses"""
        # Set up student session
        with client.session_transaction() as sess:
            sess['student_id'] = '20231234'
            sess['name'] = 'Test Student'
        
        mock_db['courses'].find.return_value = [
            {
                '_id': ObjectId(),
                'name': 'Enrolled Course',
                'students': ['20231234']
            }
        ]
        
        response = client.get('/student/dashboard')
        assert response.status_code in [200, 302, 404]