# -----------------------------------------------------------------------------
# Date: 2026-01-05
# Script Name: analyze_data.py
# Author: omegazyph
# Updated: 2026-02-14
# Description: Advanced Version. Features modular function design, 
#              CSV export capabilities, and multi-keyword extraction.
# -----------------------------------------------------------------------------

import os
import sys
import json
import csv
from datetime import datetime

def load_settings(config_path):
    """Loads configuration from JSON file."""
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[FATAL] Could not read config: {e}")
        sys.exit(1)

def parse_logs(log_path, keywords):
    """Filters logs based on keywords and returns a list of dictionaries."""
    extracted_data = []
    try:
        with open(log_path, "r") as f:
            for line_num, line in enumerate(f, 1):
                if any(key in line for key in keywords):
                    # We split the log into a dictionary for CSV structure
                    extracted_data.append({
                        "Line": line_num,
                        "Timestamp": datetime.now().isoformat(),
                        "Content": line.strip()
                    })
        return extracted_data
    except FileNotFoundError:
        print(f"[ERROR] Log file not found: {log_path}")
        return []

def save_as_csv(data, output_path):
    """Saves the extracted data into a professional CSV format."""
    if not data:
        return
    keys = data[0].keys()
    with open(output_path, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

def main():
    # Setup Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    config = load_settings(os.path.join(project_root, "config.json"))
    
    log_file = os.path.join(project_root, "logs", config["log_filename"])
    report_dir = os.path.join(project_root, "reports")
    
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    # Execute Logic
    print(f"[*] Advanced Scan Started: {datetime.now()}")
    results = parse_logs(log_file, config["search_keywords"])
    
    if results:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
        output_file = os.path.join(report_dir, f"{config['report_prefix']}_{timestamp}.csv")
        save_as_csv(results, output_file)
        print(f"[SUCCESS] {len(results)} events exported to {output_file}")
    else:
        print("[!] No matching log entries found.")

if __name__ == "__main__":
    main()