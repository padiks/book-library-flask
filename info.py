from flask import Flask, render_template_string  # Flask core and quick template rendering
import sys      # To access Python version and executable path
import platform # To get OS and system information
import flask    # To get Flask version

# For safely checking package versions
try:
    import pkg_resources  # Part of setuptools, allows querying installed package versions
except ImportError:
    pkg_resources = None  # If setuptools not installed, we handle it gracefully

# ------------------------------
# Initialize Flask
# ------------------------------
app = Flask(__name__)  # Create Flask app instance

# ------------------------------
# Info route
# ------------------------------
@app.route('/info')  # Defines a URL route /info
def info():
    """
    Display simplified Python info similar to phpinfo().
    Uses render_template_string for simplicity (no separate template file needed).
    """

    # ------------------------------
    # Safely get Waitress version
    # ------------------------------
    waitress_version = "Not installed"  # Default value if Waitress not present
    try:
        import waitress  # Try importing Waitress
        if pkg_resources:
            # Use pkg_resources to get installed version of Waitress
            waitress_version = pkg_resources.get_distribution("waitress").version
        else:
            # Fallback if pkg_resources is not available
            waitress_version = "Waitress installed (version unknown)"
    except ImportError:
        # Waitress is not installed
        waitress_version = "Waitress not installed"
    except Exception:
        # Any other error retrieving version
        waitress_version = "Waitress installed (version unknown)"

    # ------------------------------
    # HTML template string
    # ------------------------------
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Python Info</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 60%; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>Python & Flask Info</h1>
        <table>
            <tr><th>Item</th><th>Value</th></tr>
            <tr><td>Python Version</td><td>{{ python_version }}</td></tr>
            <tr><td>Flask Version</td><td>{{ flask_version }}</td></tr>
            <tr><td>Waitress Version</td><td>{{ waitress_version }}</td></tr>
            <tr><td>Platform</td><td>{{ platform }}</td></tr>
            <tr><td>Executable</td><td>{{ executable }}</td></tr>
        </table>
    </body>
    </html>
    """

    # ------------------------------
    # Render the template with dynamic values
    # ------------------------------
    return render_template_string(html,
                                  python_version=sys.version,      # Full Python version string
                                  flask_version=flask.__version__, # Flask version installed
                                  waitress_version=waitress_version, # Waitress version or fallback
                                  platform=platform.platform(),    # OS platform info
                                  executable=sys.executable)       # Python executable path

# ------------------------------
# Run Flask development server
# ------------------------------
if __name__ == '__main__':
    print("Visit http://127.0.0.1:4000/info")  # Inform user where to access the page
    app.run(host='0.0.0.0', port=4000, debug=True)  # Start dev server with debug mode
