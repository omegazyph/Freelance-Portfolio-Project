#!/bin/bash

# ============================================================
# Date:         2026-02-13
# Script Name:  health_check_basic.sh
# Author:       omegazyph
# Updated:      2026-02-13
# Description:  Basic Tier: Monitors Disk, Memory, and CPU usage. 
#               Outputs a summary to the console and a log file.
# ============================================================

# Define Paths
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
LOG_DIR="$SCRIPT_DIR/../Logs"
TIMESTAMP=$(date "+%Y-%m-%d_%H-%M-%S")
LOG_FILE="$LOG_DIR/health_report_$TIMESTAMP.log"

# Create Logs directory if it does not exist
if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
fi

echo "------------------------------------------" | tee -a "$LOG_FILE"
echo "   omegazyph SYSTEM HEALTH REPORT" | tee -a "$LOG_FILE"
echo "   Date: $TIMESTAMP" | tee -a "$LOG_FILE"
echo "------------------------------------------" | tee -a "$LOG_FILE"

# 1. Check Disk Usage (Threshold: 80%)
echo "[*] Checking Disk Usage..." | tee -a "$LOG_FILE"
df -h | grep '^/dev/' | while read -r line; do
    usage=$(echo "$line" | awk '{print $5}' | sed 's/%//')
    partition=$(echo "$line" | awk '{print $1}')
    if [ "$usage" -gt 80 ]; then
        echo "  [ALERT] Partition $partition is at ${usage}%!" | tee -a "$LOG_FILE"
    else
        echo "  [OK] Partition $partition is at ${usage}%." | tee -a "$LOG_FILE"
    fi
done

# 2. Check Memory Usage
echo -e "\n[*] Checking Memory Usage..." | tee -a "$LOG_FILE"
free -h | awk '/^Mem:/ {print "  Used: " $3 " / Total: " $2}' | tee -a "$LOG_FILE"

# 3. Check CPU Load
echo -e "\n[*] Checking CPU Load (1 min average)..." | tee -a "$LOG_FILE"
cpu_load=$(uptime | awk -F'load average:' '{ print $2 }' | cut -d, -f1 | xargs)
echo "  Current Load: $cpu_load" | tee -a "$LOG_FILE"

echo -e "\n------------------------------------------" | tee -a "$LOG_FILE"
echo "Report saved to: $LOG_FILE"
echo "------------------------------------------"