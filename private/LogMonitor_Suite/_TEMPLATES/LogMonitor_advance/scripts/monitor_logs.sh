#!/bin/bash

# ==============================================================================
# Date: 2026-01-05
# Script Name: monitor_logs.sh
# Author: omegazyph
# Updated: 2026-02-14
# Description: Advanced Controller. Features dynamic path resolution, 
#              automated dependency checks, and environment preparation.
# ==============================================================================

# Find the project root based on script location
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="$BASE_DIR/config.json"
PYTHON_ENGINE="$BASE_DIR/scripts/analyze_data.py"

echo "------------------------------------------"
echo "  OMEGAZYPH ADVANCED MONITORING SYSTEM   "
echo "------------------------------------------"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "[CRITICAL] Python is not installed or not in PATH."
    exit 1
fi

# Ensure Config exists
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "[ERROR] Missing config.json at $BASE_DIR"
    exit 1
fi

# Create directory structure if missing
mkdir -p "$BASE_DIR/logs" "$BASE_DIR/reports"

# Run the Engine
echo "[*] Initializing Python Logic Engine..."
python "$PYTHON_ENGINE"

if [ $? -eq 0 ]; then
    echo "[INFO] Process completed successfully."
else
    echo "[ERROR] Logic Engine returned a failure code."
    exit 1
fi