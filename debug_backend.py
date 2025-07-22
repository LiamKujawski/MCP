#!/usr/bin/env python3
"""Debug script to test backend with virtual environment"""

import os
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, os.getcwd())

# Check if venv exists
venv_path = Path("venv")
if venv_path.exists():
    print("✅ Virtual environment found")
    
    # Get the python executable from venv
    if sys.platform == "win32":
        python_exe = venv_path / "Scripts" / "python.exe"
    else:
        python_exe = venv_path / "bin" / "python"
    
    if python_exe.exists():
        print(f"✅ Python executable: {python_exe}")
        
        # Run a simple test
        import subprocess
        result = subprocess.run(
            [str(python_exe), "-c", "import fastapi, uvicorn; print('✅ Packages imported successfully')"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"❌ Import failed: {result.stderr}")
            
        # Try to start the backend
        print("\nStarting backend...")
        subprocess.run([str(python_exe), "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"])
    else:
        print(f"❌ Python executable not found at {python_exe}")
else:
    print("❌ Virtual environment not found. Run launcher.py first.")