################################################################################
# Date: 2026-05-02
# Script Name: advanced_extractor.py
# Author: omegazyph
# Updated: 2026-05-02
# Description: Advanced automated PDF extractor for Windows. 
#              Scans a directory, extracts data, and generates a CSV report.
################################################################################

import os
import json
import csv
import re
import pdfplumber
from datetime import datetime

def load_advanced_config():
    """Load settings and ensure the environment is ready."""
    config_file = "advanced_config.json"
    
    if not os.path.exists(config_file):
        print(f"ERROR: Configuration file '{config_file}' is missing.")
        exit()
        
    with open(config_file, "r") as file:
        return json.load(file)

def setup_directories(settings):
    """Create folders if they do not exist."""
    input_path = settings["input_folder_path"]
    output_path = settings["output_folder_path"]
    
    if not os.path.exists(input_path):
        os.makedirs(input_path)
        print(f"Created input folder: {input_path}")
        
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Created output folder: {output_path}")

def extract_data_from_pdf(pdf_path):
    """Open a PDF and look for common invoice patterns."""
    extracted_information = {
        "FileName": os.path.basename(pdf_path),
        "ExtractionDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "InvoiceDate": "Not Found",
        "TotalAmount": "0.00"
    }

    try:
        with pdfplumber.open(pdf_path) as pdf:
            # We examine the first page for header information
            first_page = pdf.pages[0]
            text_content = first_page.extract_text()

            if text_content:
                # Look for a date pattern (MM/DD/YYYY or YYYY-MM-DD)
                date_search = re.search(r"(\d{1,4}[-/]\d{1,2}[-/]\d{2,4})", text_content)
                if date_search:
                    extracted_information["InvoiceDate"] = date_search.group(1)

                # Look for a currency pattern (e.g., $1,234.56)
                money_search = re.search(r"\$(\d{1,3}(?:,\d{3})*(?:\.\d{2}))", text_content)
                if money_search:
                    extracted_information["TotalAmount"] = money_search.group(1)

    except Exception as error:
        print(f"Could not process {pdf_path}: {error}")

    return extracted_information

def run_automation():
    """The main loop that processes all files in the input folder."""
    settings = load_advanced_config()
    setup_directories(settings)
    
    input_dir = settings["input_folder_path"]
    output_file = os.path.join(settings["output_folder_path"], settings["output_filename"])
    
    # Identify all PDF files in the target folder
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]
    
    if not pdf_files:
        print("No new PDF files found to process.")
        return

    print(f"Found {len(pdf_files)} files. Starting extraction...")

    results_list = []
    for filename in pdf_files:
        full_path = os.path.join(input_dir, filename)
        data = extract_data_from_pdf(full_path)
        results_list.append(data)
        print(f"Processed: {filename}")

    # Write the results to a CSV file
    file_exists = os.path.isfile(output_file)
    with open(output_file, "a", newline="") as csv_output:
        fieldnames = ["FileName", "ExtractionDate", "InvoiceDate", "TotalAmount"]
        writer = csv.DictWriter(csv_output, fieldnames=fieldnames)
        
        # Only write the header if the file is new
        if not file_exists:
            writer.writeheader()
            
        for row in results_list:
            writer.writerow(row)

    print(f"Automation Complete. Results saved to: {output_file}")

if __name__ == "__main__":
    run_automation()