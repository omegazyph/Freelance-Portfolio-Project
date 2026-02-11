# ==============================================================================
# Date:         2026-02-11
# Script Name:  Invoice_Extractor.py
# Author:       omegazyph
# Updated:      2026-02-11
# Description:  Professional PDF data extraction for automated accounting.
# ==============================================================================

import pdfplumber
import os
import csv

# --- CONFIGURATION (Matches Structure) ---
SOURCE_DIR = "Invoices"
OUTPUT_DIR = "Output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "Extracted_Data.csv")

def run_extraction():
    # Ensure folders exist
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    
    results = []
    print(f"[*] Scanning {SOURCE_DIR}...")

    for filename in os.listdir(SOURCE_DIR):
        if filename.endswith(".pdf"):
            path = os.path.join(SOURCE_DIR, filename)
            with pdfplumber.open(path) as pdf:
                text = pdf.pages[0].extract_text()
                # Basic search logic (can be customized for client)
                print(f"[SUCCESS] Processed: {filename}")
                results.append({"File": filename, "Content_Snippet": text[:50].replace('\n', ' ')})

    # Save Results
    with open(OUTPUT_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["File", "Content_Snippet"])
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    run_extraction()