# -----------------------------------------------------------------------------
# Date: 2026-01-05
# Script Name: analyze_data.py
# Author: omegazyph
# Updated: 2026-02-14
# Description: Standard Version. Uses a JSON configuration file to dynamically
#              filter logs based on user-defined keywords.
# -----------------------------------------------------------------------------

import os
import sys
import json
from datetime import datetime

def run_log_analysis():
    # Path setup
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Locate the Config file
    config_path = os.path.join(project_root, "config.json")
    
    # Load configuration
    if not os.path.exists(config_path):
        print(f"Error: Configuration file missing at {config_path}")
        sys.exit(1)
        
    with open(config_path, "r") as f:
        config = json.load(f)

    # Set paths based on Config
    log_file = os.path.join(project_root, "logs", config["log_filename"])
    report_dir = os.path.join(project_root, "reports")
    
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    time_stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    output_file = os.path.join(report_dir, f"{config['report_prefix']}_{time_stamp}.txt")

    try:
        with open(log_file, "r") as source:
            lines = source.readlines()

        # Search for multiple keywords from the config
        found_logs = []
        for line in lines:
            if any(word in line for word in config["search_keywords"]):
                found_logs.append(line.strip())

        with open(output_file, "w") as report:
            report.write(f"STANDARD LOG REPORT - {datetime.now()}\n")
            report.write(f"Keywords Searched: {', '.join(config['search_keywords'])}\n")
            report.write("-" * 40 + "\n")
            for entry in found_logs:
                report.write(f"{entry}\n")

        print(f"Standard Analysis Complete. Found {len(found_logs)} events.")

    except FileNotFoundError:
        print(f"Error: Could not find log file at {log_file}")
        sys.exit(1)

if __name__ == "__main__":
    run_log_analysis()