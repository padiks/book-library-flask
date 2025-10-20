@echo off
REM ----------------------------------
REM Run Flask app using Waitress
REM ----------------------------------

REM Navigate to project folder
cd /d C:\laragon\www\tools\flaskapp

REM Start Waitress and log output
REM waitress-serve --listen=0.0.0.0:4000 app:app > server.log 2>&1
start /B waitress-serve --listen=0.0.0.0:4000 app:app

echo Flask + Waitress server started on port 4000!
echo Check server.log for any errors.
pause
