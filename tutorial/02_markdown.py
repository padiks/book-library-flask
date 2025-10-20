# ------------------------------------------------------------
# File: tutorial/02_markdown.py
# Description:
# This Flask application extends the basic home page by adding
# a route to render Markdown files directly.
# - '/books/<path:md_path>' renders a specific Markdown file or
#   the README.md inside a folder automatically.
# - Line breaks in Markdown are converted to <br /> for proper
#   display of lyrics or small paragraphs.
# - Uses Jinja2 template inheritance (base.html) for consistent layout.
# - Dynamic page titles are generated from the Markdown filename.
# This version is ideal for a small Book Library or lyrics viewer.
# ------------------------------------------------------------

# ------------------------------
# Import necessary modules
# ------------------------------
from flask import Flask, render_template, render_template_string, abort, Markup
from jinja2 import ChoiceLoader, FileSystemLoader
import markdown
import os

# ------------------------------
# Initialize Flask app
# ------------------------------
# 'template_folder' specifies where to find HTML templates
# 'static_folder' specifies where to find static files (CSS, JS, images)
app = Flask(__name__, template_folder='app', static_folder='static')

# ------------------------------
# Customize Jinja2 template loader
# ------------------------------
# By default, Flask looks for templates only in 'template_folder'
# ChoiceLoader allows searching multiple folders in order
app.jinja_loader = ChoiceLoader([
    FileSystemLoader('app'),       # First, search in 'app' folder
    FileSystemLoader('templates'), # Then, search in 'templates' folder
])

# ------------------------------
# Homepage route
# ------------------------------
@app.route('/')  # Triggered when accessing '/'
def home():
    """
    Home page route.
    Renders 'home.html' with a dynamic title and optional hero section.
    """
    title = "ぷらいべーと らいぶらり"  # Dynamic page title
    # 'show_hero=True/False' can be used in template to display hero section conditionally
    return render_template('home.html', title=title, show_hero=True)

# ------------------------------
# Markdown rendering route
# ------------------------------
@app.route('/books/<path:md_path>')
def render_md(md_path):
    """
    Render a Markdown file directly.
    - If link gives exact filename, render that file.
    - If link points to a folder, render README.md inside that folder.
    - Converts line breaks in Markdown to <br /> for lyrics or small paragraphs.
    """
    folder_path = os.path.join('books', md_path)

    # Determine which file to render
    if os.path.isdir(folder_path):
        # If md_path is a folder, use README.md inside it
        md_file = os.path.join(folder_path, 'README.md')
    else:
        # If md_path is a file name without .md, append .md
        if not md_path.endswith('.md'):
            md_file = folder_path + '.md'
        else:
            md_file = folder_path

    # Abort with 404 if the file does not exist
    if not os.path.exists(md_file):
        abort(404)

    # Read Markdown content and convert to HTML with <br /> for line breaks
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
        html_content = markdown.markdown(content, extensions=['nl2br'])

    # Minimal template using base.html for consistent layout
    template = """
    {% extends "base.html" %}
    {% block content %}
        {{ content|safe }}
    {% endblock %}
    """

    # Generate a dynamic title from the Markdown filename
    title = os.path.basename(md_file).replace('-', ' ').replace('.md', '').title()

    # Render the template with Markdown content
    return render_template_string(template, content=Markup(html_content), title=title)

# ------------------------------
# Run Flask development server
# ------------------------------
if __name__ == '__main__':
    # host='0.0.0.0' → accessible from any network interface
    # port=4000 → the port where the app will run
    # debug=True → automatic reload on code changes and detailed error pages
    app.run(host='0.0.0.0', port=4000, debug=True)
