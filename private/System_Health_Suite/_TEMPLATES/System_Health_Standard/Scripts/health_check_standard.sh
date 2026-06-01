#!/bin/bash

# ============================================================
# Date:         2026-02-13
# Script Name:  health_check_standard.sh
# Author:       omegazyph
# Updated:      2026-02-13
# Description:  Standard Tier: Monitors health, rotates logs, 
#               and clears /tmp files if disk space is low.
# ============================================================

# Define Paths
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
LOG_DIR="$SCRIPT_DIR/../Logs"
TIMESTAMP=$(date "+%Y-%m-%d_%H-%M-%S")
LOG_FILE="$LOG_DIR/standard_report_$TIMESTAMP.log"

# Threshold for auto-cleanup (%)
DISK_THRESHOLD=80

# Ensure Logs directory exists
mkdir -p "$LOG_DIR"

echo "------------------------------------------" | tee -a "$LOG_FILE"
echo "   omegazyph STANDARD HEALTH & CLEANUP" | tee -a "$LOG_FILE"
echo "   System: $(hostname) | Date: $TIMESTAMP" | tee -a "$LOG_FILE"
echo "------------------------------------------" | tee -a "$LOG_FILE"

# 1. Disk Check and Auto-Cleanup
echo "[*] Analyzing Disk Space..." | tee -a "$LOG_FILE"
usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')

if [ "$usage" -gt "$DISK_THRESHOLD" ]; then
    echo "  [WARNING] Disk usage is at ${usage}%. Cleaning /tmp..." | tee -a "$LOG_FILE"
    # Removes files older than 7 days in /tmp
    find /tmp -type f -atime +7 -delete 2>/dev/null
    echo "  [SUCCESS] Cleanup completed." | tee -a "$LOG_FILE"
else
    echo "  [OK] Disk usage is healthy at ${usage}%." | tee -a "$LOG_FILE"
fi

# 2. Log Rotation (Keep only the 10 most recent logs)
echo -e "\n[*] Rotating old logs..." | tee -a "$LOG_FILE"
# List logs by time, skip the first 10, delete the rest
ls -t "$LOG_DIR"/*.log 2>/dev/null | tail -n +11 | xargs rm -f 2>/dev/null
echo "  Maintenance: Log count limited to 10." | tee -a "$LOG_FILE"

# 3. System Metrics Summary
echo -e "\n[*] Current Statistics:" | tee -a "$LOG_FILE"
echo "  RAM Usage: $(free -h | awk '/^Mem:/ {print $3 "/" $2}')" | tee -a "$LOG_FILE"
echo "  CPU Load:  $(uptime | awk -F'load average:' '{print $2}' | xargs)" | tee -a "$LOG_FILE"

echo -e "\n------------------------------------------" | tee -a "$LOG_FILE"
echo "Report generated and archived." | tee -a "$LOG_FILE"