Listen 4000

# === Flask app configuration ===
# Load mod_wsgi (adjust the path to your installed Python version)
LoadModule wsgi_module "C:/Users/[NAME]/AppData/Local/Programs/Python/[VERSION]/Lib/site-packages/mod_wsgi/server/mod_wsgi.[VERSION].pyd"

<VirtualHost *:4000>
    ServerName flask.local
    DocumentRoot "C:/laragon/www/tools/flaskapp"
    WSGIScriptAlias / "C:/laragon/www/tools/flaskapp/flaskapp.wsgi"

    <Directory "C:/laragon/www/tools/flaskapp">
        Require all granted
    </Directory>
</VirtualHost>