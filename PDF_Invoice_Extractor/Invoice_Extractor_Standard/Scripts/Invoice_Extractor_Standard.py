"""
Date:         2026-02-17
Script Name:  Invoice_Extractor_Standard.py
Author:       omegazyph
Updated:      2026-02-17
Description:  Standard Tier: Extracts data to CSV AND renames PDF files 
              to a standardized format (YYYY-MM-DD_Amount.pdf).
"""

import pdfplumber
import pandas as pd
import re
import os

# ANSI Color Codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# Set up paths relative to the scripts folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVOICE_DIR = os.path.join(BASE_DIR, 'Invoices')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

def initialize():
    """Ensures necessary directories exist."""
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
    if not os.path.exists(INVOICE_DIR):
        os.makedirs(INVOICE_DIR)

def run_standard_process():
    results = []
    date_regex = r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
    total_regex = r'(?:Total|Amount Due|Balance)[:\s]*\$?\s*(\d+[\.,]\d{2})'

    print(f"{Colors.HEADER}{Colors.BOLD}--- omegazyph Standard Extractor & Organizer ---{Colors.ENDC}")

    if not os.listdir(INVOICE_DIR):
        print(f"{Colors.WARNING}No PDF invoices found in /Invoices.{Colors.ENDC}")
        return

    for filename in os.listdir(INVOICE_DIR):
        if filename.lower().endswith('.pdf'):
            path = os.path.join(INVOICE_DIR, filename)
            
            try:
                with pdfplumber.open(path) as pdf:
                    full_text = "".join([page.extract_text() or "" for page in pdf.pages])
                    
                    date_match = re.search(date_regex, full_text)
                    total_match = re.search(total_regex, full_text, re.IGNORECASE)
                    
                    date_val = date_match.group(1).replace('/', '-') if date_match else "UnknownDate"
                    total_val = total_match.group(1) if total_match else "0.00"

                    results.append({
                        'Original Name': filename,
                        'Date': date_val,
                        'Total': total_val
                    })

                # Feature: Smart Renaming
                new_name = f"{date_val}_{total_val}.pdf"
                new_path = os.path.join(INVOICE_DIR, new_name)
                
                if not os.path.exists(new_path):
                    os.rename(path, new_path)
                    print(f"{Colors.OKGREEN}✔ Renamed:{Colors.ENDC} {new_name}")
                else:
                    print(f"{Colors.OKBLUE}ℹ Processed:{Colors.ENDC} {filename} (Already Renamed)")

            except Exception as e:
                print(f"{Colors.FAIL}✘ Error processing {filename}: {e}{Colors.ENDC}")

    if results:
        report_path = os.path.join(RESULTS_DIR, 'Standard_Report.csv')
        pd.DataFrame(results).to_csv(report_path, index=False)
        print(f"\n{Colors.OKGREEN}✔ CSV Report Generated in /results folder.{Colors.ENDC}")

if __name__ == "__main__":
    os.system('color') # Enable ANSI colors in Windows
    initialize()
    run_standard_process()