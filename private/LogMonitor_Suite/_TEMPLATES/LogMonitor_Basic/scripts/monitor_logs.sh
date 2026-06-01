#!/bin/bash

# ==============================================================================
# Date: 2026-01-05
# Script Name: monitor_logs.sh
# Author: omegazyph
# Updated: 2026-02-14
# Description: Basic launcher script. Automatically detects its own directory
#              to find and execute the Python analysis engine.
# ==============================================================================

# Get the absolute path of the directory where this script is saved
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "Starting omegazyph Basic Log Monitor..."

# Change directory to where the script actually lives
cd "$SCRIPT_DIR"

# Now we check if the Python script exists in this same directory
if [ ! -f "analyze_data.py" ]; then
    echo "Error: analyze_data.py is missing from $SCRIPT_DIR"
    exit 1
fi

# Run the Python script
# Using 'python' for Windows/VSCode compatibility
python analyze_data.py

if [ $? -eq 0 ]; then
    echo "Task completed successfully."
else
    echo "The script encountered an error."
    exit 1
fi