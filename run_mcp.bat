@echo off
REM MCP One-Click Runner for Windows

echo ====================================
echo      Starting MCP Platform
echo ====================================

REM Run the Python launcher (it will handle venv setup)
python launcher.py
if errorlevel 1 (
    REM Try with python3 if python fails
    python3 launcher.py
)
pause