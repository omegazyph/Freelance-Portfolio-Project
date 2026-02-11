# 📑 Invoice Data Extractor v1.0.0

Automated PDF-to-Excel Intelligence Utility

## 📝 Description

The Invoice Data Extractor is a professional Python-based automation tool designed to eliminate manual data entry. It scans a directory of PDF invoices, extracts key financial data (Date and Total Amount) using advanced Regular Expressions (Regex), and compiles the results into a structured CSV/Excel format.

Author: omegazyph

Updated: 2026-02-11

## ✨ Key Features

    Batch Processing: Scans hundreds of PDFs in seconds.

    Smart Detection: Uses pdfplumber and Regex to identify "Total Due" and "Date" patterns regardless of document layout.

    Structured Output: Automatically generates a clean Extracted_Data.csv in the Output folder.

    Windows Optimized: Includes a one-click .bat file for users who prefer not to use the terminal.

## 📂 Project Structure

For optimal performance, the project is organized as follows:

    Invoices/: Place all your source PDF files here.

    Scripts/: Contains the core Python logic (Invoice_Extractor.py).

    Output/: Your final CSV report will appear here.

    run_extractor.bat: The "one-click" launcher for Windows users.

## 🚀 Installation & Usage

1. Requirements

Ensure you have Python installed. You will need the following libraries:
Bash

pip install pdfplumber

2.Preparation

    Place your PDF invoices inside the Invoices folder.

    Ensure you have an Output folder created (the script will create it if missing).

3.Execution

    Windows Users: Simply double-click run_extractor.bat.

    Manual Run: Execute python Scripts/Invoice_Extractor.py from the root directory.

## 🛠 Advanced Tier Feature: Smart Renaming

In the Standard/Advanced delivery tiers, this script includes a "Document Management" module that automatically renames processed PDFs to a clean format:

YYYY-MM-DD_Invoice_Amount.pdf

This ensures your digital archives stay as organized as your spreadsheets.

© 2026 omegazyph. All rights reserved.
