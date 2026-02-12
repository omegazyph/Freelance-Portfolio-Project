"""
Date:         2026-02-11
Script Name:  Invoice_Extractor_Standard.py
Author:       omegazyph
Updated:      2026-02-11
Description:  Standard Tier: Extracts data to CSV AND renames PDF files 
              to a standardized format (YYYY-MM-DD_Amount.pdf).
"""

import pdfplumber
import pandas as pd
import re
import os
#import shutil

# Set up paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVOICE_DIR = os.path.join(BASE_DIR, 'Invoices')
OUTPUT_DIR = os.path.join(BASE_DIR, 'Output')

def initialize():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def run_standard_process():
    results = []
    date_regex = r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
    total_regex = r'(?:Total|Amount Due|Balance)[:\s]*\$?\s*(\d+[\.,]\d{2})'

    print("--- omegazyph Standard Extractor & Organizer ---")

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
                # Renames file to: 2026-02-11_150.00.pdf
                new_name = f"{date_val}_{total_val}.pdf"
                new_path = os.path.join(INVOICE_DIR, new_name)
                
                # Check if name already exists to avoid overwriting
                if not os.path.exists(new_path):
                    os.rename(path, new_path)
                    print(f"Processed & Renamed: {new_name}")
                else:
                    print(f"Processed: {filename} (New name already exists)")

            except Exception as e:
                print(f"Error: {e}")

    if results:
        pd.DataFrame(results).to_csv(os.path.join(OUTPUT_DIR, 'Report.csv'), index=False)
        print("\nCSV Report Generated in Output folder.")

if __name__ == "__main__":
    initialize()
    run_standard_process()