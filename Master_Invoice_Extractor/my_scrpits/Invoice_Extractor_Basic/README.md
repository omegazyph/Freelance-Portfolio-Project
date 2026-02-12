# 📑 Invoice Data Extractor (Basic)

Automated PDF-to-CSV Extraction Utility
Author: omegazyph | Updated: 2026-02-11

## 📝 Description

A professional Python-based utility designed to extract key financial data (Date and Total Amount) from PDF invoices. This script uses `pdfplumber` and Regular Expressions to identify data patterns and compile them into a structured report.

## ✨ Key Features

* **Batch Processing:** Scans multiple PDFs in seconds.
* **Regex Intelligence:** Extracts "Total Due" and "Date" fields automatically.
* **Structured Output:** Generates a clean `Extracted_Data.csv` in the Output folder.

## 📂 Project Structure

* **Invoices/**: Place your source PDF files here.
* **Scripts/**: Contains the Python logic (`Invoice_Extractor_Basic.py`).
* **Output/**: Your final CSV report will be generated here.

## 🚀 Installation & Usage

1. **Requirements:** Ensure Python is installed.
2. **Install Libraries:** Run `pip install -r requirements.txt` in your terminal.
3. **Execution:** Run the following command from the project root:
   `python Scripts/Invoice_Extractor_Basic.py`

---
*Note: This is the Basic Tier delivery. For automated file renaming or Windows one-click launchers, please refer to the Standard/Advanced service tiers.*