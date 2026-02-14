# =================================================================
# Script Name: notify.py
# Author:      omegazyph
# Date:        2026-02-14
# Updated:     2026-02-14
# Description: Python engine to send system alerts to Discord/Slack
#              webhooks for the Advanced Backup Suite.
# =================================================================

import requests
import sys

def send_notification(message):
    # The client will provide their specific Webhook URL here
    webhook_url = "YOUR_WEBHOOK_URL_HERE"
    
    payload = {
        "content": f"🚀 **omegazyph System Alert**\n{message}"
    }

    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204 or response.status_code == 200:
            print("Notification sent successfully.")
        else:
            print(f"Failed to send notification. Status: {response.status_code}")
    except Exception as error:
        print(f"An error occurred while sending notification: {error}")

if __name__ == "__main__":
    # Check if a message was passed from the Bash script
    if len(sys.argv) > 1:
        combined_message = " ".join(sys.argv[1:])
        send_notification(combined_message)
    else:
        print("No message provided to notify.py")