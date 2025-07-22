#!/usr/bin/env python3
"""
Test script to diagnose backend startup issues
"""

import subprocess
import sys
import time

print("Testing MCP Backend Startup...")
print("=" * 50)

# Test 1: Check if src/main.py exists
try:
    with open("src/main.py", "r") as f:
        print("✅ src/main.py found")
except FileNotFoundError:
    print("❌ src/main.py not found!")
    sys.exit(1)

# Test 2: Try importing the app
print("\nTesting imports...")
try:
    from src.main import app
    print("✅ Successfully imported FastAPI app")
except Exception as e:
    print(f"❌ Import error: {e}")
    print("\nTrying to fix common issues...")
    
    # Check if we need to add current directory to Python path
    import os
    sys.path.insert(0, os.getcwd())
    
    try:
        from src.main import app
        print("✅ Fixed by adding current directory to Python path")
    except Exception as e2:
        print(f"❌ Still failing: {e2}")
        sys.exit(1)

# Test 3: Try running uvicorn directly
print("\nTesting uvicorn startup...")
print("Running: python -m uvicorn src.main:app --host 127.0.0.1 --port 8001")
print("(Using port 8001 to avoid conflicts)")
print("-" * 50)

process = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", "8001"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    universal_newlines=True
)

# Read output for 5 seconds
start_time = time.time()
while time.time() - start_time < 5:
    line = process.stdout.readline()
    if line:
        print(line.strip())
    if "Application startup complete" in line:
        print("\n✅ Backend started successfully!")
        break
    if "ERROR" in line or "error" in line:
        print(f"\n❌ Error detected!")

# Clean up
process.terminate()
print("\nTest complete. Check the output above for any errors.")