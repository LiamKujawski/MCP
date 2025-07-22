#!/usr/bin/env bash
# Simple one-click launcher for MCP (frontend + backend)
#
# Usage (Linux/macOS):
#   chmod +x run_local.sh
#   ./run_local.sh
#
# The script will:
#   1. Build & start the containers in detached mode
#   2. Wait until the UI container is healthy
#   3. Open the browser at http://localhost:3000
set -euo pipefail

PROJECT_NAME="mcp-local"
COMPOSE_FILE="docker-compose.local.yml"

# Build & start
echo "🚀  Launching MCP locally (this may take a minute on first run)…"
docker compose -p "${PROJECT_NAME}" -f "${COMPOSE_FILE}" up --build -d

# Wait for the UI to be reachable
printf "⏳  Waiting for the UI to become available…"
until curl -sSf http://localhost:3000 > /dev/null 2>&1; do
  printf "."
  sleep 2
done
printf " done!\n"

# Try to open the browser automatically
URL="http://localhost:3000"
if command -v xdg-open > /dev/null 2>&1; then
  xdg-open "$URL" &>/dev/null &
elif command -v open > /dev/null 2>&1; then  # macOS
  open "$URL"
fi

echo "✅ MCP is now running! Access the UI at $URL (API at http://localhost:8000)"