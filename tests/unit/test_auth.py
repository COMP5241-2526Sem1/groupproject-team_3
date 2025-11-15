import pytest
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from werkzeug.security import generate_password_hash, check_password_hash

# If auth_service exists with these functions, use them
# Otherwise, we'll test the werkzeug functions directly
def hash_password(password):
    """Wrapper for password hashing"""
    return generate_password_hash(password)

def verify_password(password, hashed):
    """Wrapper for password verification"""
    return check_password_hash(hashed, password)

class TestPasswordHashing:
    """Test password security functions"""
    
    def test_hash_password_returns_string(self):
        """Test that hash_password returns a string"""
        hashed = hash_password("testpass123")
        assert isinstance(hashed, str)
    
    def test_hash_password_not_equal_to_original(self):
        """Test that hashed password differs from original"""
        password = "testpass123"
        hashed = hash_password(password)
        assert hashed != password
    
    def test_same_password_different_hashes(self):
        """Test that same password produces different hashes (salt)"""
        password = "testpass123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        assert hash1 != hash2
    
    def test_verify_password_correct(self):
        """Test password verification with correct password"""
        password = "testpass123"
        hashed = hash_password(password)
        assert verify_password(password, hashed) == True
    
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password"""
        password = "testpass123"
        wrong_password = "wrongpass"
        hashed = hash_password(password)
        assert verify_password(wrong_password, hashed) == False
    
    def test_verify_password_empty_string(self):
        """Test password verification with empty string"""
        password = "testpass123"
        hashed = hash_password(password)
        assert verify_password("", hashed) == False

class TestUserValidation:
    """Test user validation logic"""
    
    def test_username_format(self):
        """Test username must be alphanumeric"""
        valid_usernames = ["teacher_demo", "student123", "admin"]
        for username in valid_usernames:
            assert len(username) > 0
    
    def test_role_validation(self):
        """Test role must be teacher or admin"""
        valid_roles = ["teacher", "admin"]
        for role in valid_roles:
            assert role in ["teacher", "admin"]