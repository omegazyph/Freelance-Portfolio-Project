#!/bin/bash

# ============================================================
# Date:         2026-02-13
# Script Name:  health_check_advanced.sh
# Author:       omegazyph
# Updated:      2026-02-13
# Description:  Advanced Tier: Monitors health, rotates logs, 
#               clears /tmp, and sends Discord/Slack Webhook 
#               alerts if critical thresholds are met.
# ============================================================

# Define Paths
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
LOG_DIR="$SCRIPT_DIR/../Logs"
TIMESTAMP=$(date "+%Y-%m-%d_%H-%M-%S")
LOG_FILE="$LOG_DIR/advanced_report_$TIMESTAMP.log"

# --- Configuration ---
DISK_THRESHOLD=90
WEBHOOK_URL="YOUR_WEBHOOK_URL_HERE" # Client provides this
ADMIN_EMAIL="admin@example.com"

mkdir -p "$LOG_DIR"

# Function to send alerts
send_alert() {
    local message="$1"
    echo "[ALERT] $message" | tee -a "$LOG_FILE"
    
    # Example: Discord/Slack Webhook Integration
    if [[ "$WEBHOOK_URL" != "YOUR_WEBHOOK_URL_HERE" ]]; then
        curl -H "Content-Type: application/json" \
             -X POST \
             -d "{\"content\": \"⚠️ **SYSTEM ALERT ($HOSTNAME)**: $message\"}" \
             "$WEBHOOK_URL" > /dev/null 2>&1
    fi
}

echo "------------------------------------------" | tee -a "$LOG_FILE"
echo "   omegazyph ENTERPRISE MONITORING" | tee -a "$LOG_FILE"
echo "------------------------------------------" | tee -a "$LOG_FILE"

# 1. Critical Disk Check
usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$usage" -gt "$DISK_THRESHOLD" ]; then
    send_alert "Disk usage is critical at ${usage}%! Immediate attention required."
else
    echo "[OK] Disk usage: ${usage}%" | tee -a "$LOG_FILE"
fi

# 2. Memory Analysis
mem_free=$(free | grep Mem | awk '{print $4/$2 * 100.0}')
if (( $(echo "$mem_free < 10.0" | bc -l) )); then
    send_alert "Low Memory Warning! Only ${mem_free}% RAM remaining."
fi

# 3. Service Check (Example: SSH)
if ! systemctl is-active --quiet ssh; then
    send_alert "SSH Service is DOWN!"
fi

# 4. Standard Maintenance (Rotation & Cleanup)
ls -t "$LOG_DIR"/*.log 2>/dev/null | tail -n +16 | xargs rm -f 2>/dev/null
find /tmp -type f -atime +3 -delete 2>/dev/null

echo -e "\n--- Process Complete at $(date) ---" | tee -a "$LOG_FILE"