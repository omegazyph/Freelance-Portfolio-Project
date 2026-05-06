################################################################################
# Date: 2026-05-02
# Script Name: advanced_extractor_gui_19.py
# Author: omegazyph
# Updated: 2026-05-06
# Description: Professional Enterprise UI for PDF Invoice Extraction.
#              Strict Dependency: Requires advanced_config.json to execute.
#              Features: Dual CSV/Excel Export with Auto-Adjusting Columns.
################################################################################

import os
import json
import csv
import re
import pdfplumber
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk 
from datetime import datetime
import sys

class ProfessionalExtractorGUI:
    def __init__(self, root):
        """
        Initialize the main application window and strictly load configurations.
        """
        self.root = root
        
        try:
            if getattr(sys, 'frozen', False):
                self.base_path = os.path.dirname(sys.executable)
            else:
                self.base_path = os.path.dirname(os.path.abspath(__file__))
            
            self.config_path = os.path.join(self.base_path, "advanced_config.json")
            self.settings = self.load_settings()
            
        except Exception as startup_error:
            root_helper = tk.Tk()
            root_helper.withdraw()
            messagebox.showerror(
                "Critical Start Failure", 
                f"The application could not initialize because of a configuration error:\n\n{startup_error}"
            )
            sys.exit()

        self.root.title(f"{self.settings.get('author')} | {self.settings.get('version_type')}")
        self.root.geometry(self.settings.get("window_geometry"))
        self.root.configure(bg="#f0f2f5") 

        self.style = ttk.Style()
        self.style.theme_use(self.settings.get("ui_theme")) 
        self.style.configure("TButton", font=("Segoe UI", 10))
        self.style.configure(
            "Header.TLabel", 
            font=("Segoe UI", 18, "bold"), 
            background="#f0f2f5", 
            foreground=self.settings.get("header_color", "#1a73e8")
        )
        self.style.configure("TProgressbar", thickness=20)

        self.create_ui()

    def load_settings(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Missing required file: {self.config_path}")
        try:
            with open(self.config_path, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as error:
            raise Exception(f"Failed to parse advanced_config.json: {error}")

    def save_settings(self):
        try:
            with open(self.config_path, "w") as file:
                json.dump(self.settings, file, indent=4)
        except Exception as save_error:
            self.log(f"Warning: Could not save session settings: {save_error}")

    def create_ui(self):
        main_frame = tk.Frame(self.root, bg="#f0f2f5", padx=20, pady=10)
        main_frame.pack(expand=True, fill="both")

        branding_frame = tk.Frame(main_frame, bg="#f0f2f5")
        branding_frame.pack(fill="x", pady=(5, 15))

        logo_path = os.path.join(self.base_path, "logo.png")
        try:
            self.logo_image = tk.PhotoImage(file=logo_path).subsample(9, 9)
            tk.Label(branding_frame, image=self.logo_image, bg="#f0f2f5").pack(side="top", pady=(0, 5))
        except Exception:
            pass

        ttk.Label(branding_frame, text=self.settings.get("header_name", "PDF Data Automation Suite"), style="Header.TLabel").pack(side="top", pady=5)

        selection_frame = tk.LabelFrame(main_frame, text=" Configuration Settings ", bg="white", font=("Segoe UI", 10, "bold"), padx=15, pady=15)
        selection_frame.pack(fill="x", pady=5)

        ttk.Label(selection_frame, text="Source Folder (PDFs):", background="white").pack(anchor="w")
        input_row = tk.Frame(selection_frame, bg="white")
        input_row.pack(fill="x", pady=(0, 10))
        self.input_entry = ttk.Entry(input_row)
        self.input_entry.insert(0, self.settings.get("last_input_folder", ""))
        self.input_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(input_row, text="Browse", command=self.browse_input).pack(side="right")

        ttk.Label(selection_frame, text="Destination Folder (Results):", background="white").pack(anchor="w")
        output_row = tk.Frame(selection_frame, bg="white")
        output_row.pack(fill="x")
        self.output_entry = ttk.Entry(output_row)
        self.output_entry.insert(0, self.settings.get("last_output_folder", ""))
        self.output_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(output_row, text="Browse", command=self.browse_output).pack(side="right")

        self.progress_label = ttk.Label(main_frame, text="System Ready", background="#f0f2f5", font=("Segoe UI", 9))
        self.progress_label.pack(anchor="w", pady=(15, 0))
        self.progress_bar = ttk.Progressbar(main_frame, orient="horizontal", mode="determinate")
        self.progress_bar.pack(fill="x", pady=5)

        work_area = tk.Frame(main_frame, bg="#f0f2f5")
        work_area.pack(expand=True, fill="both", pady=10)

        button_sidebar = tk.Frame(work_area, bg="#f0f2f5")
        button_sidebar.pack(side="left", fill="y", padx=(0, 15))

        self.run_button = tk.Button(button_sidebar, text="EXECUTE", bg="#1a73e8", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", height=2, width=20, command=self.run_process)
        self.run_button.pack(pady=5)

        self.source_button = tk.Button(button_sidebar, text="SOURCE FOLDER", bg="#5f6368", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", height=2, width=20, command=self.open_source_folder)
        self.source_button.pack(pady=5)

        self.open_button = tk.Button(button_sidebar, text="OPEN EXCEL", bg="#1a73e8", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", height=2, width=20, state="disabled", command=self.open_result_file)
        self.open_button.pack(pady=5)

        self.log_area = scrolledtext.ScrolledText(work_area, width=50, height=12, font=("Consolas", 10), bg="#ffffff", fg="#333333", borderwidth=1, relief="solid")
        self.log_area.pack(expand=True, fill="both")

        tk.Label(main_frame, text=f"Author: {self.settings.get('author')} | PDF Extraction Suite", bg="#f0f2f5", fg="#666666", font=("Segoe UI", 8)).pack(pady=(5, 0))

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

    def open_result_file(self):
        path = os.path.join(self.output_entry.get(), "master_invoice_report.xlsx")
        if os.path.exists(path):
            try:
                os.startfile(path)
            except Exception as e:
                self.log(f"Error opening report: {e}")

    def open_source_folder(self):
        path = self.input_entry.get()
        if os.path.exists(path):
            try:
                os.startfile(path)
            except Exception as e:
                self.log(f"Error opening source folder: {e}")

    def run_process(self):
        in_dir = self.input_entry.get()
        out_dir = self.output_entry.get()
        fieldnames = self.settings.get("report_headers")

        if not os.path.exists(in_dir) or not os.path.exists(out_dir):
            messagebox.showwarning("Error", "Invalid folder paths.")
            return

        self.settings["last_input_folder"] = in_dir
        self.settings["last_output_folder"] = out_dir
        self.save_settings()

        pdf_files = [f for f in os.listdir(in_dir) if f.lower().endswith(".pdf")]
        if not pdf_files:
            self.log("No PDFs found.")
            return

        patterns = self.settings.get("extraction_patterns")
        date_regexes = patterns.get("date_patterns")
        amount_regexes = patterns.get("amount_patterns")

        self.progress_bar["maximum"] = len(pdf_files)
        self.progress_bar["value"] = 0
        self.run_button.config(state="disabled")

        output_file_csv = os.path.join(out_dir, "master_invoice_report.csv")
        output_file_xlsx = os.path.join(out_dir, "master_invoice_report.xlsx")

        try:
            # Step 1: Process PDFs to CSV
            with open(output_file_csv, "w", newline="") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

                for index, filename in enumerate(pdf_files, 1):
                    self.log(f"Processing: {filename}")
                    full_path = os.path.join(in_dir, filename)
                    
                    invoice_date = "N/A"
                    total_amount = "0.00"
                    status = "Success"

                    try:
                        with pdfplumber.open(full_path) as pdf:
                            full_text = "".join([page.extract_text() or "" for page in pdf.pages])

                            if len(full_text.strip()) < 10:
                                status = "Scanned Image - No Text"
                            else:
                                for pattern in date_regexes:
                                    match = re.search(pattern, full_text, re.IGNORECASE)
                                    if match:
                                        invoice_date = match.group(1)
                                        break 

                                for pattern in amount_regexes:
                                    match = re.search(pattern, full_text, re.IGNORECASE)
                                    if match:
                                        total_amount = match.groups()[-1]
                                        break

                        writer.writerow({
                            fieldnames[0]: filename,
                            fieldnames[1]: datetime.now().strftime("%Y-%m-%d"),
                            fieldnames[2]: invoice_date,
                            fieldnames[3]: total_amount,
                            fieldnames[4]: status
                        })
                    except Exception as extraction_err:
                        self.log(f"Error in {filename}: {extraction_err}")
                    
                    self.progress_bar["value"] = index
                    self.root.update_idletasks()

            self.log("CSV Report generated.")

            # Step 2: Convert to Excel with Auto-Adjust
            self.log("Converting to Excel and formatting...")
            df = pd.read_csv(output_file_csv)
            with pd.ExcelWriter(output_file_xlsx, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Invoices')
                worksheet = writer.sheets['Invoices']
                
                for idx, col in enumerate(df.columns):
                    series = df[col]
                    max_len = max((
                        series.astype(str).map(len).max(),
                        len(str(series.name))
                    )) + 2
                    worksheet.column_dimensions[chr(65 + idx)].width = max_len

            self.log("Final Report Ready (Excel).")
            self.open_button.config(state="normal")
            
            if self.settings.get("auto_open_report"):
                self.open_result_file()

        except Exception as e:
            self.log(f"Critical System Error: {e}")
        finally:
            self.run_button.config(state="normal")

if __name__ == "__main__":
    app_root = tk.Tk()
    ProfessionalExtractorGUI(app_root)
    app_root.mainloop()