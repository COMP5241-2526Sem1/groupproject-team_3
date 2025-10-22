"""
Vercel Serverless Function Entry Point
This file is required for Vercel deployment
"""

import sys
import os

# Add the parent directory to the path so we can import from the project
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

# Create the Flask app instance
app = create_app('production')

# Vercel requires the app to be named 'app' or exported as 'application'
# This is the WSGI application that Vercel will use
application = app

# For local testing
if __name__ == '__main__':
    app.run()
