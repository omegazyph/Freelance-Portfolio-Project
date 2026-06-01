# Hotel Price Tracker (Advanced Edition)

## Developer Information

    Author: omegazyph
    Script Name: hotel_price_advanced.py
    Setup Utility: setup.sh
    Updated: 2026-02-15

## Premium Features

    This version is designed for high-performance monitoring and ease of use.

    Automated Environment Setup: Use the included Bash script to install all dependencies automatically.

    Color-Coded Terminal UI: Instant visual feedback (Green = Success, Yellow = Price Alert, Red = Error).

    Automated Email Notifications: Get alerted the moment a price drops below your custom threshold.

    External Configuration: Manage settings via config.json without touching the Python code.

## Installation

    On your Lenovo Legion (or any machine with a Bash-compatible terminal like MINGW64/Git Bash), run the following:

    Execute Setup:
    Bash

    bash setup.sh

    This script will automatically verify Python and install the required requests and beautifulsoup4 libraries.

## Configuration

    Initialize: Run the script once (python hotel_price_advanced.py) to generate config.json.

    Edit Settings: Open config.json and set your preferences:

        "email_alerts": true

        "price_threshold": 100.00 (Set your target price)

        "sender_password": "your-app-password"

## Usage

Once configured, run the tracker anytime:
Bash

python hotel_price_advanced.py

## File Structure

Plaintext

HotelPriceTracker_Advanced/
├── hotel_price_advanced.py   # Main Scraper Engine
├── setup.sh                  # Automated Bash Setup
├── requirements.txt          # Dependency List
├── config.json               # User Configuration
├── hotel_list.txt            # Target URLs
└── price_history.csv         # Historical Price Log

## Technical Support

    Spreadsheet Compatibility: The price_history.csv is optimized for OpenOffice and Excel using UTF-8-SIG encoding.

    Numeric Data: Prices are stored as clean numbers for easy calculations and charting.
