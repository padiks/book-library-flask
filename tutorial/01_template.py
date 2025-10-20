# ------------------------------------------------------------
# File: tutorial/01_template.py
# Description:
# This is the basic Flask application for the Book Library project.
# It sets up the Flask app, configures the template loader to check
# both 'app' and 'templates' folders, and defines a single home
# route ('/') that renders 'home.html' with a dynamic title.
# This version does NOT handle Markdown files; it's meant for
# learning Flask and template rendering basics.
# ------------------------------------------------------------

# ------------------------------
# Import necessary modules
# ------------------------------
from flask import Flask, render_template  # Flask core and template rendering
from jinja2 import ChoiceLoader, FileSystemLoader  # For custom template loading

# ------------------------------
# Initialize Flask app
# ------------------------------
# 'template_folder' tells Flask where to look for page templates (default is 'templates')
# 'static_folder' tells Flask where to look for static files like CSS, JS, images
app = Flask(__name__, template_folder='app', static_folder='static')

# ------------------------------
# Customize Jinja2 template loader
# ------------------------------
# By default, Flask looks for templates in 'template_folder' only
# ChoiceLoader allows Jinja2 to search multiple folders in order
app.jinja_loader = ChoiceLoader([
    FileSystemLoader('app'),       # First, search for templates inside 'app' folder
    FileSystemLoader('templates'), # Then, search inside 'templates' folder
])

# ------------------------------
# Define the home route
# ------------------------------
@app.route('/')  # The URL path '/' will trigger this function
def home():
    """
    Home page route.
    Renders 'home.html' with a dynamic title and optional hero section.
    """
    title = "Raito Noberu Toshokan"  # Dynamic page title
    # 'show_hero=True' is passed to the template to conditionally render hero section
    return render_template('home.html', title=title, show_hero=True)

# ------------------------------
# Run the Flask development server
# ------------------------------
if __name__ == '__main__':
    # Host '0.0.0.0' makes it accessible from any network interface
    # Port 4000 is where the app will run
    # 'debug=True' enables automatic reload on code changes and shows debug info
    app.run(host='0.0.0.0', port=4000, debug=True)
