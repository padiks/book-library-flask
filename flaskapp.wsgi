import sys
import os

# Add your app folder to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask app (from app.py)
from app import app as application
