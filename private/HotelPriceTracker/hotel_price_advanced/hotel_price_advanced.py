"""
Date: 2026-01-05
Script Name: hotel_price_advanced.py
Author: omegazyph
Updated: 2026-02-15
Description: Premium Edition with ANSI color-coded terminal output, 
JSON configuration, and SMTP email alerts.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os
import json
import smtplib
import sys
import io
from email.mime.text import MIMEText

# Terminal encoding fix
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ANSI Color Codes for terminal styling
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Path setup
base_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(base_dir, "hotel_list.txt")
output_file = os.path.join(base_dir, "price_history.csv")
config_file = os.path.join(base_dir, "config.json")

def load_config():
    if not os.path.exists(config_file):
        default = {
            "email_alerts": False,
            "sender_email": "user@gmail.com",
            "sender_password": "app_password_here",
            "receiver_email": "user@gmail.com",
            "price_threshold": 50.00
        }
        with open(config_file, "w") as f:
            json.dump(default, f, indent=4)
        print(f"{Colors.YELLOW}Config created. Update settings in config.json{Colors.RESET}")
        return default
    
    with open(config_file, "r") as f:
        return json.load(f)

def send_alert(config, url, price):
    msg = MIMEText(f"Price Drop Detected!\n\nTarget reached for: {url}\nCurrent Price: {price}")
    msg["Subject"] = "Hotel Price Alert"
    msg["From"] = config["sender_email"]
    msg["To"] = config["receiver_email"]

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(config["sender_email"], config["sender_password"])
            server.sendmail(config["sender_email"], config["receiver_email"], msg.as_string())
        print(f"{Colors.GREEN}{Colors.BOLD}>>> ALERT SENT: {config['receiver_email']}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}Email Alert Failed: {e}{Colors.RESET}")

def run_advanced_tracker():
    settings = load_config()

    if not os.path.exists(input_file):
        print(f"{Colors.RED}Error: hotel_list.txt not found in project folder.{Colors.RESET}")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    print(f"\n{Colors.CYAN}{Colors.BOLD}--- omegazyph Advanced Tracker v2.0 ---{Colors.RESET}")
    print(f"{Colors.CYAN}Monitoring {len(urls)} targets...{Colors.RESET}\n")

    results = []
    for url in urls:
        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code == 200:
                soup = BeautifulSoup(res.content, 'html.parser')
                price_tag = soup.find("p", {"class": "price_color"})
                
                if price_tag:
                    raw_price = price_tag.get_text(strip=True)
                    price_val = float("".join(c for c in raw_price if c.isdigit() or c == '.'))
                    
                    timestamp = datetime.now().strftime("%m-%d-%Y %I:%M %p")
                    results.append({"Date": timestamp, "URL": url, "Price": price_val})
                    
                    # Status output
                    print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} {price_val} | {url[:40]}...")

                    # Alert check with color notification
                    if settings["email_alerts"] and price_val <= settings["price_threshold"]:
                        print(f"{Colors.YELLOW}[ALERT]{Colors.RESET} Price below ${settings['price_threshold']}!")
                        send_alert(settings, url, price_val)
                else:
                    print(f"{Colors.YELLOW}[MISSING]{Colors.RESET} No price found: {url[:40]}")
            else:
                print(f"{Colors.RED}[FAILED]{Colors.RESET} HTTP {res.status_code} on {url[:40]}")
        except Exception as e:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} System failure on {url[:40]}: {e}")

    if results:
        save_data(output_file, results)

def save_data(path, data):
    exists = os.path.isfile(path)
    try:
        with open(path, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["Date", "URL", "Price"], dialect='excel')
            if not exists:
                writer.writeheader()
            writer.writerows(data)
        print(f"\n{Colors.CYAN}--- Data logged to {os.path.basename(path)} ---{Colors.RESET}")
    except PermissionError:
        print(f"\n{Colors.RED}!!! CLOSE THE CSV FILE TO SAVE NEW DATA !!!{Colors.RESET}")

if __name__ == "__main__":
    # Activate ANSI on Windows 11 terminals
    os.system('') 
    run_advanced_tracker()