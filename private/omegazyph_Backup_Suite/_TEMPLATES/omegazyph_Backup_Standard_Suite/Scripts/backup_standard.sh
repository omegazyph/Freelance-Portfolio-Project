#!/bin/bash

# =================================================================
# Script Name: backup_standard.sh
# Author:      omegazyph
# Date:        2026-02-14
# Updated:     2026-02-14
# Description: Professional backup script featuring automated 
#              rotation and retention logic to manage disk space.
# =================================================================

# --- CONFIGURATION SECTION ---
# Define the source directory you want to back up
SOURCE_DIRECTORY="$HOME/Documents"

# Define where the backup archives will be stored
BACKUP_DESTINATION="$HOME/Backups"

# Define the path for the log file
LOG_FILE_PATH="$HOME/Backups/backup_log.txt"

# RETENTION POLICY: Set the number of days to keep backup files
# Backups older than this number will be automatically deleted.
RETENTION_DAYS=14

# Generate a timestamp for the filename (Year-Month-Day_Hour-Minute)
CURRENT_TIMESTAMP=$(date +%Y-%m-%d_%H-%M)

# Define the final filename for the archive
ARCHIVE_NAME="backup_${CURRENT_TIMESTAMP}.tar.gz"

# --- INITIALIZATION ---
# Create the backup destination directory if it does not already exist
if [ ! -d "$BACKUP_DESTINATION" ]; then
    mkdir -p "$BACKUP_DESTINATION"
fi

# Create the log file if it does not exist
touch "$LOG_FILE_PATH"

echo "----------------------------------------------------------" >> "$LOG_FILE_PATH"
echo "[$(date)] --- STARTING STANDARD BACKUP PROCESS ---" >> "$LOG_FILE_PATH"

# --- STEP 1: COMPRESSION ---
echo "[$(date)] INFO: Compressing $SOURCE_DIRECTORY..." >> "$LOG_FILE_PATH"

# Create a compressed tarball of the source directory
# -c: Create, -z: Gzip compression, -f: Filename
tar -czf "$BACKUP_DESTINATION/$ARCHIVE_NAME" "$SOURCE_DIRECTORY" 2>> "$LOG_FILE_PATH"

# Check if the tar command was successful
if [ $? -eq 0 ]; then
    echo "[$(date)] SUCCESS: Backup created: $ARCHIVE_NAME" >> "$LOG_FILE_PATH"
else
    echo "[$(date)] ERROR: Compression failed. Check logs for details." >> "$LOG_FILE_PATH"
    exit 1
fi

# --- STEP 2: AUTO-CLEANUP (RETENTION) ---
echo "[$(date)] INFO: Running retention policy (Deleting files older than $RETENTION_DAYS days)..." >> "$LOG_FILE_PATH"

# Use the find command to identify and delete old backup files
# -mtime +14 finds files modified more than 14 days ago
# -delete removes the files
# -print | wc -l counts how many files were removed
DELETED_COUNT=$(find "$BACKUP_DESTINATION" -name "backup_*.tar.gz" -type f -mtime +$RETENTION_DAYS -delete -print | wc -l)

if [ "$DELETED_COUNT" -gt 0 ]; then
    echo "[$(date)] CLEANUP: Successfully removed $DELETED_COUNT old backup file(s)." >> "$LOG_FILE_PATH"
else
    echo "[$(date)] CLEANUP: No old backup files found to remove." >> "$LOG_FILE_PATH"
fi

echo "[$(date)] --- BACKUP PROCESS COMPLETE ---" >> "$LOG_FILE_PATH"
echo "----------------------------------------------------------" >> "$LOG_FILE_PATH"

# Final output to the terminal for the user
echo "Backup process finished successfully. Deleted $DELETED_COUNT old archives."