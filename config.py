"""
Configuration Management Module
Handles environment variables and application configuration
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Application configuration class
    Centralizes all configuration parameters
    """
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # MongoDB Configuration
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    DATABASE_NAME = 'learning_activity_system'
    
    # OpenAI Configuration
    # Supports both OpenAI API keys (sk-...) and GitHub Personal Access Tokens (github_pat_...)
    # For GitHub Models: Use your GitHub PAT and set model to 'gpt-4o-mini'
    # For OpenAI: Use your OpenAI API key
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    OPENAI_TIMEOUT = 30  # seconds
    
    # Application Configuration
    APP_HOST = os.getenv('APP_HOST', '0.0.0.0')
    APP_PORT = int(os.getenv('APP_PORT', 5000))
    
    # File Upload Configuration
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'csv', 'txt'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    @staticmethod
    def init_app(app):
        """
        Initialize Flask app with configuration
        """
        pass

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing environment configuration"""
    DEBUG = True
    TESTING = True
    DATABASE_NAME = 'learning_activity_system_test'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
