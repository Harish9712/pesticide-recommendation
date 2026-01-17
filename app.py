"""
Main Application for AI-Powered Crop Pest Classification System
Flask web application with farmer-friendly interface
"""

from flask import Flask, render_template, request, jsonify
from prediction_api import app
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application"""
    
    # Create necessary directories
    os.makedirs('model', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('uploads', exist_ok=True)
    
    return app

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)
