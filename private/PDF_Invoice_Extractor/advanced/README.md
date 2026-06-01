# Advanced Automated Invoice Extractor

## How a Business Uses This

This tool is designed to be a "Set and Forget" solution. It monitors a specific Windows folder and converts PDF invoices into a master spreadsheet.

### Steps for the User

1. **Installation:** Run `pip install pdfplumber` in your terminal.
2. **Configure:** Open `advanced_config.json`. Update the `input_folder_path` to the folder where you save your invoices.
3. **Run:** Execute `python advanced_extractor.py`.
4. **Review:** Open the `Extracted_Results` folder. Your `final_invoice_report.csv` will be there, ready to be opened in Excel.

### Why CSV?

We use CSV because it is the "Universal Language" of business data. Whether the client uses QuickBooks, Sage, or just basic Excel, they can import this file immediately without needing special software.

### Features

* **Auto-Folder Creation:** The script builds the necessary folders if they don't exist.
* **Regex Pattern Matching:** Automatically finds dates and dollar amounts.
* **Append Mode:** New extractions are added to the bottom of the existing report so you never lose data.