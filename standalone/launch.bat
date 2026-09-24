@echo off
cd /d "%~dp0"
if not exist out mkdir out
if not exist work mkdir work
echo Starting AZbot Local.
start "" "http://127.0.0.1:7747"
python app\server.py
if errorlevel 1 py -3 app\server.py
pause
