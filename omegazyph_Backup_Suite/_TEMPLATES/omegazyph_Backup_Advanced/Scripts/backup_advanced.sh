#!/bin/bash

# =================================================================
# Script Name: backup_advanced.sh
# Author:      omegazyph
# Date:        2026-02-14
# Updated:     2026-02-14
# Description: Advanced backup suite with retention logic and
#              Python-integrated Discord/Slack notifications.
# =================================================================

# --- CONFIGURATION ---
SOURCE_DIRECTORY="$HOME/Documents"
BACKUP_DESTINATION="$HOME/Backups"
LOG_FILE_PATH="$HOME/Backups/backup_log.txt"
RETENTION_DAYS=30
PYTHON_ENGINE="./notify.py"

CURRENT_TIMESTAMP=$(date +%Y-%m-%d_%H-%M)
ARCHIVE_NAME="backup_${CURRENT_TIMESTAMP}.tar.gz"

# --- INITIALIZATION ---
mkdir -p "$BACKUP_DESTINATION"
echo "[$(date)] --- STARTING ADVANCED BACKUP PROCESS ---" >> "$LOG_FILE_PATH"

# --- STEP 1: COMPRESSION ---
if tar -czf "$BACKUP_DESTINATION/$ARCHIVE_NAME" "$SOURCE_DIRECTORY" 2>> "$LOG_FILE_PATH"; then
    STATUS_MSG="SUCCESS: Backup created: $ARCHIVE_NAME"
    echo "[$(date)] $STATUS_MSG" >> "$LOG_FILE_PATH"
else
    STATUS_MSG="ERROR: Backup FAILED for $SOURCE_DIRECTORY"
    echo "[$(date)] $STATUS_MSG" >> "$LOG_FILE_PATH"
    # Send immediate failure alert
    python3 "$PYTHON_ENGINE" "$STATUS_MSG"
    exit 1
fi

# --- STEP 2: AUTO-CLEANUP ---
DELETED_COUNT=$(find "$BACKUP_DESTINATION" -name "backup_*.tar.gz" -type f -mtime +$RETENTION_DAYS -delete -print | wc -l)
echo "[$(date)] CLEANUP: Removed $DELETED_COUNT old files." >> "$LOG_FILE_PATH"

# --- STEP 3: ADVANCED NOTIFICATION ---
# Send a final status report via the Python engine
REPORT="Backup complete. Status: Success. Files Rotated: $DELETED_COUNT."
python3 "$PYTHON_ENGINE" "$REPORT"

echo "[$(date)] --- ADVANCED PROCESS COMPLETE ---" >> "$LOG_FILE_PATH"