"""
Date:           2026-02-11
Script Name:    Create_Samples.py
Author:         omegazyph
Updated:        2026-02-11
Description:    Generates mock PDF invoices for testing the Extractor.
                Ensures absolute pathing for reliable file generation.
"""

from fpdf import FPDF
import os

# Identify the directory where this script is currently located
# This represents the "Log_Monitor_System/scripts" folder
script_directory = os.path.dirname(os.path.abspath(__file__))

# Navigate up one level to reach the main project root directory
# This represents the "Log_Monitor_System" folder
project_root = os.path.dirname(script_directory)

# Define the absolute path to the Invoices folder
invoice_folder_path = os.path.join(project_root, "Invoices")

# Ensure the Invoices folder exists
if not os.path.exists(invoice_folder_path):
    os.makedirs(invoice_folder_path)

def create_invoice(filename, date, total, vendor):
    """
    Generates a PDF document with vendor and total amount details.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"INVOICE: {vendor}", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Date: {date}", ln=True)
    pdf.cell(200, 10, txt=f"Vendor: {vendor}", ln=True)
    pdf.ln(20)
    
    # This is the line your Extractor looks for
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"Total Balance Due: ${total}", ln=True)
    
    # FIX: Use the absolute path defined above to save the file
    full_output_path = os.path.join(invoice_folder_path, filename)
    
    pdf.output(full_output_path)
    print(f"Generated: {full_output_path}")

# Generate test cases
create_invoice("Invoice_001.pdf", "02/10/2026", "450.00", "TechSupplies Co")
create_invoice("Invoice_002.pdf", "01/15/2026", "1,200.50", "Cloud Services Ltd")
create_invoice("Invoice_003.pdf", "12/20/2025", "75.25", "Office Depot")

print(f"\nSuccess! 3 sample invoices are now in: {invoice_folder_path}")