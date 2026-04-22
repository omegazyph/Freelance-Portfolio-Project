# 📑 Invoice Data Extractor & Organizer (Standard)

Author: omegazyph | Updated: 2026-02-17

## ✨ Standard Tier Exclusive Features

* **One-Click Launch:** Includes `Start_Extractor.bat` for easy execution.
* **Auto-File Renaming:** Automatically renames PDFs to `YYYY-MM-DD_Amount.pdf` for better archiving.
* **CSV Reporting:** Full data extraction to `results/Standard_Report.csv`.
* **Clean Architecture:** Organized folder structure separating logic, config, and data.

## 📂 Project Structure

 **config/**: Contains `requirements.txt` (Dependency list).
 **Invoices/**: Place your source PDF invoices here.
 **results/**: Your generated CSV reports will be saved here.
 **scripts/**: Core Python logic and cleanup utilities.

## 🚀 Usage

### Windows 11 (VSCode/Terminal)

1. **Setup**: Double-click `setup_windows.bat`. This installs libraries from the `config/` folder.
2. **Prepare**: Place PDFs in the `Invoices/` folder.
3. **Run**: Double-click `Start_Extractor.bat`.
4. **Result**: Your PDFs will be renamed in-place and a CSV will be ready in `results/`.

### Linux (Parrot OS)

1. **Permissions**: Run `chmod +x *.sh`.
2. **Setup**: Run `./setup_linux.sh`.
3. **Run**: Run `./start_extractor.sh`.

---
> **Note:** This tool renames files in the `Invoices/` folder. It is recommended to keep a backup of your original files.
