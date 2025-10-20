@echo off
REM ----------------------------------
REM Batch file to run Flask app
REM ----------------------------------

REM Navigate to the project folder
cd /d C:\laragon\www\tools\flaskapp

REM Optional: pause before running (for debugging)
REM pause

REM Run the Flask app with Python
python app.py

REM Keep the console open after the app stops
pause
