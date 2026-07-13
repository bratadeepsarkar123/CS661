@echo off
cd /d "%~dp0..\dashboard-light"
echo Serving dashboard-light on http://127.0.0.1:8088/
echo Close this window or press Ctrl+C to stop.
python -m http.server 8088 --bind 127.0.0.1
pause
