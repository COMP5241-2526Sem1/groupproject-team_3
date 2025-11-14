"""
Authentication Service Module
Handles user authentication, registration, and password management
"""

import bcrypt
import logging
from datetime import datetime
from bson import ObjectId
from services.db_service import db_service
from utils.time_utils import get_hk_time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthService:
    """
    Authentication service for user management
    Handles registration, login, and password hashing
    """
    
    def __init__(self):
        """Initialize authentication service"""
        self.users_collection = db_service.get_collection('users')
        logger.info("Auth Service initialized")
    
    def hash_password(self, password):
        """
        Hash password using bcrypt
        
        Args:
            password (str): Plain text password
            
        Returns:
            str: Hashed password
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password, hashed_password):
        """
        Verify password against hash
        
        Args:
            password (str): Plain text password
            hashed_password (str): Hashed password
            
        Returns:
            bool: True if password matches
        """
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    
    def register_user(self, username, password, email, role='teacher', institution='', student_id=None):
        """
        Register a new user (teacher, student, or admin)
        
        Args:
            username (str): Username
            password (str): Password
            email (str): Email address
            role (str): User role (teacher/student/admin)
            institution (str): Institution name
            student_id (str): Student ID (required for student role)
            
        Returns:
            dict: Result with success status and user_id or error message
        """
        try:
            # Check if username already exists
            existing_user = self.users_collection.find_one({'username': username})
            if existing_user:
                return {
                    'success': False,
                    'message': 'Username already exists'
                }
            
            # Check if email already exists
            existing_email = self.users_collection.find_one({'email': email})
            if existing_email:
                return {
                    'success': False,
                    'message': 'Email already registered'
                }
            
            # For student role, check if student_id is provided and unique
            if role == 'student':
                if not student_id:
                    return {
                        'success': False,
                        'message': 'Student ID is required for student registration'
                    }
                
                existing_student = self.users_collection.find_one({'student_id': student_id})
                if existing_student:
                    return {
                        'success': False,
                        'message': 'Student ID already registered'
                    }
            
            # Hash password
            hashed_password = self.hash_password(password)
            
            # Create user document
            user_doc = {
                'username': username,
                'password': hashed_password,
                'email': email,
                'role': role,
                'institution': institution,
                'created_at': get_hk_time(),
                'last_login': None,
                'active': True,
                'enrolled_courses': []  # For students
            }
            
            # Add student_id for student role
            if role == 'student' and student_id:
                user_doc['student_id'] = student_id
            
            # Insert user
            result = self.users_collection.insert_one(user_doc)
            
            logger.info(f"User registered successfully: {username} ({role})")
            
            return {
                'success': True,
                'user_id': str(result.inserted_id),
                'message': 'Registration successful'
            }
            
        except Exception as e:
            logger.error(f"Error during registration: {e}")
            return {
                'success': False,
                'message': 'Registration failed. Please try again.'
            }
    
    def login_user(self, username, password):
        """
        Authenticate user login
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            dict: Result with success status and user info or error message
        """
        try:
            # Find user
            user = self.users_collection.find_one({'username': username})
            
            if not user:
                return {
                    'success': False,
                    'message': 'Invalid username or password'
                }
            
            # Verify password
            if not self.verify_password(password, user['password']):
                return {
                    'success': False,
                    'message': 'Invalid username or password'
                }
            
            # Check if user is active
            if not user.get('active', True):
                return {
                    'success': False,
                    'message': 'Account is deactivated'
                }
            
            # Update last login
            self.users_collection.update_one(
                {'_id': user['_id']},
                {'$set': {'last_login': get_hk_time()}}
            )
            
            logger.info(f"User logged in successfully: {username}")
            
            # Return user info (without password)
            return {
                'success': True,
                'user': {
                    'id': str(user['_id']),
                    'username': user['username'],
                    'email': user['email'],
                    'role': user['role'],
                    'institution': user.get('institution', '')
                }
            }
            
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return {
                'success': False,
                'message': 'Login failed. Please try again.'
            }
    
    def get_user_by_id(self, user_id):
        """
        Get user information by ID
        
        Args:
            user_id (str): User ID
            
        Returns:
            dict: User information or None
        """
        try:
            user = self.users_collection.find_one({'_id': ObjectId(user_id)})
            
            if user:
                user['_id'] = str(user['_id'])
                del user['password']  # Remove password from response
                return user
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching user: {e}")
            return None
    
    def update_user(self, user_id, update_data):
        """
        Update user information
        
        Args:
            user_id (str): User ID
            update_data (dict): Data to update
            
        Returns:
            bool: True if successful
        """
        try:
            # Don't allow updating certain fields
            restricted_fields = ['_id', 'password', 'role', 'created_at']
            for field in restricted_fields:
                if field in update_data:
                    del update_data[field]
            
            result = self.users_collection.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': update_data}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            return False
    
    def change_password(self, user_id, old_password, new_password):
        """
        Change user password
        
        Args:
            user_id (str): User ID
            old_password (str): Current password
            new_password (str): New password
            
        Returns:
            dict: Result with success status and message
        """
        try:
            user = self.users_collection.find_one({'_id': ObjectId(user_id)})
            
            if not user:
                return {
                    'success': False,
                    'message': 'User not found'
                }
            
            # Verify old password
            if not self.verify_password(old_password, user['password']):
                return {
                    'success': False,
                    'message': 'Current password is incorrect'
                }
            
            # Hash new password
            hashed_password = self.hash_password(new_password)
            
            # Update password
            self.users_collection.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': {'password': hashed_password}}
            )
            
            logger.info(f"Password changed for user: {user['username']}")
            
            return {
                'success': True,
                'message': 'Password changed successfully'
            }
            
        except Exception as e:
            logger.error(f"Error changing password: {e}")
            return {
                'success': False,
                'message': 'Failed to change password'
            }

# Create global auth service instance
auth_service = AuthService()
