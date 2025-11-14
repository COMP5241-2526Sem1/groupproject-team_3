import pytest
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    with app.test_client() as client:
        yield client

@pytest.fixture
def runner():
    """Create a test runner for the Flask application"""
    return app.test_cli_runner()

class TestAppConfiguration:
    """Test Flask application configuration"""
    
    def test_app_exists(self):
        """Test that Flask app exists"""
        assert app is not None
    
    def test_app_is_testing(self, client):
        """Test that app is in testing mode"""
        assert app.config['TESTING'] == True
    
    def test_app_has_secret_key(self):
        """Test that app has a secret key configured"""
        assert app.config.get('SECRET_KEY') is not None

class TestBasicRoutes:
    """Test basic application routes"""
    
    def test_index_route(self, client):
        """Test the index route returns 200 or redirects"""
        response = client.get('/')
        assert response.status_code in [200, 302, 303]
    
    def test_login_route_exists(self, client):
        """Test the login route exists"""
        response = client.get('/login')
        assert response.status_code in [200, 302]
    
    def test_404_not_found(self, client):
        """Test that invalid routes return 404"""
        response = client.get('/this-route-does-not-exist')
        assert response.status_code == 404