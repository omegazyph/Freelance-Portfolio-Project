################################################################################
# Date: 2026-05-02
# Script Name: advanced_extractor_gui.py
# Author: omegazyph
# Updated: 2026-05-02
# Description: Professional UI for PDF Invoice Extraction with Progress Bar.
#              Features a modern layout, themed colors, and visual feedback.
################################################################################

import os
import json
import csv
import re
import pdfplumber
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk 
from datetime import datetime

class ProfessionalExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("omegazyph | Enterprise PDF Extractor")
        self.root.geometry("700x650")
        self.root.configure(bg="#f0f2f5") 

        # Configuration Loading
        self.config_path = "advanced_config.json"
        self.settings = self.load_settings()

        # Styles
        self.style = ttk.Style()
        self.style.theme_use('clam') # Use a cleaner theme for the progress bar
        self.style.configure("TButton", font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), background="#f0f2f5", foreground="#1a73e8")
        self.style.configure("TProgressbar", thickness=20)

        self.create_ui()

    def load_settings(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as file:
                return json.load(file)
        return {"last_input_folder": "", "last_output_folder": "", "author": "omegazyph"}

    def save_settings(self):
        with open(self.config_path, "w") as file:
            json.dump(self.settings, file, indent=4)

    def create_ui(self):
        # Main Container
        main_frame = tk.Frame(self.root, bg="#f0f2f5", padx=20, pady=10)
        main_frame.pack(expand=True, fill="both")

        # Header Section
        header = ttk.Label(main_frame, text="PDF Data Automation Suite", style="Header.TLabel")
        header.pack(pady=(0, 15))

        # Folder Selection Section
        selection_frame = tk.LabelFrame(main_frame, text=" Configuration Settings ", bg="white", font=("Segoe UI", 10, "bold"), padx=15, pady=15)
        selection_frame.pack(fill="x", pady=5)

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

        # Progress Section
        progress_frame = tk.Frame(main_frame, bg="#f0f2f5")
        progress_frame.pack(fill="x", pady=15)
        
        self.progress_label = ttk.Label(progress_frame, text="Ready to process", background="#f0f2f5")
        self.progress_label.pack(anchor="w")
        
        self.progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=100, mode="determinate")
        self.progress_bar.pack(fill="x", pady=5)

        # Execution Section
        self.run_btn = tk.Button(main_frame, text="EXECUTE AUTOMATION", bg="#1a73e8", fg="white", 
                                font=("Segoe UI", 12, "bold"), relief="flat", height=2, cursor="hand2",
                                command=self.run_process)
        self.run_btn.pack(fill="x", pady=5)

        # Log Section
        tk.Label(main_frame, text="Process Activity Log", bg="#f0f2f5", font=("Segoe UI", 9, "italic")).pack(anchor="w")
        self.log_area = scrolledtext.ScrolledText(main_frame, width=70, height=10, font=("Consolas", 10), 
                                                 bg="#ffffff", fg="#333333", borderwidth=1, relief="solid")
        self.log_area.pack(expand=True, fill="both")

        # Footer
        tk.Label(main_frame, text=f"Author: {self.settings.get('author', 'omegazyph')}", 
                 bg="#f0f2f5", fg="#666666", font=("Segoe UI", 8)).pack(pady=(5, 0))

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

        self.settings["last_input_folder"] = input_dir
        self.settings["last_output_folder"] = output_dir
        self.save_settings()

        pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]
        total_files = len(pdf_files)
        
        if total_files == 0:
            self.log("Notice: No PDF files found.")
            return

        # Reset Progress Bar
        self.progress_bar["maximum"] = total_files
        self.progress_bar["value"] = 0
        self.run_btn.config(state="disabled") # Prevent double clicking

        output_file = os.path.join(output_dir, "master_invoice_report.csv")
        
        try:
            with open(output_file, "a", newline="") as csv_file:
                fieldnames = ["FileName", "ProcessedDate", "InvoiceDate", "Amount"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                
                if not os.path.exists(output_file) or os.path.getsize(output_file) == 0:
                    writer.writeheader()

                for index, filename in enumerate(pdf_files, start=1):
                    self.log(f"Processing ({index}/{total_files}): {filename}")
                    self.progress_label.config(text=f"Processing file {index} of {total_files}...")
                    
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
                    
                    # Update Progress Bar
                    self.progress_bar["value"] = index
                    self.root.update_idletasks()
            
            self.log("Success: Report complete.")
            self.progress_label.config(text="Status: All files processed successfully.")
            messagebox.showinfo("Task Complete", f"Processed {total_files} files successfully.")

        except Exception as e:
            self.log(f"Process Error: {str(e)}")
            messagebox.showerror("System Error", f"An error occurred: {e}")
        
        finally:
            self.run_btn.config(state="normal")

if __name__ == "__main__":
    app_root = tk.Tk()
    ProfessionalExtractorGUI(app_root)
    app_root.mainloop()