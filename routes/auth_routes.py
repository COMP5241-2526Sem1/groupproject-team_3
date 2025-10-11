"""
Authentication Routes Module
Handles user registration, login, and logout endpoints
"""

from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from services.auth_service import auth_service
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Teacher registration endpoint
    GET: Show registration form
    POST: Process registration
    """
    if request.method == 'GET':
        return render_template('register.html')
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        # Validate required fields
        required_fields = ['username', 'password', 'email']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'{field.capitalize()} is required'
                }), 400
        
        # Extract data
        username = data.get('username').strip()
        password = data.get('password')
        email = data.get('email').strip()
        institution = data.get('institution', '').strip()
        
        # Validate password length
        if len(password) < 6:
            return jsonify({
                'success': False,
                'message': 'Password must be at least 6 characters'
            }), 400
        
        # Register user
        result = auth_service.register_user(
            username=username,
            password=password,
            email=email,
            role='teacher',
            institution=institution
        )
        
        if result['success']:
            logger.info(f"New teacher registered: {username}")
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({
            'success': False,
            'message': 'Registration failed. Please try again.'
        }), 500

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login endpoint
    GET: Show login form
    POST: Process login
    """
    if request.method == 'GET':
        # Redirect to dashboard if already logged in
        if 'user_id' in session:
            return redirect(url_for('course.dashboard'))
        return render_template('login.html')
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        # Validate required fields
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400
        
        # Authenticate user
        result = auth_service.login_user(username, password)
        
        if result['success']:
            # Store user info in session
            user = result['user']
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            
            logger.info(f"User logged in: {username} ({user['role']})")
            
            # Return redirect URL based on role
            if user['role'] == 'admin':
                redirect_url = url_for('admin.admin_dashboard')
            else:
                redirect_url = url_for('course.dashboard')
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'redirect': redirect_url,
                'user': user
            }), 200
        else:
            return jsonify(result), 401
            
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({
            'success': False,
            'message': 'Login failed. Please try again.'
        }), 500

@auth_bp.route('/logout')
def logout():
    """
    User logout endpoint
    Clears session and redirects to login
    """
    username = session.get('username', 'Unknown')
    session.clear()
    logger.info(f"User logged out: {username}")
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
def profile():
    """
    View user profile
    Requires authentication
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = auth_service.get_user_by_id(session['user_id'])
    if not user:
        return redirect(url_for('auth.logout'))
    
    return render_template('profile.html', user=user)

@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    """
    Change user password
    Requires authentication
    """
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'message': 'Not authenticated'
        }), 401
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        old_password = data.get('old_password', '')
        new_password = data.get('new_password', '')
        confirm_password = data.get('confirm_password', '')
        
        # Validate fields
        if not all([old_password, new_password, confirm_password]):
            return jsonify({
                'success': False,
                'message': 'All fields are required'
            }), 400
        
        if new_password != confirm_password:
            return jsonify({
                'success': False,
                'message': 'New passwords do not match'
            }), 400
        
        if len(new_password) < 6:
            return jsonify({
                'success': False,
                'message': 'Password must be at least 6 characters'
            }), 400
        
        # Change password
        result = auth_service.change_password(
            session['user_id'],
            old_password,
            new_password
        )
        
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        logger.error(f"Change password error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to change password'
        }), 500
