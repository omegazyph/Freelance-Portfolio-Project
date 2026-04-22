# Date: 2026-03-08
# Author: omegazyph
# Description: Advanced GUI Invoice Extractor with JSON Config & Google Sync

import os
import re
import json
import pdfplumber
import pandas as pd
import gspread
import customtkinter as ctk
from tkinter import filedialog, messagebox
from google.oauth2.service_account import Credentials

# --- THEME & PATHS ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, 'config', 'config.json')
CREDS_FILE = os.path.join(BASE_DIR, 'config', 'credentials.json')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

class InvoiceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Omegazyph Advanced Invoice Extractor")
        self.geometry("800x600")

        # Load JSON Config
        self.settings = self.load_config()

        # UI State
        self.target_folder = ctk.StringVar(value="No folder selected")
        
        # --- UI LAYOUT ---
        self.grid_columnconfigure(0, weight=1)
        self.header = ctk.CTkLabel(self, text="INVOICE DATA SYNC PRO", font=("Arial", 28, "bold"))
        self.header.grid(row=0, column=0, pady=20)

        # Folder Picker
        self.picker_frame = ctk.CTkFrame(self)
        self.picker_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_browse = ctk.CTkButton(self.picker_frame, text="Browse Invoices", command=self.browse)
        self.btn_browse.pack(side="left", padx=10, pady=10)
        
        self.lbl_path = ctk.CTkLabel(self.picker_frame, textvariable=self.target_folder)
        self.lbl_path.pack(side="left", padx=10)

        # Console Output
        self.console = ctk.CTkTextbox(self, width=700, height=250, font=("Consolas", 12))
        self.console.grid(row=2, column=0, padx=20, pady=10)
        self.log("SYSTEM READY: Config loaded.")

        # Action Button
        self.btn_run = ctk.CTkButton(self, text="START EXTRACTION & CLOUD SYNC", 
                                     height=50, fg_color="#2ecc71", hover_color="#27ae60",
                                     command=self.process)
        self.btn_run.grid(row=3, column=0, pady=20)

    def load_config(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                return json.load(f)
        return {"google_sheets": {"spreadsheet_name": "Invoice_Data_Sync"}}

    def log(self, text):
        self.console.insert("end", f"> {text}\n")
        self.console.see("end")
        self.update_idletasks()

    def browse(self):
        folder = filedialog.askdirectory()
        if folder: 
            self.target_folder.set(folder)

    def google_sync(self, data):
        sheet_name = self.settings["google_sheets"]["spreadsheet_name"]
        self.log(f"Accessing Google Sheet: {sheet_name}...")
        
        try:
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = Credentials.from_service_account_file(CREDS_FILE, scopes=scope)
            client = gspread.authorize(creds)
            
            sheet = client.open(sheet_name).get_worksheet(0)
            
            for row in data:
                sheet.append_row([row['File'], row['Date'], row['Total']])
            
            self.log("SUCCESS: Cloud Sync verified.")
        except Exception as e:
            self.log(f"SYNC ERROR: {str(e)}")

    def process(self):
        folder = self.target_folder.get()
        if folder == "No folder selected":
            messagebox.showwarning("Error", "Please select an invoice folder.")
            return

        self.log(f"Scanning folder: {folder}")
        files = [f for f in os.listdir(folder) if f.endswith('.pdf')]
        
        if not files:
            self.log("No PDFs found!")
            return

        results = []
        # Pull patterns from JSON
        date_re = self.settings["extraction_settings"]["date_pattern"]
        total_re = self.settings["extraction_settings"]["total_pattern"]

        for f in files:
            full_path = os.path.join(folder, f)
            with pdfplumber.open(full_path) as pdf:
                text = pdf.pages[0].extract_text()
                date = re.search(date_re, text)
                total = re.search(total_re, text)
                
                entry = {
                    "File": f,
                    "Date": date.group(1) if date else "N/A",
                    "Total": total.group(1) if total else "0.00"
                }
                results.append(entry)
                self.log(f"Parsed: {f}")

        # Local Save
        df = pd.DataFrame(results)
        os.makedirs(RESULTS_DIR, exist_ok=True)
        df.to_csv(os.path.join(RESULTS_DIR, "latest_results.csv"), index=False)
        
        # Cloud Sync
        self.google_sync(results)
        messagebox.showinfo("Complete", f"Processed {len(results)} invoices.")

if __name__ == "__main__":
    app = InvoiceApp()
    app.mainloop()