# Hotel Price Tracker (Standard Edition)

## Developer Information

    Author: omegazyph
    Script Name: hotel_price_standard.py
    Updated: 2026-02-15

## Project Overview

This project provides an automated solution for tracking hotel prices across multiple targets. It is designed for users who need to monitor pricing trends over time and save that data into a persistent, spreadsheet-ready format.
Key Improvements

    Persistent Logging: Automatically appends new data to price_history.csv instead of overwriting.

    Batch Processing: Reads multiple URLs from hotel_list.txt for parallel monitoring.

    Cross-Platform Compatibility: Uses utf-8-sig encoding and standard Excel dialects to ensure files open correctly in OpenOffice, LibreOffice, and Microsoft Excel without filter prompts.

    Numeric Cleaning: Strips currency symbols to allow for immediate mathematical analysis in spreadsheets.

## File Structure

Keep the following files in the same directory on your machine:
Plaintext

HotelPriceTracker_Standard/
├── hotel_price_standard.py   # Main Scraper
├── hotel_list.txt            # URL Input File
└── price_history.csv         # Generated Historical Log

## Usage Instructions

    Target Setup: Add your hotel URLs to hotel_list.txt (one per line).

    Run Script: Execute via terminal:
    Bash

    python hotel_price_standard.py

    Analyze Data: Open price_history.csv in your preferred spreadsheet program.

        Note: If prompted by OpenOffice, select Comma as the separator and Unicode (UTF-8) as the character set.

## Technical Notes

    Time Format: US Standard (MM-DD-YYYY HH:MM AM/PM).

    Encoding: UTF-8 with BOM (Byte Order Mark) for automated software detection.

    Error Handling: Includes protection against file-access errors if the CSV is already open in another program.
    