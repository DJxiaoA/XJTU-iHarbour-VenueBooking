@echo off
setlocal
cd /d "%~dp0"
set "PYTHON_EXE=python"
set "WAIT_SECONDS=180"
"%PYTHON_EXE%" main.py
timeout /t %WAIT_SECONDS% /nobreak
"%PYTHON_EXE%" write_to_calendar.py
