#!/bin/bash

# ==============================================================================
# Date: 2026-02-10
# Script Name: monitor_logs.sh
# Author: omegazyph
# Updated: 2026-02-10
# Description: This script serves as the primary controller. It validates the 
#              environment, handles optional file cleanup via arguments, 
#              and executes the Python analysis engine.
# ==============================================================================

# ------------------------------------------------------------------------------
# User Configuration and Arguments
# ------------------------------------------------------------------------------

# This variable determines if old reports are deleted.
# It can be set here to "YES" or "NO".
ENABLE_CLEANUP="NO"

# If the user provides an argument when running the script, we capture it.
# Example: ./monitor_logs.sh cleanup
USER_ARGUMENT=$1

if [ "$USER_ARGUMENT" == "cleanup" ]; then
    ENABLE_CLEANUP="YES"
fi

# Define the number of days to keep a report if cleanup is active
RETENTION_DAYS=30

# ------------------------------------------------------------------------------
# Directory Path Definitions
# ------------------------------------------------------------------------------

PROJECT_ROOT="LogMonitorPro"
LOG_DIRECTORY="$PROJECT_ROOT/logs"
SCRIPT_DIRECTORY="$PROJECT_ROOT/scripts"
REPORT_DIRECTORY="$PROJECT_ROOT/reports"

echo "Initialising the monitor logs script..."

# Ensure the logs directory exists so the script does not fail
if [ ! -d "$LOG_DIRECTORY" ]; then
    echo "Warning: The logs directory was missing. Creating it now at $LOG_DIRECTORY"
    mkdir -p "$LOG_DIRECTORY"
fi

# Ensure the reports directory exists for the cleanup and analysis tasks
if [ ! -d "$REPORT_DIRECTORY" ]; then
    echo "The reports directory was missing. Creating it now at $REPORT_DIRECTORY"
    mkdir -p "$REPORT_DIRECTORY"
fi

# ------------------------------------------------------------------------------
# Conditional Cleanup Execution
# ------------------------------------------------------------------------------

if [ "$ENABLE_CLEANUP" == "YES" ]; then
    echo "Cleanup mode is active. Removing reports older than $RETENTION_DAYS days..."
    
    # Locate and delete old analysis reports
    find "$REPORT_DIRECTORY" -name "analysis_report_*.txt" -type f -mtime +$RETENTION_DAYS -delete
    
    echo "The cleanup process has finished."
else
    echo "Skipping cleanup. All existing reports will be preserved."
fi

# ------------------------------------------------------------------------------
# Environment Validation
# ------------------------------------------------------------------------------

# Ensure the log file exists so the Python script does not fail
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

# ------------------------------------------------------------------------------
# Python Execution
# ------------------------------------------------------------------------------

# Execute the Python program and capture any error codes
python "${SCRIPT_DIRECTORY}/analyze_data.py"

if [ $? -eq 0 ]; then
    echo "The Python engine has finished processing successfully."
else
    echo "The Python engine encountered an error during execution."
    exit 1
fi