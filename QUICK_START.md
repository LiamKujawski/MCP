# 🚀 MCP Quick Start Guide

Welcome to MCP! This guide will help you get started in just a few minutes.

## 📋 Prerequisites

Before starting, make sure you have:
- **Python 3.8+** installed ([Download Python](https://www.python.org/downloads/))
- **Node.js 18+** installed ([Download Node.js](https://nodejs.org/))

## 🎯 One-Click Start

### Windows Users:
1. **Double-click** `run_mcp.bat`
2. The application will automatically:
   - Create a virtual environment (first time only)
   - Install all dependencies in the virtual environment
   - Start the backend server
   - Start the frontend server
   - Open your browser to the MCP Control Center

### Mac/Linux Users:
1. **Double-click** `run_mcp.sh` or run `./run_mcp.sh` in terminal
2. The application will automatically:
   - Create a virtual environment (first time only)
   - Install all dependencies in the virtual environment
   - Start the backend server
   - Start the frontend server
   - Open your browser to the MCP Control Center

### Alternative Method:
Run this command in your terminal:
```bash
python launcher.py
```

## 🎮 Using MCP Control Center

Once MCP is running, you'll see the Control Center in your browser at http://localhost:3000

### Main Features:

#### 1. **Dashboard (Overview Tab)**
- See all your research topics
- Monitor active agents
- Check pipeline status
- Quick action buttons for common tasks

#### 2. **Research Tab**
- **View existing research topics**: See all your research organized by topic
- **Create new topics**: 
  1. Click "Create New Research Topic"
  2. Enter a name (e.g., "AI Safety Research")
  3. Add a description
  4. Write your initial content in Markdown format
  5. Click "Create Research Topic"

#### 3. **Pipeline Tab**
- **Run the full pipeline**: Click "Start Pipeline" to process all research
- **Process specific topic**: Select a topic from the dropdown, then click "Start Pipeline"
- **Monitor progress**: Watch real-time progress through the 5 phases:
  - Research Collection
  - Synthesis
  - Experiment
  - Deploy
  - Optimize

#### 4. **Agents Tab**
- View all available AI agents
- See their capabilities and status

#### 5. **Settings Tab**
- System information
- Quick links to documentation
- API configuration info

## 🔑 API Keys (Optional)

To enable AI features, add your API keys to the `.env` file:
1. Open the `.env` file in a text editor
2. Replace the placeholder values:
   ```
   OPENAI_API_KEY=your-actual-openai-key
   ANTHROPIC_API_KEY=your-actual-anthropic-key
   ```
3. Save the file and restart MCP

## 🛑 Stopping MCP

To stop the application:
- Press `Ctrl+C` in the terminal/command prompt
- Or close the terminal window

## 🆘 Troubleshooting

### Application won't start:
1. Make sure Python and Node.js are installed
2. Try running `python --version` and `node --version` to verify
3. If on Mac/Linux, make sure the script is executable: `chmod +x run_mcp.sh`

### "Backend API failed to start" error:
This is often due to Python environment or import issues. Try these solutions:

#### Solution 1: ModuleNotFoundError: No module named 'synthesized_agent'
This happens when Python can't find the modules. Fix:
```bash
# On Windows:
set PYTHONPATH=%CD%
python launcher.py

# On Mac/Linux:
export PYTHONPATH=$PWD
python3 launcher.py
```

#### Solution 2: Manual Backend Start (Windows)
Use the simple backend starter:
```bash
start_backend.bat
```

#### Solution 3: Manual Dependency Installation
```bash
# Install Python packages manually
python -m pip install -r requirements.txt

# Then run the launcher
python launcher.py
```

#### Solution 4: Use a Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the launcher
python launcher.py
```

### Browser doesn't open automatically:
- Manually open http://localhost:3000

### Port already in use:
- Another application is using port 3000 or 8000
- Stop the other application or restart your computer

### Dependencies fail to install:
- Make sure you have an internet connection
- Try running as administrator (Windows) or with sudo (Mac/Linux)
- On newer Linux systems, you may need to add `--break-system-packages` flag

## 📚 Next Steps

1. **Create your first research topic** in the Research tab
2. **Run the pipeline** to see MCP in action
3. **Explore the API** at http://localhost:8000/docs
4. **Read the full documentation** in the repository

## 🎉 That's it!

You're now ready to use MCP! The platform handles all the complex operations behind the scenes, so you can focus on your research and experiments.

For more detailed information, see the main [README.md](README.md) file.