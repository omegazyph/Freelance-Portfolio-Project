# Project Name: Basic Hotel Price Scraper

Author: omegazyph

Date: 2026-01-05

Updated: 2026-02-15

## Description

This is a lightweight Python-based utility designed to automate the extraction of pricing data from hotel websites. It uses a "headless" request method with custom browser headers to mimic human traffic and bypass basic bot detection.

## Features

    Targeted Extraction: Uses BeautifulSoup4 to pinpoint specific HTML elements.

    Browser Masking: Includes professional User-Agent headers.

    Error Handling: Built-in logic to handle connection timeouts and missing data.

    Real-time Output: Logs the timestamp and price directly to the terminal.

## Installation

To run this script on your local machine, you need Python 3 and the following libraries. Open your terminal (or Git Bash) and run:
Bash

pip install requests beautifulsoup4

How to Use

    Open hotel_price_basic.py in VSCode.

    Update the target_url variable with the hotel link you wish to analyze.

    Run the script using the following command:
    Bash

    python hotel_price_basic.py

## File Structure

Plaintext

HotelScraper_Basic/
├── hotel_price_basic.py    # Main Python logic
└── README.md               # Documentation and instructions
