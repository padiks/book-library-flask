### Project Structure

```
flibrary/                    # Cross-platform Flask project (Windows and Debian, runs on Apache, Waitress, or console)
├── app.py                   # Entry point for production (Apache/Waitress); defines the `application` object
├── config.py                # Configuration file for development and production; stores centralized settings
├── apps/                    # Core application modules (shared code, routing, etc.)
│   ├── __init__.py          # Initializes the Flask app, registers blueprints, and sets the global 404 handler
│   ├── routes/              # Application route definitions
│   │   ├── __init__.py      # Imports all route modules (home, books, etc.)
│   │   ├── home.py          # Home page routes
│   │   ├── about.py         # About page routes
│   │   ├── books.py         # Books, volumes, and chapters routes
│   │   ├── auth.py          # Authentication routes (login/logout)
│   │   ├── sitemap.py       # Sitemap blueprint
│   │   └── search.py        # Search blueprint
│   ├── models/              # Optional: database models or ORM classes
│   │   ├── __init__.py
│   │   └── user.py
│   ├── utils/               # Optional: helper functions or shared utilities
│   │   ├── __init__.py
│   │   └── markdown.py
│   └── services/            # Optional: business logic or API integrations
│       ├── __init__.py
│       └── email_service.py
├── templates/               # HTML templates
│   ├── base.html            # Base layout template
│   ├── 404.html             # 404 error page
│   ├── home.html            # Home page template
│   ├── about.html           # About page template
│   ├── books/               # Templates related to books
│   │   └── index.html       # Books listing template
│   └── auth/                # Authentication templates
│       └── login.html       # Login page template
├── books/                   # Storage for all books (in Markdown format)
│   └── lorem-ipsum/         # Example book (one folder per book)
│       ├── README.md        # Root README for the book
│       └── volume-1/        # Subfolder for volumes
│           ├── README.md    # Volume README
│           └── chapter-1.md # Chapter file
├── static/                  # Static assets (CSS, JavaScript, images)
│   ├── css/                 # CSS files
│   │   ├── paper.css        # PaperCSS — the less formal CSS framework
│   │   └── style.css        # Custom style file
│   ├── js/                  # JavaScript files
│   │   └── theme.js         # Dark/light mode toggle script
│   └── images/              # Image assets
│       ├── geometry2.png    # Background image
│       └── favicon.ico      # Favicon
├── data/                    # Data directory for SQLite or JSON storage
│   └── users.db             # SQLite database for the user authentication system
├── flaskapp.wsgi            # WSGI entry point for Apache/mod_wsgi (used on Debian deployment)
└── venv/                    # Virtual environment (excluded from version control)
```