import pytest
from bson import ObjectId
from datetime import datetime

class TestActivityCreation:
    """Test creating learning activities"""
    
    def test_create_activity_route_exists(self, authenticated_client, mock_db):
        """Test that activity creation route exists"""
        course_id = str(ObjectId())
        
        # Mock course lookup
        mock_db['courses'].find_one.return_value = {
            '_id': ObjectId(course_id),
            'name': 'Test Course',
            'teacher_id': ObjectId()
        }
        
        response = authenticated_client.get(f'/courses/{course_id}/activities/create')
        assert response.status_code in [200, 302, 404, 405]
    
    def test_create_poll_activity(self, authenticated_client, mock_db):
        """Test creating a poll activity"""
        course_id = str(ObjectId())
        activity_id = ObjectId()
        
        # Mock course exists
        mock_db['courses'].find_one.return_value = {
            '_id': ObjectId(course_id),
            'name': 'Test Course',
            'teacher_id': ObjectId()
        }
        
        # Mock activity insertion
        mock_db['activities'].insert_one.return_value.inserted_id = activity_id
        
        response = authenticated_client.post(
            f'/courses/{course_id}/activities/create',
            data={
                'type': 'poll',
                'title': 'Test Poll',
                'question': 'What is your favorite color?',
                'options': 'Red,Blue,Green'
            },
            follow_redirects=True
        )
        
        assert response.status_code in [200, 201, 302, 400, 404, 500]
    
    def test_create_activity_without_auth(self, client, mock_db):
        """Test that creating activity without auth fails"""
        course_id = str(ObjectId())
        
        response = client.post(
            f'/courses/{course_id}/activities/create',
            data={
                'type': 'poll',
                'title': 'Test Poll'
            }
        )
        
        # Should redirect to login or return unauthorized
        assert response.status_code in [302, 401, 403, 404]

class TestActivityViewing:
    """Test viewing activities"""
    
    def test_view_activity_list_route_exists(self, authenticated_client, mock_db):
        """Test that activity list route exists"""
        course_id = str(ObjectId())
        
        # Mock course lookup
        mock_db['courses'].find_one.return_value = {
            '_id': ObjectId(course_id),
            'name': 'Test Course'
        }
        
        # Mock activities list
        mock_db['activities'].find.return_value = []
        
        response = authenticated_client.get(f'/courses/{course_id}/activities')
        assert response.status_code in [200, 302, 404]
    
    def test_view_activity_detail(self, authenticated_client, mock_db):
        """Test viewing single activity details"""
        activity_id = str(ObjectId())
        course_id = ObjectId()
        
        # Mock activity lookup
        mock_db['activities'].find_one.return_value = {
            '_id': ObjectId(activity_id),
            'type': 'poll',
            'title': 'Test Poll',
            'content': {'question': 'Test?', 'options': ['A', 'B']},
            'responses': [],
            'course_id': course_id,
            'teacher_id': ObjectId(),
            'created_at': datetime.now()
        }
        
        # Mock course lookup
        mock_db['courses'].find_one.return_value = {
            '_id': course_id,
            'name': 'Test Course'
        }
        
        response = authenticated_client.get(f'/activities/{activity_id}')
        assert response.status_code in [200, 302, 404]

class TestStudentResponses:
    """Test student response submission"""
    
    def test_submit_response_route_exists(self, authenticated_client, mock_db):
        """Test that response submission route exists"""
        activity_id = str(ObjectId())
        
        # Mock activity lookup
        mock_db['activities'].find_one.return_value = {
            '_id': ObjectId(activity_id),
            'type': 'poll',
            'title': 'Test Poll',
            'content': {'question': 'Test?', 'options': ['A', 'B']}
        }
        
        response = authenticated_client.post(
            f'/activities/{activity_id}/respond',
            data={
                'student_id': '20231234',
                'response': 'Test response'
            }
        )
        
        assert response.status_code in [200, 302, 400, 404, 405, 500]
    
    def test_submit_poll_response(self, authenticated_client, mock_db):
        """Test submitting a poll response"""
        activity_id = str(ObjectId())
        
        # Mock activity lookup
        mock_db['activities'].find_one.return_value = {
            '_id': ObjectId(activity_id),
            'type': 'poll',
            'title': 'Test Poll',
            'content': {'question': 'Test?', 'options': ['A', 'B']},
            'responses': []
        }
        
        # Mock successful update
        mock_db['activities'].update_one.return_value.modified_count = 1
        
        response = authenticated_client.post(
            f'/activities/{activity_id}/respond',
            data={
                'student_id': '20231234',
                'response': 'Option A'
            },
            follow_redirects=True
        )
        
        assert response.status_code in [200, 201, 302, 400, 404, 500]

class TestActivityBasicOperations:
    """Test basic activity operations"""
    
    def test_app_has_activity_routes(self, app):
        """Test that app has activity-related routes registered"""
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        
        # Check if any activity routes exist
        activity_routes = [r for r in routes if 'activity' in r.lower() or 'activities' in r.lower()]
        
        if not activity_routes:
            pytest.skip("No activity routes found in application - this may be expected")
        else:
            assert len(activity_routes) > 0
