# ==============================
# Book Library (Flask + mod_wsgi)
# Library app with login, markdown books, search, and sitemap.
# Developed and tested on Windows with Apache + mod_wsgi.
# Should be portable to other OS (Linux, Debian) with proper Flask & WSGI setup.
# ==============================

# ==============================
# app.py - Flask Library App with Global Login
# ==============================
import os
import glob
import re
from flask import Flask, render_template, render_template_string, abort, Markup, url_for, request, redirect, make_response
from jinja2 import ChoiceLoader, FileSystemLoader
import markdown

# ==============================
# LOGIN SETTINGS
# ==============================
PASSWORD_ENABLED = True
PASSWORD = 'q'  # Your site password

# ------------------------------
# Compute absolute paths
# ------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOKS_DIR = os.path.join(BASE_DIR, 'books')
TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, 'app'),
    os.path.join(BASE_DIR, 'templates')
]
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# ------------------------------
# Initialize Flask app
# ------------------------------
app = Flask(__name__, template_folder=TEMPLATE_DIRS[0], static_folder=STATIC_DIR)
app.jinja_loader = ChoiceLoader([FileSystemLoader(d) for d in TEMPLATE_DIRS])

# ==============================
# GLOBAL LOGIN ENFORCEMENT
# ==============================
@app.before_request
def require_login():
    # Allow login/logout and static files without a cookie
    if not PASSWORD_ENABLED:
        return
    allowed_endpoints = ['login', 'logout', 'static']
    if request.endpoint not in allowed_endpoints:
        access_token = request.cookies.get('access_token')
        if access_token != 'ok':
            return redirect(url_for('login'))

# ==============================
# Inject login status into all templates
# ==============================
@app.context_processor
def inject_login_status():
    access_token = request.cookies.get('access_token')
    return dict(is_logged_in=(access_token == 'ok'))

# ==============================
# LOGIN ROUTES
# ==============================
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if not PASSWORD_ENABLED:
        resp = make_response(redirect(url_for('home')))
        resp.set_cookie('access_token', 'ok', max_age=3600, path='/')
        return resp

    if request.method == 'POST':
        pw = request.form.get('password', '')
        if pw == PASSWORD:
            resp = make_response(redirect(url_for('home')))
            resp.set_cookie('access_token', 'ok', max_age=3600, path='/')
            return resp
        else:
            error = 'Wrong password!'

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('access_token', '', expires=0, path='/')
    return resp

# ==============================
# HOMEPAGE ROUTE
# ==============================
@app.route('/')
def home():
    title = "ぷらいべーと らいぶらり"
    return render_template('home.html', title=title, show_hero=False)

# ==============================
# MARKDOWN RENDERING ROUTE
# ==============================
@app.route('/books/<path:md_path>')
def render_md(md_path):
    folder_path = os.path.join(BOOKS_DIR, md_path)

    if os.path.isdir(folder_path):
        md_file = os.path.join(folder_path, 'README.md')
    else:
        md_file = folder_path if md_path.endswith('.md') else folder_path + '.md'

    if os.path.exists(md_file):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        def replace_relative_links(match):
            link = match.group(1)
            if link.startswith('./'):
                full_path = os.path.join(md_path, link[2:]).replace('\\', '/')
                return f'({url_for("render_md", md_path=full_path)})'
            return f'({link})'

        content = re.sub(r'\((.*?)\)', replace_relative_links, content)
        html_content = markdown.markdown(content, extensions=['nl2br'])

        template = """
        {% extends "base.html" %}
        {% block content %}
            {{ content|safe }}
        {% endblock %}
        """
        title = os.path.basename(md_file).replace('-', ' ').replace('.md', '').title()
        return render_template_string(template, content=Markup(html_content), title=title)

    # Folder exists but no README.md - list contents
    if os.path.isdir(folder_path):
        links = []
        for d in sorted(os.listdir(folder_path)):
            d_path = os.path.join(folder_path, d)
            if os.path.isdir(d_path):
                links.append({
                    'name': d.replace('-', ' ').title(),
                    'url': url_for('render_md', md_path=f"{md_path}/{d}".replace('\\', '/'))
                })
        for f in sorted(glob.glob(os.path.join(folder_path, '*.md'))):
            name = os.path.splitext(os.path.basename(f))[0]
            links.append({
                'name': name.replace('-', ' ').title(),
                'url': url_for('render_md', md_path=f"{md_path}/{name}".replace('\\', '/'))
            })
        title = md_path.replace('-', ' ').title()
        return render_template('folder_index.html', title=title, links=links)

    abort(404)

# ==============================
# SITEMAP ROUTE
# ==============================
@app.route('/sitemap')
def sitemap():
    books_dict = {}
    for book_folder in sorted(os.listdir(BOOKS_DIR)):
        book_path = os.path.join(BOOKS_DIR, book_folder)
        if os.path.isdir(book_path):
            chapters = []
            for item in sorted(os.listdir(book_path)):
                item_path = os.path.join(book_path, item)
                if os.path.isdir(item_path):
                    chapters.append({'title': item.replace('-', ' ').title(), 'path': f"{book_folder}/{item}"})
                elif item.endswith('.md') and item.lower() != 'readme.md':
                    chapters.append({'title': item.replace('.md', '').replace('-', ' ').title(),
                                     'path': f"{book_folder}/{item.replace('.md','')}"} )
            books_dict[book_folder.replace('-', ' ').title()] = chapters
    return render_template('sitemap.html', books=books_dict, title="Sitemap")

# ==============================
# SEARCH ROUTE
# ==============================
@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    results = []

    if query:
        for root, dirs, files in os.walk(BOOKS_DIR):
            for file in files:
                if file.endswith('.md'):
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                    except Exception:
                        continue
                    if re.search(re.escape(query), content, re.IGNORECASE):
                        pos = re.search(re.escape(query), content, re.IGNORECASE).start()
                        snippet_start = max(0, pos - 30)
                        snippet = content[snippet_start: pos + 150]
                        snippet = re.sub(r'[#>*_`~\-]+', '', snippet)
                        snippet = re.sub(r'<[^>]*>', '', snippet).strip()
                        rel_path = os.path.relpath(full_path, BOOKS_DIR)
                        url_path = rel_path.replace('\\', '/').replace('.md', '')
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
    return render_template('search.html', title="Search Results", query=query, results=results)

# ==============================
# CUSTOM 404 HANDLER
# ==============================
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title="Page Not Found"), 404

# ==============================
# RUN DEVELOPMENT SERVER
# ==============================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)

# ==============================
# EXPOSE WSGI APPLICATION FOR APACHE + MOD_WSGI
# ==============================
application = app
