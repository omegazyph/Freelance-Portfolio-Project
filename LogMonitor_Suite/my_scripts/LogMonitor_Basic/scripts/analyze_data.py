# -----------------------------------------------------------------------------
# Date: 2026-01-05
# Script Name: analyze_data.py
# Author: omegazyph
# Updated: 2026-02-14
# Description: This program uses path resolution to navigate from the scripts 
#              folder to a separate logs folder to process data.
# -----------------------------------------------------------------------------

import os
import sys
from datetime import datetime

def run_log_analysis():

    # this will be the 'scripts' folder.
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Navigate 'up' one level to the main Project folder.
    project_root = os.path.dirname(script_directory)

    # Define the paths for the logs and reports folders.
    log_folder_path = os.path.join(project_root, "logs")
    report_folder_path = os.path.join(project_root, "reports")
    
    # Specify the file name inside that folder.
    input_file_path = os.path.join(log_folder_path, "system_activity.log")
    
    # Create a unique filename for the output report with a timestamp.
    time_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file_path = os.path.join(report_folder_path, f"analysis_report_{time_stamp}.txt")

    # Ensure the reports directory exists; if not, create it.
    if not os.path.exists(report_folder_path):
        os.makedirs(report_folder_path)

    print(f"Attempting to open the log file at: {input_file_path}")

    try:
        # Open the log file using the resolved path.
        with open(input_file_path, "r") as source_file:
            log_lines = source_file.readlines()

        if not log_lines:
            print("The log file was located but it contains no data.")
            return

        # Logic: Identify every line that contains the word ERROR.
        error_logs = [line.strip() for line in log_lines if "ERROR" in line]

        # Write the results to the report file.
        with open(output_file_path, "w") as report_file:
            report_file.write("LOG MONITORING SYSTEM REPORT\n")
            report_file.write("Author: omegazyph\n")
            report_file.write(f"Date of Analysis: {datetime.now()}\n")
            report_file.write("-" * 30 + "\n")
            report_file.write(f"Total Lines Processed: {len(log_lines)}\n")
            report_file.write(f"Total Errors Identified: {len(error_logs)}\n\n")
            
            for count, error in enumerate(error_logs, start=1):
                report_file.write(f"{count}. {error}\n")

        print(f"Analysis complete. Report saved at: {output_file_path}")

    except FileNotFoundError:
        print(f"Error: Could not find the file at {input_file_path}")
        print("Check if the 'logs' folder exists and contains 'system_activity.log'.")
        sys.exit(1)
    except Exception as unexpected_error:
        print(f"An unexpected error has occurred: {unexpected_error}")
        sys.exit(1)

if __name__ == "__main__":
    run_log_analysis()