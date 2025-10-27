"""
Main Flask Application
Entry point for the Learning Activity Management System
"""

from flask import Flask, render_template, redirect, url_for
from config import config, Config
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_name='default'):
    """
    Create and configure Flask application
    
    Args:
        config_name (str): Configuration name (development/production/testing)
        
    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Configure session
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    # Create upload folder if it doesn't exist (skip in production/serverless)
    # Vercel functions run in read-only filesystem, use /tmp for temporary files
    if config_name != 'production' and not os.path.exists(Config.UPLOAD_FOLDER):
        try:
            os.makedirs(Config.UPLOAD_FOLDER)
        except OSError:
            # If we can't create uploads folder (e.g., read-only filesystem),
            # use /tmp directory which is writable in serverless environments
            Config.UPLOAD_FOLDER = '/tmp/uploads'
            if not os.path.exists(Config.UPLOAD_FOLDER):
                os.makedirs(Config.UPLOAD_FOLDER)
    
    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.course_routes import course_bp
    from routes.activity_routes import activity_bp
    from routes.admin_routes import admin_bp
    from routes.student_routes import student_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(activity_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(student_bp)
    
    # Home route
    @app.route('/')
    def index():
        """Home page - redirect to login or dashboard"""
        from flask import session
        if 'user_id' in session:
            role = session.get('role')
            if role == 'admin':
                return redirect(url_for('admin.admin_dashboard'))
            elif role == 'student':
                return redirect(url_for('student.dashboard'))
            else:  # teacher
                return redirect(url_for('course.dashboard'))
        return redirect(url_for('auth.login'))
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return render_template('error.html', 
                             error_code=404, 
                             error_message='Page not found'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        logger.error(f"Internal server error: {error}")
        return render_template('error.html', 
                             error_code=500, 
                             error_message='Internal server error'), 500
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 errors"""
        return render_template('error.html', 
                             error_code=403, 
                             error_message='Access denied'), 403
    
    # Template filters
    @app.template_filter('datetime_format')
    def datetime_format(value, format='%Y-%m-%d %H:%M'):
        """Format datetime for display"""
        if value is None:
            return ''
        return value.strftime(format)
    
    logger.info("Flask application created successfully")
    
    return app

if __name__ == '__main__':
    # Get environment
    env = os.getenv('FLASK_ENV', 'development')
    
    # Create app
    app = create_app(env)
    
    # Run app
    host = Config.APP_HOST
    port = Config.APP_PORT
    debug = env == 'development'
    
    logger.info(f"Starting application on {host}:{port} (Environment: {env})")
    logger.info(f"Access the application at: http://localhost:{port}")
    
    app.run(host=host, port=port, debug=debug)
