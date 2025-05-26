@echo off
call "%~dp0.venv\Scripts\activate.bat"
python "%~dp0src\extract_stems.py"
pause
