#!/bin/bash

# ==============================================================================
# Date: 2026-02-10
# Script Name: monitor_logs.sh
# Author: omegazyph
# Updated: 2026-02-10
# Description: This script serves as the primary controller. It validates the 
#              environment and handles execution permissions for the system.
# ==============================================================================

# Define clear variables for all directory paths
PROJECT_ROOT=$"LogMonitorPro"
LOG_DIRECTORY="$PROJECT_ROOT/logs"
SCRIPT_DIRECTORY="$PROJECT_ROOT/scripts"

echo "Initialising the monitor logs script..."

# Ensure the logs directory exists so the script does not fail
if [ ! -d "$LOG_DIRECTORY" ]; then
    echo "Warning: The logs directory was missing. Creating it now at $LOG_DIRECTORY"
    mkdir -p "$LOG_DIRECTORY"
fi

# Ensure the file exists so the python script dose not fail
if [ ! -f "$LOG_DIRECTORY/system_activity.log" ]; then
    echo "Please put your system_activity.log in ${LOG_DIRECTORY}"
    echo "Exiting program now..."

    # This stops the entire script immediately
    exit 1
fi


# Check for the existence of the Python analysis script
if [ ! -f "$SCRIPT_DIRECTORY/analyze_data.py" ]; then
    echo "Fatal Error: The Python script analyze_data.py is missing from $SCRIPT_DIRECTORY"
    exit 1
fi

echo "Environment validation is complete. Starting the Python analysis engine..."

# Execute the Python program and capture any error codes
python "${SCRIPT_DIRECTORY}/analyze_data.py"

if [ $? -eq 0 ]; then
    echo "The Python engine has finished processing successfully."
else
    echo "The Python engine encountered an error during execution."
    exit 1
fi



