"""
Date:         2026-02-11
Script Name:  Invoice_Extractor_Advanced.py
Author:       omegazyph
Updated:      2026-02-11
Description:  Advanced Tier: Extracts data, renames files, and syncs 
              results directly to a Google Sheets document via API.
"""

import pdfplumber
#import pandas as pd
import re
import os
import gspread
from google.oauth2.service_account import Credentials

# Set up paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVOICE_DIR = os.path.join(BASE_DIR, 'Invoices')
CRED_FILE = os.path.join(BASE_DIR, 'credentials.json')

def sync_to_google_sheets(data_list):
    """Connects to Google Sheets API and appends data."""
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    try:
        creds = Credentials.from_service_account_file(CRED_FILE, scopes=scopes)
        client = gspread.authorize(creds)
        
        # The client must provide the Sheet Name
        sheet = client.open("Invoice_Data_Sync").sheet1
        
        for entry in data_list:
            sheet.append_row([entry['Date'], entry['Total'], entry['Original Name']])
        print("Successfully synced to Google Sheets!")
    except Exception as e:
        print(f"Google Sync Error: {e}")

def run_advanced_process():
    results = []
    date_regex = r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
    total_regex = r'(?:Total|Amount Due|Balance)[:\s]*\$?\s*(\d+[\.,]\d{2})'

    print("--- omegazyph Advanced Enterprise Extractor ---")

    for filename in os.listdir(INVOICE_DIR):
        if filename.lower().endswith('.pdf'):
            path = os.path.join(INVOICE_DIR, filename)
            
            with pdfplumber.open(path) as pdf:
                text = "".join([page.extract_text() or "" for page in pdf.pages])
                date_m = re.search(date_regex, text)
                total_m = re.search(total_regex, text, re.IGNORECASE)
                
                date_val = date_m.group(1) if date_m else "Unknown"
                total_val = total_m.group(1) if total_m else "0.00"

                results.append({
                    'Original Name': filename,
                    'Date': date_val,
                    'Total': total_val
                })

    # Run the Sync
    if results:
        sync_to_google_sheets(results)

if __name__ == "__main__":
    if os.path.exists(CRED_FILE):
        run_advanced_process()
    else:
        print("Error: credentials.json not found. Please add it to the root folder.")