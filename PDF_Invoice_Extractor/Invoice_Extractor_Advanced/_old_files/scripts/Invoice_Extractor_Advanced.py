"""
Date:         2026-02-17
Script Name:  Invoice_Extractor_Advanced.py
Author:       omegazyph
Updated:      2026-02-17
Description:  Advanced Tier: Extracts data from PDF invoices, creates a local 
              CSV backup via Pandas, and syncs to Google Sheets.
              Updated to use /config and /results directories.
"""

import pdfplumber
import pandas as pd
import re
import os
import gspread
from google.oauth2.service_account import Credentials

# ANSI Color Codes for Professional Terminal Output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# Set up project directory structure
# Since this script is in /scripts, BASE_DIR is one level up
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVOICE_DIR = os.path.join(BASE_DIR, 'Invoices')
CONFIG_DIR = os.path.join(BASE_DIR, 'config')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

# Updated path to look inside the config folder
CREDENTIALS_FILE = os.path.join(CONFIG_DIR, 'credentials.json')

def sync_to_google_sheets(data_list):
    """Connects to Google Sheets API and appends extracted invoice data."""
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    try:
        credentials = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)
        client = gspread.authorize(credentials)
        
        # Open the specific spreadsheet - Client must ensure this name matches
        sheet = client.open("Invoice_Data_Sync").sheet1
        
        for entry in data_list:
            sheet.append_row([entry['Date'], entry['Total'], entry['Original Name']])
        print(f"{Colors.OKGREEN}✔ Successfully synced to Google Sheets!{Colors.ENDC}")
    except Exception as error:
        print(f"{Colors.FAIL}✘ Google Sync Error: {error}{Colors.ENDC}")

def run_advanced_process():
    """Main process to iterate through PDFs and extract data."""
    results = []
    date_pattern = r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
    total_pattern = r'(?:Total|Amount Due|Balance)[:\s]*\$?\s*(\d+[\.,]\d{2})'

    print(f"{Colors.HEADER}{Colors.BOLD}--- omegazyph Advanced Enterprise Extractor ---{Colors.ENDC}")

    # Ensure the Invoices directory exists
    if not os.path.exists(INVOICE_DIR):
        print(f"{Colors.FAIL}Error: Directory {INVOICE_DIR} not found.{Colors.ENDC}")
        return

    # Process PDFs
    for filename in os.listdir(INVOICE_DIR):
        if filename.lower().endswith('.pdf'):
            print(f"{Colors.OKBLUE}Processing:{Colors.ENDC} {filename}...")
            file_path = os.path.join(INVOICE_DIR, filename)
            
            with pdfplumber.open(file_path) as pdf:
                text = "".join([page.extract_text() or "" for page in pdf.pages])
                date_match = re.search(date_pattern, text)
                total_match = re.search(total_pattern, text, re.IGNORECASE)
                
                date_value = date_match.group(1) if date_match else "Unknown"
                total_value = total_match.group(1) if total_match else "0.00"

                results.append({'Original Name': filename, 'Date': date_value, 'Total': total_value})

    if results:
        # --- PANDAS INTEGRATION ---
        # Ensure Results directory exists
        if not os.path.exists(RESULTS_DIR):
            os.makedirs(RESULTS_DIR)
            print(f"{Colors.OKBLUE}Created results directory.{Colors.ENDC}")

        # Convert results to a DataFrame
        data_frame = pd.DataFrame(results)
        
        # Save local CSV in the /results folder
        backup_path = os.path.join(RESULTS_DIR, "invoice_summary_backup.csv")
        data_frame.to_csv(backup_path, index=False)
        print(f"{Colors.OKGREEN}✔ Local CSV backup created in /results folder.{Colors.ENDC}")
        
        # Proceed to Cloud Sync
        sync_to_google_sheets(results)
    else:
        print(f"{Colors.WARNING}No PDF invoices found in the directory.{Colors.ENDC}")

if __name__ == "__main__":
    # Enable ANSI colors for Windows 11 terminal
    os.system('color') 
    
    # Check if the credentials file exists in the config folder
    if os.path.exists(CREDENTIALS_FILE):
        run_advanced_process()
    else:
        print(f"{Colors.FAIL}Error: credentials.json not found in /config folder.{Colors.ENDC}")