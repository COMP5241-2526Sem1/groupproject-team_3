"""
Vercel Serverless Function Entry Point
This file is required for Vercel deployment
"""

import sys
import os

# Add the parent directory to the path so we can import from the project
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from flask import Flask, Response
import traceback

# Try to create the Flask app; if initialization fails (e.g. DB connection),
# create a minimal Flask app that returns a 500 so the Serverless function
# doesn't crash on import and we can inspect logs.
try:
    app = create_app('production')
    application = app
except Exception as e:
    # Log the traceback to stdout/stderr (captured by Vercel logs)
    print("ERROR: Failed to initialize Flask app:")
    traceback.print_exc()

    # Create a minimal fallback Flask app that returns 500 for all requests
    fallback = Flask("fallback_app")

    @fallback.route("/", defaults={"path": ""})
    @fallback.route("/<path:path>")
    def _fail(path=""):
        body = ("Application failed to initialize. Check logs for details.\n"
                f"Error: {str(e)}")
        return Response(body, status=500, mimetype='text/plain')

    application = fallback

# For local testing
if __name__ == '__main__':
    application.run()
