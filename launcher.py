#!/usr/bin/env python3
"""
MCP One-Click Launcher
A simple launcher that starts the entire MCP platform with a single click.
No technical knowledge required!
"""

import os
import sys
import subprocess
import time
import webbrowser
import socket
import signal
import platform
from pathlib import Path
import threading
import json

class MCPLauncher:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.workspace_path = Path(__file__).parent.absolute()
        self.ui_path = self.workspace_path / "ui"
        self.backend_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:3000"
        
    def is_port_open(self, port):
        """Check if a port is available"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result == 0
        
    def wait_for_service(self, port, service_name, timeout=60):
        """Wait for a service to become available"""
        print(f"⏳ Waiting for {service_name} to start...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.is_port_open(port):
                print(f"✅ {service_name} is ready!")
                return True
            time.sleep(1)
        print(f"❌ {service_name} failed to start within {timeout} seconds")
        return False
        
    def check_dependencies(self):
        """Check if all required dependencies are installed"""
        print("🔍 Checking dependencies...")
        
        # Check Python
        try:
            python_version = subprocess.check_output([sys.executable, "--version"], stderr=subprocess.STDOUT).decode().strip()
            print(f"✅ Python: {python_version}")
        except Exception as e:
            print(f"❌ Python not found: {e}")
            return False
            
        # Check Node.js
        try:
            node_version = subprocess.check_output(["node", "--version"], stderr=subprocess.STDOUT).decode().strip()
            print(f"✅ Node.js: {node_version}")
        except Exception:
            print("❌ Node.js not found. Please install Node.js from https://nodejs.org/")
            return False
            
        # Check if Python packages are installed
        try:
            import fastapi
            import uvicorn
            print("✅ Python packages installed")
        except ImportError:
            print("📦 Installing Python packages...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            
        # Check if Node packages are installed
        if not (self.ui_path / "node_modules").exists():
            print("📦 Installing Node.js packages...")
            subprocess.run(["npm", "install"], cwd=self.ui_path, check=True)
            
        return True
        
    def setup_environment(self):
        """Set up environment variables"""
        env = os.environ.copy()
        
        # Create .env file if it doesn't exist
        env_file = self.workspace_path / ".env"
        if not env_file.exists():
            print("📝 Creating default .env file...")
            default_env = """# MCP Environment Configuration
DATABASE_URL=sqlite:///./mcp.db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# Optional: Add your API keys above to enable AI features
"""
            env_file.write_text(default_env)
            print("⚠️  Please add your API keys to the .env file for full functionality")
            
        # Load .env file
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if line.strip() and not line.startswith('#') and '=' in line:
                        key, value = line.strip().split('=', 1)
                        env[key] = value
                        
        return env
        
    def start_backend(self, env):
        """Start the FastAPI backend"""
        print("\n🚀 Starting backend server...")
        
        # Start uvicorn
        self.backend_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Monitor backend output in a thread
        def monitor_backend():
            for line in self.backend_process.stdout:
                if "Application startup complete" in line:
                    print("✅ Backend started successfully!")
        
        threading.Thread(target=monitor_backend, daemon=True).start()
        
    def start_frontend(self, env):
        """Start the Next.js frontend"""
        print("\n🚀 Starting frontend server...")
        
        # Start Next.js dev server
        self.frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=self.ui_path,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Monitor frontend output in a thread
        def monitor_frontend():
            for line in self.frontend_process.stdout:
                if "ready" in line.lower():
                    print("✅ Frontend started successfully!")
        
        threading.Thread(target=monitor_frontend, daemon=True).start()
        
    def open_browser(self):
        """Open the application in the default browser"""
        print(f"\n🌐 Opening MCP in your browser at {self.frontend_url}")
        time.sleep(2)  # Give the frontend a moment to fully initialize
        webbrowser.open(self.frontend_url)
        
    def create_desktop_shortcut(self):
        """Create a desktop shortcut for easy access"""
        system = platform.system()
        
        if system == "Windows":
            # Create Windows shortcut
            desktop = Path.home() / "Desktop"
            shortcut_path = desktop / "MCP Platform.bat"
            shortcut_content = f"""@echo off
cd /d "{self.workspace_path}"
python launcher.py
"""
            shortcut_path.write_text(shortcut_content)
            print(f"✅ Desktop shortcut created: {shortcut_path}")
            
        elif system == "Darwin":  # macOS
            # Create macOS app
            print("📝 To create a macOS app, you can use Automator to run this script")
            
        elif system == "Linux":
            # Create Linux desktop entry
            desktop = Path.home() / "Desktop"
            shortcut_path = desktop / "mcp-platform.desktop"
            shortcut_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=MCP Platform
Comment=Multi-Agent Collaborative Platform
Exec=python3 {self.workspace_path}/launcher.py
Icon={self.workspace_path}/ui/public/favicon.ico
Terminal=false
Categories=Development;
"""
            shortcut_path.write_text(shortcut_content)
            shortcut_path.chmod(0o755)
            print(f"✅ Desktop shortcut created: {shortcut_path}")
            
    def cleanup(self, signum=None, frame=None):
        """Clean up processes on exit"""
        print("\n🛑 Shutting down MCP...")
        
        if self.backend_process:
            self.backend_process.terminate()
            self.backend_process.wait()
            print("✅ Backend stopped")
            
        if self.frontend_process:
            self.frontend_process.terminate()
            self.frontend_process.wait()
            print("✅ Frontend stopped")
            
        print("👋 MCP shut down successfully")
        sys.exit(0)
        
    def run(self):
        """Main launcher function"""
        print("""
╔════════════════════════════════════════════╗
║         MCP - One-Click Launcher           ║
║    Multi-Agent Collaborative Platform      ║
╚════════════════════════════════════════════╝
        """)
        
        # Set up signal handlers for clean shutdown
        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)
        
        # Check dependencies
        if not self.check_dependencies():
            print("\n❌ Please install missing dependencies and try again.")
            input("Press Enter to exit...")
            return
            
        # Set up environment
        env = self.setup_environment()
        
        # Start services
        self.start_backend(env)
        if not self.wait_for_service(8000, "Backend API"):
            self.cleanup()
            return
            
        self.start_frontend(env)
        if not self.wait_for_service(3000, "Frontend UI"):
            self.cleanup()
            return
            
        # Open browser
        self.open_browser()
        
        # Create desktop shortcut on first run
        first_run_flag = self.workspace_path / ".first_run_complete"
        if not first_run_flag.exists():
            self.create_desktop_shortcut()
            first_run_flag.touch()
        
        print("""
╔════════════════════════════════════════════╗
║            MCP is now running!             ║
║                                            ║
║  Frontend: http://localhost:3000           ║
║  Backend:  http://localhost:8000           ║
║  API Docs: http://localhost:8000/docs      ║
║                                            ║
║  Press Ctrl+C to stop the application      ║
╚════════════════════════════════════════════╝
        """)
        
        # Keep the script running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.cleanup()

if __name__ == "__main__":
    launcher = MCPLauncher()
    launcher.run()