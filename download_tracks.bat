@echo off
REM ───────────── OPTIONAL: activate your virtual-env ─────────────
REM comment out the next line if you’re using the system-wide Python
call "%~dp0.venv\Scripts\activate.bat"

REM ───────────── Run the Python driver script ─────────────
python "%~dp0src\spotdl_script.py"

REM Keeps the window open so you can read any messages
pause
