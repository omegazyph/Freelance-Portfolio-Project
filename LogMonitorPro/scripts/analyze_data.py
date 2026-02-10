"""
Date: 2026-02-10
Script Name: analyze_data.py
Author: omegazyph
Updated: 2026-02-10
Description: This program uses absolute path resolution to ensure it can locate 
             the logs and reports folders even when executed from a subfolder.
"""

import os
import sys
from datetime import datetime

def run_log_analysis():
    # Identify the directory where this script is currently located
    # This represents the "Log_Monitor_System/scripts" folder
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Navigate up one level to reach the main project root directory
    # This represents the "Log_Monitor_System" folder
    project_root = os.path.dirname(script_directory)

    # Define the full paths to the logs and reports folders
    log_folder_path = os.path.join(project_root, "logs")
    report_folder_path = os.path.join(project_root, "reports")
    
    input_file_path = os.path.join(log_folder_path, "system_activity.log")
    
    # Create a unique filename for the output report
    time_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file_path = os.path.join(report_folder_path, f"analysis_report_{time_stamp}.txt")

    # Ensure the reports directory exists at the root level
    if not os.path.exists(report_folder_path):
        os.makedirs(report_folder_path)

    print(f"Attempting to open the log file at: {input_file_path}")

    try:
        # Open the log file using the resolved absolute path
        with open(input_file_path, "r") as source_file:
            log_lines = source_file.readlines()

        if not log_lines:
            print("The log file was located but it contains no data.")
            return

        # Identify every line that contains the word ERROR
        error_logs = [line.strip() for line in log_lines if "ERROR" in line]

        # Write the summary findings to the report file
        with open(output_file_path, "w") as report_file:
            report_file.write("LOG MONITORING SYSTEM REPORT\n")
            report_file.write("Author: omegazyph\n")
            report_file.write(f"Date of Analysis: {datetime.now()}\n")
            report_file.write("-" * 30 + "\n")
            report_file.write(f"Total Lines Processed: {len(log_lines)}\n")
            report_file.write(f"Total Errors Identified: {len(error_logs)}\n\n")
            
            for count, error in enumerate(error_logs, start=1):
                report_file.write(f"{count}. {error}\n")

        print(f"The analysis is complete. The report is saved at: {output_file_path}")

    except FileNotFoundError:
        print(f"Error: Could not find the file at {input_file_path}")
        print("Please ensure that the logs folder and the log file exist at the log folder.")
    except Exception as unexpected_error:
        print(f"An unexpected error has occurred: {unexpected_error}")
        sys.exit(1)

if __name__ == "__main__":
    run_log_analysis()