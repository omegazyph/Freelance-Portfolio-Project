# System Health Enterprise (Advanced Tier)

**Author:** omegazyph  
**Date:** 2026-02-13

## 💎 Premium Features

* **Instant Notifications:** Integrated Webhook support for Discord or Slack alerts.
* **Service Monitoring:** Automatically monitors the status of critical services (e.g., SSH, Apache, Nginx).
* **Memory Thresholds:** Advanced math calculations using `bc` for precise RAM percentage monitoring.
* **Aggressive Cleanup:** Shorter retention periods for temporary files and expanded log history (15 logs).

## 🚀 Setup

1. **Webhook:** Open `Scripts/health_check_advanced.sh` and paste your Discord/Slack Webhook URL in the `WEBHOOK_URL` variable.
2. **Dependencies:** Ensure `curl` and `bc` are installed:
   `sudo apt install curl bc`
3. **Execution:** `./run_advanced.sh`

## 📊 Automation (Cron)

For enterprise-grade monitoring, run this every 5 minutes:
`*/5 * * * * /path/to/run_advanced.sh`
