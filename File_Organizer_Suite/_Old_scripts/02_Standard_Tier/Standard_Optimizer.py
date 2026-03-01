"""
Date:           2026-01-05
Script Name:    Standard_Optimizer.py
Author:         omegazyph
Updated:        2026-02-16
Description:    Standard Tier: Python-based organizer with subfolder 
                configuration management and color-coded reporting.
"""

import os
import shutil
import json

# Visual Theming
BLUE = '\033[94m'
GREEN = '\033[92m'
CYAN = '\033[96m'
ENDC = '\033[0m'
BOLD = '\033[1m'

def load_config():
    """Loads config.json from the /config/ directory or creates it."""
    # Define the directory and file path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(script_dir, 'config')
    config_file = os.path.join(config_dir, 'config.json')
    
    # Ensure the config directory exists
    os.makedirs(config_dir, exist_ok=True)
    
    default_groups = {
        "Images":    [".jpg", ".jpeg", ".png", ".gif", ".svg"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".csv", ".xlsx", ".ods"],
        "Archives":  [".zip", ".tar", ".gz", ".rar", ".7z"],
        "Videos":    [".mp4", ".mov", ".avi", ".mkv", ".wmv"]
    }
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except:
            return default_groups
    else:
        try:
            with open(config_file, 'w') as f:
                json.dump(default_groups, f, indent=4)
            print(f"{CYAN}⚙️  System: Created config/config.json{ENDC}")
        except Exception as e:
            print(f"Error creating config: {e}")
            
    return default_groups

def run_standard():
    # Targeted path for the Lenovo Legion Downloads
    target = os.path.expanduser("~/Downloads")
    groups = load_config()
    
    print(f"{BLUE}=================================================={ENDC}")
    print(f"{GREEN}{BOLD}      OMEGAZYPH STANDARD OPTIMIZER (PY)           {ENDC}")
    print(f"{BLUE}=================================================={ENDC}")
    print(f"{CYAN}📂 Targeting: {target}{ENDC}\n")

    if not os.path.exists(target):
        print(f"Error: {target} not found.")
        return

    # Store original directory to avoid path issues
    original_dir = os.getcwd()
    os.chdir(target)
    count = 0

    # Main Loop
    for filename in os.listdir('.'):
        if os.path.isfile(filename) and filename != os.path.basename(__file__):
            ext = os.path.splitext(filename)[1].lower()
            for folder, extensions in groups.items():
                if ext in extensions:
                    os.makedirs(folder, exist_ok=True)
                    try:
                        shutil.move(filename, os.path.join(folder, filename))
                        print(f"  {GREEN}✔{ENDC} {filename[:30].ljust(30)} {CYAN}→ {folder}{ENDC}")
                        count += 1
                        break
                    except Exception as e:
                        print(f"Error moving {filename}: {e}")

    os.chdir(original_dir)
    print(f"\n{GREEN}{BOLD}✅ Optimization Complete: {count} files moved.{ENDC}")

if __name__ == "__main__":
    run_standard()