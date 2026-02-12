"""
Date:         2026-02-11
Script Name:  Invoice_Extractor_Basic.py
Author:       omegazyph
Updated:      2026-02-11
Description:  Starter Tier: Extracts Date and Total Amount from PDF 
              invoices and saves the data to a structured CSV file.
"""

import pdfplumber
import pandas as pd
import re
import os

# Define project directory structure relative to this script location
# This ensures it runs correctly on the client's machine
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVOICE_FOLDER = os.path.join(BASE_DIR, "Invoices")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "Output")

def setup_directories():
    """Initializes the environment by ensuring the Output folder exists."""
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

def extract_invoice_data():
    """Main logic to scan PDFs and pull data using Regular Expressions (Regex)."""
    data_list = []
    
    # Regex Patterns: 
    # Date: Matches MM/DD/YYYY, DD/MM/YYYY, or YYYY-MM-DD
    # Total: Looks for Total/Amount/Balance followed by currency and numbers
    date_regex = r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"
    total_regex = r"(?:Total|Amount Due|Balance)[:\s]*\$?\s*(\d+[\.,]\d{2})"

    print("--- omegazyph Invoice Extractor (Basic) ---")
    print(f"Scanning Directory: {INVOICE_FOLDER}")

    # Iterate through PDF files
    for file in os.listdir(INVOICE_FOLDER):
        if file.lower().endswith(".pdf"):
            full_path = os.path.join(INVOICE_FOLDER, file)
            
            try:
                with pdfplumber.open(full_path) as pdf:
                    # Extract text from every page of the document
                    content = ""
                    for page in pdf.pages:
                        content += page.extract_text() or ""

                    # Apply Regex searches
                    found_date = re.search(date_regex, content)
                    found_total = re.search(total_regex, content, re.IGNORECASE)

                    # Append findings to the list
                    data_list.append({
                        "File Name": file,
                        "Date": found_date.group(1) if found_date else "Not Found",
                        "Total Amount": found_total.group(1) if found_total else "Not Found"
                    })
                    print(f"Successfully processed: {file}")
            except Exception as e:
                print(f"Could not read {file}: {e}")

    # Export results to CSV
    if data_list:
        df = pd.DataFrame(data_list)
        csv_output = os.path.join(OUTPUT_FOLDER, "Extracted_Data.csv")
        df.to_csv(csv_output, index=False)
        print(f"\nTask Complete! Data saved to: {csv_output}")
    else:
        print("\nNo data extracted. Please ensure PDFs are in the Invoices folder.")

if __name__ == "__main__":
    setup_directories()
    extract_invoice_data()