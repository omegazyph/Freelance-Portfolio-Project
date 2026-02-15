# Hotel Price Tracker (Advanced Edition)

## Developer Information

    Author: omegazyph
    Script Name: hotel_price_advanced.py
    Updated: 2026-02-15

## Premium Features

    This is the flagship version of the tracker, built for automated monitoring and immediate notification.

    Color-Coded Terminal UI: High-visibility status updates (Green for success, Yellow for alerts, Red for errors).

    Automated Email Alerts: Integrated SMTP support to notify you the second a price drops below your target.

    JSON Configuration: Manage all settings (emails, passwords, price thresholds) in an external config.json file—no coding required.

    Universal CSV Export: Uses utf-8-sig for instant, clean opening in OpenOffice, Excel, and Google Sheets.

## Installation & Setup

    Project Directory: Ensure hotel_price_advanced.py and hotel_list.txt are in the same folder.

    Initialize Config: Run the script once to generate the config.json file.

    Configure Settings: Open config.json in VSCode and update:

        email_alerts: Set to true to enable notifications.

        sender_password: Use a Google App Password (not your standard login).

        price_threshold: Set your "Deal" price (e.g., 120.00).

## Operation

Run the script from your terminal:
Bash

python hotel_price_advanced.py

## Project Structure

Plaintext

HotelPriceTracker_Advanced/
├── hotel_price_advanced.py   # Main Engine
├── config.json               # User Settings (Auto-generated)
├── hotel_list.txt            # Target URLs
└── price_history.csv         # Persistent Log
