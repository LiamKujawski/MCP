#!/bin/bash
# MCP One-Click Runner for Unix-based systems

echo "╔════════════════════════════════════════════╗"
echo "║         Starting MCP Platform              ║"
echo "╚════════════════════════════════════════════╝"

# Run the Python launcher (it will handle venv setup)
python3 launcher.py || python launcher.py