################################################################################
# Date: 2026-05-02
# Script Name: advanced_extractor_gui.py
# Author: omegazyph
# Updated: 2026-05-31
# Description: Professional Enterprise UI for PDF Invoice Extraction.
#              Features regular expression text parsing, runtime process
#              logging, an interactive Tkinter graphical interface, and 
#              dual CSV/Excel reporting with automated cell width calibration.
#              Strict Dependency: Requires advanced_config.json to execute.
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
        
        # Identify the base executable context pathway for file access
        if getattr(sys, 'frozen', False):
            self.base_path = os.path.dirname(sys.executable)
        else:
            self.base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Define the absolute pathway pointing to the json configuration file
        self.config_path = os.path.join(self.base_path, "..", "config", "advanced_config.json")
        
        # Normalize the file path structure to match operating system standards
        self.config_path = os.path.normpath(self.config_path)
        
        try:
            self.settings = self.load_settings()
        except Exception as startup_error:
            # Generate a temporary hidden instance window to pass error dialogue safely
            root_helper = tk.Tk()
            root_helper.withdraw()
            messagebox.showerror(
                "Critical Start Failure", 
                f"The application could not initialize because of a configuration error:\n\n{startup_error}"
            )
            sys.exit()

        # Frame setup configurations using application settings values
        self.root.title(f"{self.settings.get('author')} | {self.settings.get('version_type')}")
        self.root.geometry(self.settings.get("window_geometry"))
        self.root.configure(bg="#f0f2f5") 

        # Configure standardized widget stylings for the application interface
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

        # Build and render user interface panels
        self.create_ui()

    def load_settings(self):
        """
        Verifies and reads application data patterns and directory links from JSON.
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Missing required file: {self.config_path}")
        try:
            with open(self.config_path, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as error:
            raise Exception(f"Failed to parse advanced_config.json: {error}")

    def save_settings(self):
        """
        Saves updated directory pathways down into the configuration file.
        """
        try:
            with open(self.config_path, "w") as file:
                json.dump(self.settings, file, indent=4)
        except Exception as save_error:
            self.log(f"Warning: Could not save session settings: {save_error}")

    def create_ui(self):
        """
        Assembles all windows, inputs, text regions, logs, and user controls.
        """
        main_frame = tk.Frame(self.root, bg="#f0f2f5", padx=20, pady=10)
        main_frame.pack(expand=True, fill="both")

        branding_frame = tk.Frame(main_frame, bg="#f0f2f5")
        branding_frame.pack(fill="x", pady=(5, 15))

        # Attempt to load and fit the corporate image banner safely if available
        logo_path = os.path.join(self.base_path, "logo.png")
        try:
            self.logo_image = tk.PhotoImage(file=logo_path).subsample(9, 9)
            tk.Label(branding_frame, image=self.logo_image, bg="#f0f2f5").pack(side="top", pady=(0, 5))
        except Exception:
            # Fallback smoothly if asset is missing without disrupting system operations
            pass

        ttk.Label(
            branding_frame, 
            text=self.settings.get("header_name", "PDF Data Automation Suite"), 
            style="Header.TLabel"
        ).pack(side="top", pady=5)

        # Directory selector layout setup panels
        selection_frame = tk.LabelFrame(
            main_frame, 
            text=" Configuration Settings ", 
            bg="white", 
            font=("Segoe UI", 10, "bold"), 
            padx=15, 
            pady=15
        )
        selection_frame.pack(fill="x", pady=5)

        # Input source path elements construction
        ttk.Label(selection_frame, text="Source Folder (PDFs):", background="white").pack(anchor="w")
        input_row = tk.Frame(selection_frame, bg="white")
        input_row.pack(fill="x", pady=(0, 10))
        self.input_entry = ttk.Entry(input_row)
        self.input_entry.insert(0, self.settings.get("last_input_folder", ""))
        self.input_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(input_row, text="Browse", command=self.browse_input).pack(side="right")

        # Output target path elements construction
        ttk.Label(selection_frame, text="Destination Folder (Results):", background="white").pack(anchor="w")
        output_row = tk.Frame(selection_frame, bg="white")
        output_row.pack(fill="x")
        self.output_entry = ttk.Entry(output_row)
        self.output_entry.insert(0, self.settings.get("last_output_folder", ""))
        self.output_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(output_row, text="Browse", command=self.browse_output).pack(side="right")

        # System progress feedback indicators
        self.progress_label = ttk.Label(main_frame, text="System Ready", background="#f0f2f5", font=("Segoe UI", 9))
        self.progress_label.pack(anchor="w", pady=(15, 0))
        self.progress_bar = ttk.Progressbar(main_frame, orient="horizontal", mode="determinate")
        self.progress_bar.pack(fill="x", pady=5)

        # Workspace panel for text consoles and actions sidebar
        work_area = tk.Frame(main_frame, bg="#f0f2f5")
        work_area.pack(expand=True, fill="both", pady=10)

        button_sidebar = tk.Frame(work_area, bg="#f0f2f5")
        button_sidebar.pack(side="left", fill="y", padx=(0, 15))

        # Main operational controls construction
        self.run_button = tk.Button(
            button_sidebar, 
            text="EXECUTE", 
            bg="#1a73e8", 
            fg="white", 
            font=("Segoe UI", 11, "bold"), 
            relief="flat", 
            height=2, 
            width=20, 
            command=self.run_process
        )
        self.run_button.pack(pady=5)

        self.source_button = tk.Button(
            button_sidebar, 
            text="SOURCE FOLDER", 
            bg="#5f6368", 
            fg="white", 
            font=("Segoe UI", 11, "bold"), 
            relief="flat", 
            height=2, 
            width=20, 
            command=self.open_source_folder
        )
        self.source_button.pack(pady=5)

        self.open_button = tk.Button(
            button_sidebar, 
            text="OPEN EXCEL", 
            bg="#1a73e8", 
            fg="white", 
            font=("Segoe UI", 11, "bold"), 
            relief="flat", 
            height=2, 
            width=20, 
            state="disabled", 
            command=self.open_result_file
        )
        self.open_button.pack(pady=5)

        # Real-time execution text output stream matrix console
        self.log_area = scrolledtext.ScrolledText(
            work_area, 
            width=50, 
            height=12, 
            font=("Consolas", 10), 
            bg="#ffffff", 
            fg="#333333", 
            borderwidth=1, 
            relief="solid"
        )
        self.log_area.pack(expand=True, fill="both")

        # Footer credit label component
        tk.Label(
            main_frame, 
            text=f"Author: {self.settings.get('author')} | PDF Extraction Suite", 
            bg="#f0f2f5", 
            fg="#666666", 
            font=("Segoe UI", 8)
        ).pack(pady=(5, 0))

    def browse_input(self):
        """
        Handles interactive directory dialogue mapping for target invoices.
        """
        folder = filedialog.askdirectory()
        if folder:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, folder)

    def browse_output(self):
        """
        Handles interactive directory dialogue mapping for generated reporting output.
        """
        folder = filedialog.askdirectory()
        if folder:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder)

    def log(self, message):
        """
        Outputs synchronized timestamps alongside informational logs to the interface panel.
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_area.see(tk.END)
        self.root.update_idletasks()

    def open_result_file(self):
        """
        Launches the master spreadsheet automatically inside the native host application.
        """
        path = os.path.join(self.output_entry.get(), "master_invoice_report.xlsx")
        if os.path.exists(path):
            try:
                os.startfile(path)
            except Exception as error:
                self.log(f"Error opening report: {error}")

    def open_source_folder(self):
        """
        Opens the system file manager targeted directly at the selected input folder.
        """
        path = self.input_entry.get()
        if os.path.exists(path):
            try:
                os.startfile(path)
            except Exception as error:
                self.log(f"Error opening source folder: {error}")

    def run_process(self):
        """
        Controls text analysis workflows across targeted PDF invoice targets.
        """
        in_dir = self.input_entry.get()
        out_dir = self.output_entry.get()
        fieldnames = self.settings.get("report_headers")

        # Confirm targeted pathways are valid system routes before running data operations
        if not os.path.exists(in_dir) or not os.path.exists(out_dir):
            messagebox.showwarning("Error", "Invalid folder paths.")
            return

        # Ensure dynamic system configuration adjustments carry across processing updates
        self.settings["last_input_folder"] = in_dir
        self.settings["last_output_folder"] = out_dir
        self.save_settings()

        # Build clean collections containing only target files matching standard PDF metrics
        pdf_files = []
        for file in os.listdir(in_dir):
            if file.lower().endswith(".pdf"):
                pdf_files.append(file)

        if not pdf_files:
            self.log("No PDFs found inside target directory.")
            return

        # Fetch configured regular expression validation arrays
        patterns = self.settings.get("extraction_patterns")
        date_regexes = patterns.get("date_patterns")
        amount_regexes = patterns.get("amount_patterns")

        # Configure the execution visual progress indicator
        self.progress_bar["maximum"] = len(pdf_files)
        self.progress_bar["value"] = 0
        self.run_button.config(state="disabled")

        output_file_csv = os.path.join(out_dir, "master_invoice_report.csv")
        output_file_xlsx = os.path.join(out_dir, "master_invoice_report.xlsx")

        try:
            # Step 1: Open stream to write data elements to CSV files
            with open(output_file_csv, "w", newline="", encoding="utf-8") as csv_file:
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
                            # Concatenate extracted content across individual document pages
                            text_list = []
                            for page in pdf.pages:
                                extracted_text = page.extract_text()
                                if extracted_text:
                                    text_list.append(extracted_text)
                            full_text = "".join(text_list)

                            # Identify unscanned images or bad extractions smoothly
                            if len(full_text.strip()) < 10:
                                status = "Scanned Image - No Text"
                            else:
                                # Apply configuration date patterns sequentially to find match
                                for pattern in date_regexes:
                                    match = re.search(pattern, full_text, re.IGNORECASE)
                                    if match:
                                        invoice_date = match.group(1)
                                        break 

                                # Apply financial patterns to extract numerical currency details
                                for pattern in amount_regexes:
                                    match = re.search(pattern, full_text, re.IGNORECASE)
                                    if match:
                                        total_amount = match.groups()[-1]
                                        break

                        # Write verified metadata entries securely down into row indexes
                        writer.writerow({
                            fieldnames[0]: filename,
                            fieldnames[1]: datetime.now().strftime("%Y-%m-%d"),
                            fieldnames[2]: invoice_date,
                            fieldnames[3]: total_amount,
                            fieldnames[4]: status
                        })
                    except Exception as extraction_err:
                        self.log(f"Error in {filename}: {extraction_err}")
                    
                    # Advance progress visualization properties cleanly
                    self.progress_bar["value"] = index
                    self.root.update_idletasks()

            self.log("CSV Report generated successfully.")

            # Step 2: Migrate data tables into calibrated Excel logs
            self.log("Converting to Excel and formatting layouts...")
            df = pd.read_csv(output_file_csv)
            with pd.ExcelWriter(output_file_xlsx, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Invoices')
                worksheet = writer.sheets['Invoices']
                
                # Iteratively scan columns to dynamically adjust boundaries to data lengths
                for idx, col in enumerate(df.columns):
                    series = df[col]
                    max_len = max((
                        series.astype(str).map(len).max(),
                        len(str(series.name))
                    )) + 2
                    
                    # Translate mathematical index keys to alphabetical cells
                    column_letter = chr(65 + idx)
                    worksheet.column_dimensions[column_letter].width = max_len

            self.log("Final Report Ready (Excel Workbook Generated).")
            self.open_button.config(state="normal")
            
            if self.settings.get("auto_open_report"):
                self.open_result_file()

        except Exception as error:
            self.log(f"Critical System Error encountered: {error}")
        finally:
            self.run_button.config(state="normal")

if __name__ == "__main__":
    app_root = tk.Tk()
    ProfessionalExtractorGUI(app_root)
    app_root.mainloop()