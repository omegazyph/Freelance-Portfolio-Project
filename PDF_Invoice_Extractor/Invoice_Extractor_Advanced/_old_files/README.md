# Omegazyph Advanced Invoice Extractor (Enterprise Tier)

An automated solution for extracting data from PDF invoices, generating local CSV backups, and syncing data directly to Google Sheets.

## 📂 Project Structure

- **config/**: Contains `requirements.txt` and your `credentials.json`.
- **Invoices/**: Place all your PDF invoices here before running.
- **results/**: Your local CSV backups will be saved here automatically.
- **scripts/**: Core logic and cleanup utilities.

## 🚀 Quick Start (Windows 11)

1. **Setup**: Double-click `setup_windows.bat` to install dependencies.
2. **Configure**: Place your Google API `credentials.json` into the `config/` folder.
3. **Run**: Place your PDFs in the `Invoices/` folder and double-click `Start_Extractor.bat`.

## 🐧 Quick Start (Linux/Parrot OS)

1. **Permissions**: Run `chmod +x *.sh` in the root folder.
2. **Setup**: Run `./setup_linux.sh`.
3. **Run**: Run `./start_extractor.sh`.

## ☁️ Google Sheets Sync

To enable cloud sync:

1. Create a Google Cloud Service Account.
2. Download the JSON key and rename it to `credentials.json`.
3. Move it to the `config/` folder.
4. Create a Google Sheet named **"Invoice_Data_Sync"** and share it with the `client_email` found in your JSON file.

---
    *Created by omegazyph - 2026-02-17*
    