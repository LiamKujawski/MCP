@echo off
REM Simple backend starter for MCP

echo Starting MCP Backend...
echo.

REM Add current directory to PYTHONPATH
set PYTHONPATH=%CD%;%PYTHONPATH%

REM Check if venv exists
if exist venv\Scripts\python.exe (
    echo Using virtual environment...
    venv\Scripts\python.exe -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
) else (
    echo Using system Python...
    python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
)

pause
