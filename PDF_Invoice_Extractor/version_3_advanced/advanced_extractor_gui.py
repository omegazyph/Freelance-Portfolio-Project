################################################################################
# Date: 2026-05-02
# Script Name: advanced_extractor_gui.py
# Author: omegazyph
# Updated: 2026-05-02
# Description: Professional UI for PDF Invoice Extraction.
#              Features a modern layout, themed colors, and robust logging.
################################################################################

import os
import json
import csv
import re
import pdfplumber
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk  # Used for modern themed widgets
from datetime import datetime

class ProfessionalExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("omegazyph | Enterprise PDF Extractor")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f2f5")  # Light grey/blue professional background

        # Configuration Loading
        self.config_path = "advanced_config.json"
        self.settings = self.load_settings()

        # Styles
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), background="#f0f2f5", foreground="#1a73e8")

        self.create_ui()

    def load_settings(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as file:
                return json.load(file)
        return {"last_input_folder": "", "last_output_folder": ""}

    def save_settings(self):
        with open(self.config_path, "w") as file:
            json.dump(self.settings, file, indent=4)

    def create_ui(self):
        # Main Container
        main_frame = tk.Frame(self.root, bg="#f0f2f5", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        # Header Section
        header = ttk.Label(main_frame, text="PDF Data Automation Suite", style="Header.TLabel")
        header.pack(pady=(0, 20))

        # Folder Selection Section (Card Style)
        selection_frame = tk.LabelFrame(main_frame, text=" Configuration Settings ", bg="white", font=("Segoe UI", 10, "bold"), padx=15, pady=15)
        selection_frame.pack(fill="x", pady=10)

        # Input Row
        ttk.Label(selection_frame, text="Source Folder (PDFs):", background="white").pack(anchor="w")
        input_row = tk.Frame(selection_frame, bg="white")
        input_row.pack(fill="x", pady=(0, 10))
        self.input_entry = ttk.Entry(input_row)
        self.input_entry.insert(0, self.settings.get("last_input_folder", ""))
        self.input_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(input_row, text="Browse", command=self.browse_input).pack(side="right")

        # Output Row
        ttk.Label(selection_frame, text="Destination Folder (CSV):", background="white").pack(anchor="w")
        output_row = tk.Frame(selection_frame, bg="white")
        output_row.pack(fill="x")
        self.output_entry = ttk.Entry(output_row)
        self.output_entry.insert(0, self.settings.get("last_output_folder", ""))
        self.output_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(output_row, text="Browse", command=self.browse_output).pack(side="right")

        # Execution Section
        self.run_btn = tk.Button(main_frame, text="EXECUTE AUTOMATION", bg="#1a73e8", fg="white", 
                                font=("Segoe UI", 12, "bold"), relief="flat", height=2, cursor="hand2",
                                command=self.run_process)
        self.run_btn.pack(fill="x", pady=20)

        # Log Section
        tk.Label(main_frame, text="Process Activity Log", bg="#f0f2f5", font=("Segoe UI", 9, "italic")).pack(anchor="w")
        self.log_area = scrolledtext.ScrolledText(main_frame, width=70, height=12, font=("Consolas", 10), 
                                                 bg="#ffffff", fg="#333333", borderwidth=1, relief="solid")
        self.log_area.pack(expand=True, fill="both")

        # Footer
        tk.Label(main_frame, text=f"Author: {self.settings.get('author', 'omegazyph')}", 
                 bg="#f0f2f5", fg="#666666", font=("Segoe UI", 8)).pack(pady=(10, 0))

    def browse_input(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, folder)

    def browse_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder)

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_area.see(tk.END)
        self.root.update_idletasks()

    def run_process(self):
        input_dir = self.input_entry.get()
        output_dir = self.output_entry.get()

        if not os.path.exists(input_dir) or not input_dir:
            messagebox.showwarning("Incomplete Path", "Please select a valid input folder.")
            return

        # Update and save settings
        self.settings["last_input_folder"] = input_dir
        self.settings["last_output_folder"] = output_dir
        self.save_settings()

        self.log("Initializing scanning engine...")
        
        pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]
        if not pdf_files:
            self.log("Notice: No PDF files found in the source directory.")
            return

        output_file = os.path.join(output_dir, "master_invoice_report.csv")
        
        try:
            with open(output_file, "a", newline="") as csv_file:
                fieldnames = ["FileName", "ProcessedDate", "InvoiceDate", "Amount"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                
                if os.path.getsize(output_file) == 0 if os.path.exists(output_file) else True:
                    writer.writeheader()

                for filename in pdf_files:
                    self.log(f"Extracting: {filename}")
                    full_path = os.path.join(input_dir, filename)
                    
                    with pdfplumber.open(full_path) as pdf:
                        text = pdf.pages[0].extract_text()
                        
                        date_match = re.search(r"(\d{1,4}[-/]\d{1,2}[-/]\d{2,4})", text)
                        money_match = re.search(r"\$(\d{1,3}(?:,\d{3})*(?:\.\d{2}))", text)
                        
                        writer.writerow({
                            "FileName": filename,
                            "ProcessedDate": datetime.now().strftime("%Y-%m-%d"),
                            "InvoiceDate": date_match.group(1) if date_match else "N/A",
                            "Amount": money_match.group(1) if money_match else "0.00"
                        })
            
            self.log("Success: Report updated.")
            messagebox.showinfo("Task Complete", "Extraction finished successfully.")

        except Exception as e:
            self.log(f"Process Error: {str(e)}")
            messagebox.showerror("System Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app_root = tk.Tk()
    ProfessionalExtractorGUI(app_root)
    app_root.mainloop()