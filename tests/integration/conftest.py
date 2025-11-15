import sys
import os
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock
import pytest

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Set environment variables before any imports
os.environ.setdefault('MONGODB_URI', 'mongodb://localhost:27017/test_db')
os.environ.setdefault('SECRET_KEY', 'test_secret_key')
os.environ.setdefault('FLASK_ENV', 'testing')

# Create mock database collections
def create_mock_db():
    """Create a mock database instance"""
    mock_db = MagicMock()
    collections = {}
    
    def get_collection_func(name):
        """Get or create a mock collection"""
        if name not in collections:
            collections[name] = MagicMock()
        return collections[name]
    
    # Configure __getitem__ to handle being called as db['collection']
    # MagicMock will pass self as first argument, so we need to ignore it
    mock_db.__getitem__ = lambda self, name: get_collection_func(name)
    
    # Configure get_collection method
    mock_db.get_collection = lambda name: get_collection_func(name)
    
    return mock_db, collections

# Global mock that will be used during import
_mock_db, _mock_collections = create_mock_db()

@pytest.fixture(scope='session', autouse=True)
def mock_mongodb():
    """Mock MongoDB connection at session level"""
    with patch('pymongo.MongoClient') as mock_client:
        mock_client.return_value.__getitem__.return_value = _mock_db
        yield mock_client

@pytest.fixture(scope='session')
def app():
    """Create Flask app for testing"""
    # Patch the db_service before importing
    with patch('services.db_service.DatabaseService.db', new_callable=PropertyMock) as mock_db_prop:
        mock_db_prop.return_value = _mock_db
        
        # Now it's safe to import
        from app import create_app
        test_app = create_app()
        test_app.config['TESTING'] = True
        test_app.config['WTF_CSRF_ENABLED'] = False
        
        yield test_app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def authenticated_client(app):
    """Create authenticated test client"""
    from bson import ObjectId
    
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['user_id'] = str(ObjectId())
            sess['username'] = 'teacher_demo'
            sess['role'] = 'teacher'
        yield client

@pytest.fixture
def mock_db():
    """Provide mock database collections for tests"""
    # Create fresh mocks for each test
    mock_courses = MagicMock()
    mock_activities = MagicMock()
    mock_students = MagicMock()
    mock_users = MagicMock()
    
    def getitem_side_effect(name):
        """Return the appropriate mock collection"""
        if name == 'courses':
            return mock_courses
        elif name == 'activities':
            return mock_activities
        elif name == 'students':
            return mock_students
        elif name == 'users':
            return mock_users
        return MagicMock()
    
    with patch('services.db_service.DatabaseService.db', new_callable=PropertyMock) as mock_db_property:
        mock_db_inst = MagicMock()
        # Configure __getitem__ to ignore self
        mock_db_inst.__getitem__ = lambda self, name: getitem_side_effect(name)
        # Configure get_collection method
        mock_db_inst.get_collection = lambda name: getitem_side_effect(name)
        mock_db_property.return_value = mock_db_inst
        
        yield {
            'db': mock_db_inst,
            'courses': mock_courses,
            'activities': mock_activities,
            'students': mock_students,
            'users': mock_users
        }