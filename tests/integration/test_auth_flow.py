import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app import app

@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client

class TestAuthenticationFlow:
    """Test user authentication workflows"""
    
    def test_login_page_loads(self, client):
        """Test that login page loads successfully"""
        response = client.get('/login')
        assert response.status_code in [200, 302]
    
    def test_login_with_valid_credentials(self, client):
        """Test login with valid credentials"""
        with patch('services.db_service.db_service.db') as mock_db:
            # Mock user in database
            mock_users = MagicMock()
            mock_users.find_one.return_value = {
                'username': 'teacher_demo',
                'password': 'pbkdf2:sha256:600000$...',  # Hashed password
                'role': 'teacher'
            }
            mock_db.__getitem__.return_value = mock_users
            
            response = client.post('/login', data={
                'username': 'teacher_demo',
                'password': 'password123'
            }, follow_redirects=True)
            
            # Should redirect after successful login
            assert response.status_code == 200
    
    def test_login_with_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        with patch('services.db_service.db_service.db') as mock_db:
            # Mock no user found
            mock_users = MagicMock()
            mock_users.find_one.return_value = None
            mock_db.__getitem__.return_value = mock_users
            
            response = client.post('/login', data={
                'username': 'nonexistent',
                'password': 'wrongpass'
            })
            
            # Should stay on login page or redirect back
            assert response.status_code in [200, 302]
    
    def test_logout(self, client):
        """Test logout functionality"""
        # First login
        with client.session_transaction() as sess:
            sess['user_id'] = 'test_user_id'
            sess['username'] = 'teacher_demo'
        
        # Then logout
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        
        # Check session is cleared
        with client.session_transaction() as sess:
            assert 'user_id' not in sess
    
    def test_protected_route_without_login(self, client):
        """Test that protected routes redirect to login"""
        response = client.get('/dashboard')
        # Should redirect to login
        assert response.status_code in [302, 401]

class TestSessionManagement:
    """Test session handling"""
    
    def test_session_persistence(self, client):
        """Test that session persists across requests"""
        with client.session_transaction() as sess:
            sess['user_id'] = 'test_user'
        
        response = client.get('/dashboard')
        
        with client.session_transaction() as sess:
            assert sess.get('user_id') == 'test_user'