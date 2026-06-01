# omegazyph Backup & Notification Suite (Advanced)

**Version:** 1.0  
**Author:** omegazyph  
**Updated:** 2026-02-14

## Description

The Advanced Suite is a high-end disaster recovery and monitoring solution. It combines the reliability of Bash archiving with a Python-based notification engine to provide real-time status updates directly to your Discord or Slack workspace.

## Key Features

* **Full Automation:** Backup, Compression, and Rotation (Cleanup).
* **Real-Time Alerts:** Immediate notifications via Webhooks if a backup succeeds or fails.
* **Hybrid Technology:** Leverages Bash for system-level speed and Python for modern API connectivity.
* **Extended Retention:** Defaulted to 30-day history (customizable).

## Prerequisites

This suite requires **Python 3.x** and the `requests` library.
To install dependencies, run:

bash
pip install -r requirements.txt

Installation & Setup

    Configure the Webhook:
    Open Scripts/notify.py in VSCode and paste your Discord or Slack Webhook URL into the webhook_url variable.

    Configure Paths:
    Open Scripts/backup_advanced.sh and set your SOURCE_DIRECTORY and BACKUP_DESTINATION.

    Grant Permissions:
    Bash

    chmod +x Scripts/backup_advanced.sh

    Test the System:
    Run the script manually to ensure the notification arrives in your chat channel:
    Bash

    ./Scripts/backup_advanced.sh

## File Structure

    Scripts/backup_advanced.sh: The main automation logic.

    Scripts/notify.py: The Python engine for API alerts.

    requirements.txt: Python dependency list.

    Logs/: Directory for audit logs.

## Support

This is the flagship product of the omegazyph brand. For further customization (Cloud storage sync to AWS/Google), please contact me via Upwork.
