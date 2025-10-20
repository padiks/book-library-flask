# ------------------------------
# Import necessary modules
# ------------------------------
from flask import Flask, render_template, render_template_string, abort, Markup, url_for
from jinja2 import ChoiceLoader, FileSystemLoader
import markdown
import os
import glob
import re

# ------------------------------
# Initialize Flask app
# ------------------------------
# 'template_folder' specifies where to find HTML templates
# 'static_folder' specifies where to find static files (CSS, JS, images)
app = Flask(__name__, template_folder='app', static_folder='static')

# ------------------------------
# Customize Jinja2 template loader
# ------------------------------
# ChoiceLoader allows Jinja2 to search multiple folders in order
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
    return render_template('home.html', title=title, show_hero=False)

# ------------------------------
# Markdown rendering route with nested folder support
# ------------------------------
@app.route('/books/<path:md_path>')
def render_md(md_path):
    """
    Render a Markdown file or folder:
    - If the path points to a Markdown file, render it.
    - If the path points to a folder, try README.md inside the folder.
    - If no Markdown exists, list subfolders and Markdown files as links.
    - Converts line breaks in Markdown to <br /> for small paragraphs/lyrics.
    - Fixes URL slashes on Windows to use forward slashes for proper URLs.
    """
    folder_path = os.path.join('books', md_path)

    # Determine which file to render
    if os.path.isdir(folder_path):
        # Folder: use README.md if exists
        md_file = os.path.join(folder_path, 'README.md')
    else:
        # File: append .md if not present
        if not md_path.endswith('.md'):
            md_file = folder_path + '.md'
        else:
            md_file = folder_path

    # If file exists, render Markdown
    if os.path.exists(md_file):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # ------------------------------
        # Convert relative Markdown links (./something) to Flask URL
        # ------------------------------
        def replace_relative_links(match):
            link = match.group(1)
            if link.startswith('./'):
                # Convert relative path to full URL path
                full_path = os.path.join(md_path, link[2:])
                # Replace OS-specific backslashes with forward slashes
                full_path = full_path.replace('\\', '/')
                return f'({url_for("render_md", md_path=full_path)})'
            return f'({link})'

        content = re.sub(r'\((.*?)\)', replace_relative_links, content)

        # Convert Markdown to HTML with <br /> for line breaks
        html_content = markdown.markdown(content, extensions=['nl2br'])

        # Minimal template using base.html for consistent layout
        template = """
        {% extends "base.html" %}
        {% block content %}
            {{ content|safe }}
        {% endblock %}
        """

        # Dynamic title from filename or folder
        title = os.path.basename(md_file).replace('-', ' ').replace('.md', '').title()
        return render_template_string(template, content=Markup(html_content), title=title)

    # If folder exists but no README.md, list subfolders and Markdown files
    if os.path.isdir(folder_path):
        links = []

        # Add subfolders as links
        for d in sorted(os.listdir(folder_path)):
            d_path = os.path.join(folder_path, d)
            if os.path.isdir(d_path):
                links.append({
                    'name': d.replace('-', ' ').title(),
                    'url': url_for('render_md', md_path=f"{md_path}/{d}".replace('\\', '/'))
                })

        # Add Markdown files as links
        for f in sorted(glob.glob(os.path.join(folder_path, '*.md'))):
            name = os.path.splitext(os.path.basename(f))[0]
            links.append({
                'name': name.replace('-', ' ').title(),
                'url': url_for('render_md', md_path=f"{md_path}/{name}".replace('\\', '/'))
            })

        title = md_path.replace('-', ' ').title()
        return render_template('folder_index.html', title=title, links=links)

    # If neither file nor folder exists, abort with 404
    abort(404)

# ------------------------------
# Sitemap route
# ------------------------------
@app.route('/sitemap')
def sitemap():
    """
    Generates a sitemap of all books and chapters.
    Organized as:
    books → chapters/volumes
    """
    import glob

    books_dir = 'books'
    books_dict = {}

    # List all top-level folders (books)
    for book_folder in sorted(os.listdir(books_dir)):
        book_path = os.path.join(books_dir, book_folder)
        if os.path.isdir(book_path):
            chapters = []
            # List all folders and markdown files inside the book folder
            for item in sorted(os.listdir(book_path)):
                item_path = os.path.join(book_path, item)
                if os.path.isdir(item_path):
                    chapters.append({
                        'title': item.replace('-', ' ').title(),
                        'path': f"{book_folder}/{item}"
                    })
                elif item.endswith('.md') and item.lower() != 'readme.md':
                    chapters.append({
                        'title': item.replace('.md', '').replace('-', ' ').title(),
                        'path': f"{book_folder}/{item.replace('.md','')}"
                    })
            books_dict[book_folder.replace('-', ' ').title()] = chapters

    return render_template('sitemap.html', books=books_dict, title="Sitemap")	

# ------------------------------
# Search route
# ------------------------------
from flask import request

@app.route('/search')
def search():
    """
    Search all Markdown files in /books for a query string.
    Displays snippets and links to matching files.
    """
    query = request.args.get('q', '').strip()
    results = []

    if query:
        # Find all markdown files recursively under 'books'
        for root, dirs, files in os.walk('books'):
            for file in files:
                if file.endswith('.md'):
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                    except Exception:
                        continue  # Skip unreadable files

                    # Case-insensitive match
                    if re.search(re.escape(query), content, re.IGNORECASE):
                        # Get position of match and short snippet
                        pos = re.search(re.escape(query), content, re.IGNORECASE).start()
                        snippet_start = max(0, pos - 30)
                        snippet = content[snippet_start: pos + 150]

                        # Clean snippet of markdown and HTML
                        snippet = re.sub(r'[#>*_`~\-]+', '', snippet)
                        snippet = re.sub(r'<[^>]*>', '', snippet)
                        snippet = snippet.strip()

                        # Derive path and link (relative to /books/)
                        rel_path = os.path.relpath(full_path, 'books')
                        url_path = rel_path.replace('\\', '/').replace('.md', '')

                        # Book = first folder name
                        parts = url_path.split('/')
                        book = parts[0]
                        volume = parts[-1]

                        results.append({
                            'path': url_path,
                            'url': url_for('render_md', md_path=url_path),
                            'book': book,
                            'volume': volume,
                            'match_snippet': snippet + '...'
                        })

    # Render template
    return render_template('search.html', title="Search Results", query=query, results=results)

		
# ------------------------------
# 404 handler
# ------------------------------
@app.errorhandler(404)
def page_not_found(e):
    """
    Render custom 404 page if the requested route or file does not exist.
    """
    return render_template('404.html', title="Page Not Found"), 404

# ------------------------------
# Run Flask development server
# ------------------------------
if __name__ == '__main__':
    # host='0.0.0.0' → accessible from any network interface
    # port=4000 → the port where the app will run
    # debug=True → automatic reload on code changes and detailed error pages
    app.run(host='0.0.0.0', port=4000, debug=True)
