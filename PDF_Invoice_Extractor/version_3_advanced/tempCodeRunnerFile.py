################################################################################
# Date: 2026-05-02
# Script Name: advanced_extractor_gui.py
# Author: omegazyph
# Updated: 2026-05-05
# Description: Professional Enterprise UI for PDF Invoice Extraction.
#              Includes Logo support, Sidebar Execution, and Open-File logic.
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
        """
        Initialize the main application window and load initial configurations.
        """
        self.root = root
        self.root.title("omegazyph | Enterprise PDF Extractor")
        self.root.geometry("700x750") 
        self.root.configure(bg="#f0f2f5") 

        # Define the path for the configuration file
        self.config_path = "advanced_config.json"
        # Load existing settings or create default values
        self.settings = self.load_settings()

        # Configure the visual styles for the application widgets
        self.style = ttk.Style()
        self.style.theme_use('clam') 
        
        # Standard button font configuration
        self.style.configure(
            "TButton", 
            font=("Segoe UI", 10)
            )
        
        # Header label style with corporate branding colors
        self.style.configure(
            "Header.TLabel", 
            font=("Segoe UI", 18, "bold"), 
            background="#f0f2f5", 
            foreground="#1a73e8"
            )
        
        # Progress bar thickness for better visibility
        self.style.configure(
            "TProgressbar", 
            thickness=20
            )

        # Initialize the User Interface elements
        self.create_ui()

    def load_settings(self):
        """
        Load settings from a JSON file or return default settings if the file is missing.
        """
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as file:
                    return json.load(file)
            except Exception:
                # If the file is corrupted, fall back to defaults
                pass
        return {
            "last_input_folder": "", 
            "last_output_folder": "", 
            "author": "omegazyph"
            }

    def save_settings(self):
        """
        Save the current folder selections and settings to the configuration JSON file.
        """
        with open(self.config_path, "w") as file:
            json.dump(self.settings, file, indent=4)

    def create_ui(self):
        """
        Construct the graphical interface, including frames, labels, buttons, and logs.
        """
        # Create the primary container for the entire application
        main_frame = tk.Frame(
            self.root, 
            bg="#f0f2f5", 
            padx=20, 
            pady=10
            )
        main_frame.pack(
            expand=True,
            fill="both"
            )

        # --- BRANDING SECTION (Logo and Title) ---
        branding_frame = tk.Frame(
            main_frame, 
            bg="#f0f2f5"
            )
        branding_frame.pack(
            fill="x",
            pady=(5, 15)
            )

        # Determine the directory of the current script to locate assets
        script_directory = os.path.dirname(
            os.path.abspath(__file__)
            )

        logo_path = os.path.join(
            script_directory, 
            "logo.png"
            )

        # Attempt to load the corporate logo if it exists
        try:
            self.logo_image = tk.PhotoImage(
                file=logo_path
            ).subsample(9, 9)

            logo_label = tk.Label(
                branding_frame, 
                image=self.logo_image, 
                bg="#f0f2f5"
                )
            logo_label.pack(
                side="top", 
                pady=(0, 5)
                )
        except Exception:
            # Silently fail if the logo file is not present
            pass

        # Main application title displayed under the logo
        header = ttk.Label(
            branding_frame, 
            text="PDF Data Automation Suite", 
            style="Header.TLabel"
            )
        header.pack(
            side="top", 
            pady=5
            )

        # --- FOLDER CONFIGURATION SECTION ---
        selection_frame = tk.LabelFrame(
            main_frame, 
            text=" Configuration Settings ", 
            bg="white", 
            font=("Segoe UI", 10, "bold"), 
            padx=15, 
            pady=15
            )
        selection_frame.pack(
            fill="x", 
            pady=5
            )

        # Source Folder UI Elements
        ttk.Label(
            selection_frame, 
            text="Source Folder (PDFs):", 
            background="white"
            ).pack(anchor="w")

        input_row = tk.Frame(
            selection_frame, 
            bg="white"
            )
        input_row.pack(
            fill="x", 
            pady=(0, 10)
            )

        self.input_entry = ttk.Entry(
            input_row
            )
        self.input_entry.insert(0, self.settings.get("last_input_folder",""))
        self.input_entry.pack(
            side="left", 
            expand=True, 
            fill="x", 
            padx=(0, 5)
            )

        ttk.Button(
            input_row, 
            text="Browse", 
            command=self.browse_input
            ).pack(side="right")

        # Destination Folder UI Elements
        ttk.Label(
            selection_frame, 
            text="Destination Folder (CSV):", 
            background="white"
            ).pack(anchor="w")

        output_row = tk.Frame(
            selection_frame, 
            bg="white"
            )
        output_row.pack(
            fill="x"
            )

        self.output_entry = ttk.Entry(
            output_row
            )
        self.output_entry.insert(0, self.settings.get("last_output_folder", ""))
        self.output_entry.pack(
            side="left", 
            expand=True, 
            fill="x", 
            padx=(0, 5)
            )

        ttk.Button(
            output_row, 
            text="Browse", 
            command=self.browse_output
            ).pack(side="right")

        # --- PROGRESS TRACKING SECTION ---
        progress_frame = tk.Frame(
            main_frame, 
            bg="#f0f2f5"
            )
        progress_frame.pack(
            fill="x", 
            pady=15
            )

        self.progress_label = ttk.Label(
            progress_frame, 
            text="System Ready", 
            background="#f0f2f5", 
            font=("Segoe UI", 9)
            )
        self.progress_label.pack(
            anchor="w"
            )

        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            orient="horizontal", 
            length=100, 
            mode="determinate"
            )
        self.progress_bar.pack(
            fill="x", 
            pady=5
            )

        # --- WORK AREA (Split View with Sidebar and Logs) ---
        work_area = tk.Frame(
            main_frame, 
            bg="#f0f2f5"
            )
        work_area.pack(
            expand=True,
            fill="both", 
            pady=10
            )

        # Sidebar containing action buttons
        button_sidebar = tk.Frame(
            work_area,
            bg="#f0f2f5"
            )
        button_sidebar.pack(
            side="left",
            fill="y",
            padx=(0, 15)
            )

        side_button_width = 20

        # Execute processing button
        self.run_button = tk.Button(
            button_sidebar, 
            text="EXECUTE", 
            bg="#1a73e8", 
            fg="white", 
            font=("Segoe UI", 11, "bold"), 
            relief="flat", 
            height=2, 
            width=side_button_width,
            cursor="hand2",
            command=self.run_process
            )
        self.run_button.pack(
            side="top",  
            pady=5
            )

        # Open source directory button
        self.source_button = tk.Button(
            button_sidebar,
            text="SOURCE FOLDER",
            bg="#5f6368", 
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            height=2,
            width=side_button_width,
            cursor="hand2",
            command=self.open_source_folder
            )
        self.source_button.pack(
            side="top",
            pady=5
            )

        # Open result file button (initially disabled until processing finishes)
        self.open_button = tk.Button(
            button_sidebar, 
            text="OPEN REPORT",
            bg="#1a73e8", 
            fg="white", 
            font=("Segoe UI", 11, "bold"), 
            relief="flat", 
            height=2, 
            width=side_button_width,
            cursor="hand2",
            state="disabled", 
            command=self.open_result_file
            )
        self.open_button.pack(
            side="top", 
            pady=5
            )

        # --- ACTIVITY LOG SECTION ---
        log_container = tk.Frame(
            work_area,
            bg="#f0f2f5"
            )
        log_container.pack(
            side="left",
            expand=True,
            fill="both"
            )
        
        tk.Label(
            log_container, 
            text="Process Activity Log", 
            bg="#f0f2f5", 
            font=("Segoe UI", 9, "italic")
            ).pack(anchor="w")
        
        self.log_area = scrolledtext.ScrolledText(
            log_container,
            width=50, 
            height=12, 
            font=("Consolas", 10), 
            bg="#ffffff", 
            fg="#333333", 
            borderwidth=1, 
            relief="solid"
            )
        self.log_area.pack(
            expand=True,
            fill="both"
            )

        # Footer indicating the author's handle
        tk.Label(
            main_frame, 
            text=f"Author Handle: {self.settings.get('author', 'omegazyph')}", 
            bg="#f0f2f5", 
            fg="#666666", 
            font=("Segoe UI", 8)
            ).pack(pady=(5, 0))

    def browse_input(self):
        """Trigger a directory selection dialog for the input source."""
        folder = filedialog.askdirectory()
        if folder:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, folder)

    def browse_output(self):
        """Trigger a directory selection dialog for the output destination."""
        folder = filedialog.askdirectory()
        if folder:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder)

    def log(self, message):
        """Append a timestamped message to the scrolled text log area."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_area.see(tk.END)
        self.root.update_idletasks()

    def open_result_file(self):
        """Open the generated report CSV using the system's default application."""
        output_directory = self.output_entry.get()
        output_file = os.path.join(
            output_directory, 
            "master_invoice_report.csv"
            )

        if os.path.exists(output_file):
            try:
                os.startfile(output_file)
                self.log(f"System: Opening {output_file}")
            except Exception as error:
                messagebox.showerror(
                    "Error", 
                    f"Could not open file: {error}"
                    )
        else:
            messagebox.showwarning(
                "File Not Found", 
                "The report file does not exist yet."
                )

    def open_source_folder(self):
        """Open the folder containing the source PDFs for quick review."""
        input_directory = self.input_entry.get()

        if os.path.exists(input_directory) and input_directory:
            try:
                os.startfile(input_directory)
                self.log(f"System: Opening source folder {input_directory}")
            except Exception as error:
                messagebox.showerror(
                    "Error",
                    f"Could not open folder: {error}"
                    )
        else:
            messagebox.showwarning(
                "Folder Not found",
                "The source folder path is empty or invalid."
                )

    def run_process(self):
        """Execute the PDF scanning and CSV writing logic."""
        input_directory = self.input_entry.get()
        output_directory = self.output_entry.get()

        # Validate that the selected paths are legitimate
        if not os.path.exists(input_directory) or not input_directory:
            messagebox.showwarning(
                "Input Required",
                "Please select a valid source folder containing PDFs."
                )
            return

        if not os.path.exists(output_directory) or not output_directory:
            messagebox.showwarning(
                "Output Required",
                "Please select a valid destination folder for the CSV."
                )
            return

        # Save the current paths for the next session
        self.settings["last_input_folder"] = input_directory
        self.settings["last_output_folder"] = output_directory
        self.save_settings()

        # Gather a list of all PDF files in the directory
        pdf_files = [f for f in os.listdir(input_directory) if f.lower().endswith(".pdf")]
        total_files = len(pdf_files)
        
        if total_files == 0:
            self.log("Notice: No PDF files found in the selected folder.")
            messagebox.showinfo(
                "No Files",
                "The selected folder does not contain any .pdf files."
                )
            return

        # Prepare the progress tracking bar
        self.progress_bar["maximum"] = total_files
        self.progress_bar["value"] = 0
        self.run_button.config(state="disabled")

        total_value = 0.0
        output_file = os.path.join(
            output_directory,
            "master_invoice_report.csv"
            )

        try:
            # Open the CSV file in append mode
            with open(output_file, "a", newline="") as csv_file:
                fieldnames = ["FileName", "ProcessedDate", "InvoiceDate", "Amount"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                # Write the header if the file is new or empty
                if not os.path.exists(output_file) or os.path.getsize(output_file) == 0:
                    writer.writeheader()

                for index, filename in enumerate(pdf_files, start=1):
                    self.log(f"Processing ({index}/{total_files}): {filename}")
                    self.progress_label.config(
                        text=f"Extracting file {index} of {total_files}..."
                    )

                    full_path = os.path.join(input_directory, filename)

                    try:
                        # Perform the data extraction using pdfplumber
                        with pdfplumber.open(full_path) as pdf:
                            first_page = pdf.pages[0] 
                            extracted_text = first_page.extract_text()

                            # Check if the PDF is text-based or just a flat image
                            if not extracted_text or not extracted_text.strip():
                                self.log(f"Warning: {filename} appears to be an image/scan. Skipping.")
                                continue 

                            # Use Regular Expressions to find dates and dollar amounts
                            date_match = re.search(
                                r"(\d{1,4}[-/]\d{1,2}[-/]\d{2,4})", 
                                extracted_text
                                )

                            money_match = re.search(
                                r"\$(\d{1,3}(?:,\d{3})*(?:\.\d{2}))", 
                                extracted_text
                                )

                            extracted_amount = "0.00"
                            if money_match:
                                extracted_amount = money_match.group(1)
                                # Remove commas for mathematical summation
                                clean_amount = extracted_amount.replace(',', '')
                                total_value += float(clean_amount)

                            # Record the extracted data to the CSV row
                            writer.writerow({
                                "FileName": filename,
                                "ProcessedDate": datetime.now().strftime("%Y-%m-%d"),
                                "InvoiceDate": date_match.group(1) if date_match else "N/A",
                                "Amount": extracted_amount
                                })

                    except Exception as file_error:
                        self.log(
                            f"Error in {filename}: {str(file_error)}"
                            )
                        continue

                    # Update the progress UI components
                    self.progress_bar["value"] = index
                    self.root.update_idletasks()

            self.log(
                f"Success: Extraction process complete. Total value: ${total_value:,.2f}"
                )

            self.progress_label.config(
                text="Status: Process finished successfully."
                )

            # Display a final summary to the user
            summary_message = (
                f"Successfully processed {total_files} invoices.\n\n"
                f"Total Extracted Value: ${total_value:,.2f}"
                )
            messagebox.showinfo(
                "Task Complete", 
                summary_message
                )

        except Exception as error:
            self.log(
                f"System Error: {str(error)}"
                )
            messagebox.showerror(
                "Error", 
                f"A processing error occurred:\n{error}"
            )

        finally:
            # Re-enable the UI buttons
            self.run_button.config(state="normal")
            self.open_button.config(state="normal") 

# Execution entry point
if __name__ == "__main__":
    app_root = tk.Tk()
    application = ProfessionalExtractorGUI(app_root)
    app_root.mainloop()