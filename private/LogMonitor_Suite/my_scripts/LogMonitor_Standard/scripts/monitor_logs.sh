#!/bin/bash

# ==============================================================================
# Date: 2026-01-05
# Script Name: monitor_logs.sh
# Author: omegazyph
# Updated: 2026-02-14
# Description: Standard Controller. Uses dynamic path detection to ensure
#              the LogMonitor folder is found regardless of terminal location.
# ==============================================================================

# ------------------------------------------------------------------------------
# Dynamic Path Detection
# ------------------------------------------------------------------------------
# This finds the directory where monitor_logs.sh is actually stored
CURRENT_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Go up one level to set the Project Root automatically
# This way, the name of the folder doesn't matter as much!
PROJECT_ROOT="$(dirname "$CURRENT_SCRIPT_DIR")"

LOG_DIRECTORY="$PROJECT_ROOT/logs"
SCRIPT_DIRECTORY="$PROJECT_ROOT/scripts"
REPORT_DIRECTORY="$PROJECT_ROOT/reports"
CONFIG_FILE="$PROJECT_ROOT/config.json"

echo "--- omegazyph Log Monitor: Standard Edition ---"
echo "[DEBUG] Current Path: $PROJECT_ROOT"

# ------------------------------------------------------------------------------
# Environment Validation
# ------------------------------------------------------------------------------

# 1. Check for the Configuration File
if [ ! -f "$CONFIG_FILE" ]; then
    echo "[ERROR] config.json not found at: $CONFIG_FILE"
    exit 1
fi

# 2. Ensure directories exist
[ ! -d "$LOG_DIRECTORY" ] && mkdir -p "$LOG_DIRECTORY"
[ ! -d "$REPORT_DIRECTORY" ] && mkdir -p "$REPORT_DIRECTORY"

# 3. Check for the Python engine
if [ ! -f "$SCRIPT_DIRECTORY/analyze_data.py" ]; then
    echo "[ERROR] Python script missing at: $SCRIPT_DIRECTORY/analyze_data.py"
    exit 1
fi

# ------------------------------------------------------------------------------
# Execution
# ------------------------------------------------------------------------------
echo "[*] Validation successful. Launching Python..."

# Run the Python script using the absolute path we found
python "$SCRIPT_DIRECTORY/analyze_data.py"

if [ $? -eq 0 ]; then
    echo "[SUCCESS] Task completed."
else
    echo "[FAILURE] Python engine error."
    exit 1
fi