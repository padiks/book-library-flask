# Book Library (Flask + mod_wsgi / waitress)

This is a Flask-based Book Library project that organizes books, volumes, and chapters in Markdown format and uses base templates for rendering.

### Features

- Organizes books into volumes and chapters using Markdown.
- Reusable base templates for header, footer, and hero section.
- App templates for home page, book listing, chapters, search results, sitemap, and login.
- Static folder for CSS, JS, and images.

### Requirements

- Python
- Flask
- mod_wsgi or Waitress (for production-like serving )
- Optional: `markdown` library for rendering chapters dynamically

### Notes

- Simplified for **learning Flask and mod_wsgi**.
- Uses **template inheritance** (`base.html` ? page templates) for easy customization.
- Can be extended later with **dynamic routes**, search, or login functionality.

### License

This project is intended for learning purposes.
