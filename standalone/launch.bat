@echo off
cd /d "%~dp0"
if not exist out mkdir out
if not exist work mkdir work
echo AZbot Local — 127.0.0.1:7747
echo Slingshot Prep only. No upload.
start "" "http://127.0.0.1:7747"
python app\server.py
if errorlevel 1 py -3 app\server.py
pause
