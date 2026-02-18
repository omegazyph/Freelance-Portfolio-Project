"""
Date:         2026-02-17
Script Name:  Invoice_Extractor_Basic.py
Author:       omegazyph
Updated:      2026-02-17
Description:  Starter Tier: Extracts Date and Total Amount from PDF 
              invoices and saves the data to a structured CSV file.
"""

import pdfplumber
import pandas as pd
import re
import os

# ANSI Color Codes for Professional Terminal Output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# Define directory structure
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVOICE_FOLDER = os.path.join(BASE_DIR, "Invoices")
RESULTS_FOLDER = os.path.join(BASE_DIR, "results")

def setup_directories():
    if not os.path.exists(RESULTS_FOLDER):
        os.makedirs(RESULTS_FOLDER)
    if not os.path.exists(INVOICE_FOLDER):
        os.makedirs(INVOICE_FOLDER)

def extract_invoice_data():
    data_list = []
    date_regex = r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"
    total_regex = r"(?:Total|Amount Due|Balance)[:\s]*\$?\s*(\d+[\.,]\d{2})"

    print(f"{Colors.HEADER}{Colors.BOLD}--- omegazyph Invoice Extractor (Basic) ---{Colors.ENDC}")

    if not os.path.exists(INVOICE_FOLDER) or not os.listdir(INVOICE_FOLDER):
        print(f"{Colors.WARNING}No PDF invoices found in /Invoices.{Colors.ENDC}")
        return

    for file in os.listdir(INVOICE_FOLDER):
        if file.lower().endswith(".pdf"):
            full_path = os.path.join(INVOICE_FOLDER, file)
            try:
                with pdfplumber.open(full_path) as pdf:
                    content = "".join([page.extract_text() or "" for page in pdf.pages])
                    found_date = re.search(date_regex, content)
                    found_total = re.search(total_regex, content, re.IGNORECASE)

                    data_list.append({
                        "File Name": file,
                        "Date": found_date.group(1) if found_date else "Not Found",
                        "Total Amount": found_total.group(1) if found_total else "Not Found"
                    })
                    print(f"{Colors.OKBLUE}✔ Processed:{Colors.ENDC} {file}")
            except Exception as e:
                print(f"{Colors.FAIL}✘ Error reading {file}: {e}{Colors.ENDC}")

    if data_list:
        df = pd.DataFrame(data_list)
        csv_output = os.path.join(RESULTS_FOLDER, "Extracted_Data.csv")
        df.to_csv(csv_output, index=False)
        print(f"\n{Colors.OKGREEN}Task Complete! Data saved to: {csv_output}{Colors.ENDC}")

if __name__ == "__main__":
    os.system('color') # Enable Windows colors
    setup_directories()
    extract_invoice_data()