#!/usr/bin/env python3
"""
Install all dependencies for MCP Platform
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} - Failed")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False
    return True

def main():
    print("=" * 60)
    print("MCP Dependency Installer")
    print("=" * 60)
    
    # Check Python version
    print(f"\nPython version: {sys.version}")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required!")
        sys.exit(1)
    
    # Upgrade pip
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        print("\n⚠️  Failed to upgrade pip, continuing anyway...")
    
    # Install Python dependencies
    print("\n📦 Installing Python packages...")
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ requirements.txt not found!")
        sys.exit(1)
    
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing Python packages"):
        print("\n❌ Failed to install Python packages!")
        print("Try running: pip install -r requirements.txt")
        sys.exit(1)
    
    # Verify Python installations
    print("\n🔍 Verifying Python packages...")
    try:
        import fastapi
        import uvicorn
        import pydantic
        print("✅ Core packages verified")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        sys.exit(1)
    
    # Check Node.js
    print("\n🔍 Checking Node.js...")
    node_result = subprocess.run("node --version", shell=True, capture_output=True, text=True)
    if node_result.returncode == 0:
        print(f"✅ Node.js version: {node_result.stdout.strip()}")
    else:
        print("❌ Node.js not found! Please install from https://nodejs.org/")
        sys.exit(1)
    
    # Install Node packages
    ui_path = Path("ui")
    if ui_path.exists():
        os.chdir(ui_path)
        print("\n📦 Installing Node.js packages...")
        if not run_command("npm install", "Installing Node packages"):
            print("\n❌ Failed to install Node packages!")
            print("Try running: cd ui && npm install")
            sys.exit(1)
        os.chdir("..")
    else:
        print("⚠️  ui directory not found, skipping Node.js packages")
    
    print("\n" + "=" * 60)
    print("✅ All dependencies installed successfully!")
    print("=" * 60)
    print("\nYou can now run the application with:")
    print("  python launcher.py")
    print("or")
    print("  ./run_mcp.sh (Linux/Mac)")
    print("  run_mcp.bat (Windows)")

if __name__ == "__main__":
    main()