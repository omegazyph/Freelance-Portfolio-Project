#!/bin/bash

# =================================================================
# Script Name: backup_local.sh
# Author:      omegazyph
# Date:        2026-02-14
# Updated:     2026-02-14
# Description: local backup script with timestamped 
#              compression and automated logging.
# =================================================================

# --- CONFIGURATION ---
# The folder you want to back up
SOURCE_DIR="$HOME/Documents"

# Where the backup files will be stored
BACKUP_DIR="$HOME/Backups"

# Where the logs will be kept
LOG_FILE="$HOME/Backups/backup_log.txt"

# Timestamp format (Year-Month-Day_Hour-Minute)
DATE=$(date +%Y-%m-%d_%H-%M)

# Final filename
BACKUP_NAME="backup_$DATE.tar.gz"

# --- START PROCESS ---

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

echo "[$(date)] Starting backup of $SOURCE_DIR..." >> "$LOG_FILE"

# Run the compression
# -c: create, -z: gzip, -f: file
if tar -czf "$BACKUP_DIR/$BACKUP_NAME" "$SOURCE_DIR" 2>> "$LOG_FILE"; then
    echo "[$(date)] SUCCESS: Backup created at $BACKUP_DIR/$BACKUP_NAME" >> "$LOG_FILE"
    echo "Backup successful: $BACKUP_NAME"
else
    echo "[$(date)] ERROR: Backup failed for $SOURCE_DIR" >> "$LOG_FILE"
    echo "Backup failed. Check $LOG_FILE for details."
    exit 1
fi

# --- END PROCESS ---