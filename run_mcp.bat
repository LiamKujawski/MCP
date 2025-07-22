@echo off
REM MCP One-Click Runner for Windows

echo ====================================
echo      Starting MCP Platform
echo ====================================

REM Set PYTHONPATH to include current directory
set PYTHONPATH=%CD%;%PYTHONPATH%

REM Run the Python launcher (it will handle venv setup)
python launcher.py
if errorlevel 1 (
    REM Try with python3 if python fails
    python3 launcher.py
    if errorlevel 1 (
        echo.
        echo Failed to start MCP. Common issues:
        echo - Python not installed or not in PATH
        echo - Missing dependencies
        echo.
        echo Try running: python -m pip install -r requirements.txt
        echo Or use: start_backend.bat to test the backend alone
    )
)
pause