from flask import Flask, render_template_string

# Create Flask app instance
app = Flask(__name__)

# Define a single route
@app.route('/')
def hello():
    # Simple HTML output
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Hello World</title>
    </head>
    <body>
        <h1>Hello World!</h1>
        <p>Flask is working under Apache + mod_wsgi.</p>
    </body>
    </html>
    """
    return render_template_string(html)
