################################################################################
# Date: 2026-05-05
# Script Name: test_pdf_generator.py
# Author: omegazyph
# Updated: 2026-05-05
# Description: Automated PDF generation tool for testing extraction logic.
#              Generates random invoice data to test regex robustness.
################################################################################

import os
import random
from fpdf import FPDF

class InvoiceGenerator:
    def __init__(self, project_folder="Invoice_Testing_Suite"):
        """
        Initialize the project structure for test files.
        """
        self.project_folder = project_folder
        self.input_folder = os.path.join(self.project_folder, "Test_Invoices")
        
        if not os.path.exists(self.input_folder):
            os.makedirs(self.input_folder)
            print(f"Created folder: {self.input_folder}")

    def generate_random_invoice(self, file_index):
        """
        Creates a single PDF with randomized dates and amounts.
        """
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        months = ["January", "February", "March", "April", "May", "June", 
                  "July", "August", "September", "October", "November", "December"]
        
        date_styles = [
            f"{random.randint(1, 12)}/{random.randint(1, 28)}/2026",
            f"{random.choice(months)} {random.randint(1, 28)}, 2026",
            f"2026-0{random.randint(1, 9)}-{random.randint(10, 28)}"
        ]
        
        invoice_date = random.choice(date_styles)
        amount = round(random.uniform(100.00, 5000.00), 2)
        amount_str = f"{amount:,.2f}"

        pdf.cell(200, 10, txt="GENERATED TEST INVOICE", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Invoice Number: INV-{1000 + file_index}", ln=True)
        pdf.cell(200, 10, txt=f"Date: {invoice_date}", ln=True)
        pdf.ln(10)
        pdf.cell(200, 10, txt="Description: Automated Test Freight Charges", ln=True)
        pdf.ln(20)
        
        labels = ["Total:", "Amount Due:", "Balance: $"]
        label = random.choice(labels)
        
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt=f"{label} ${amount_str}", ln=True)

        file_name = f"test_invoice_{file_index}.pdf"
        file_path = os.path.join(self.input_folder, file_name)
        pdf.output(file_path)

    def bulk_generate(self, count):
        """
        Generates a specified number of test PDFs.
        """
        print(f"Generating {count} test PDFs...")
        for i in range(1, count + 1):
            self.generate_random_invoice(i)
            if i % 10 == 0:
                print(f"Created {i} files...")
        print(f"Success! All files are in: {self.input_folder}")

if __name__ == "__main__":
    generator = InvoiceGenerator(project_folder="Invoice_Testing_Suite")
    generator.bulk_generate(50)