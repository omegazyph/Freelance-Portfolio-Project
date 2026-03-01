# Date: 2026-03-01
# Script Name: File_Optimizer_Standard.py
# Author: omegazyph
# Updated: 2026-03-01
# Description: Professional CLI file optimizer with Color Output and Path Selection.

import os
import shutil
import json
import logging
from datetime import datetime

# Base directory for the script's internal files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')
LOG_PATH = os.path.join(BASE_DIR, 'optimizer_log.txt')

# Setup logging
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Simple class for ANSI Colors
class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

class FileOptimizerStandard:
    def __init__(self):
        self.rules = self.load_config()

    def load_config(self):
        default_rules = {
            "Images": [".jpg", ".jpeg", ".png", ".gif"],
            "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
            "Videos": [".mp4", ".mkv", ".mov"],
            "Archives": [".zip", ".rar", ".7z"]
        }
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, 'r') as f:
                    return json.load(f)
            except Exception:
                return default_rules
        else:
            with open(CONFIG_PATH, 'w') as f:
                json.dump(default_rules, f, indent=4)
            return default_rules

    def organize(self, target_directory):
        target_directory = os.path.abspath(target_directory)
        
        if not os.path.exists(target_directory):
            print(f"{Color.RED}Error: The path '{target_directory}' does not exist.{Color.END}")
            return

        start_time = datetime.now()
        print(f"\n{Color.CYAN}Scanning: {Color.BOLD}{target_directory}{Color.END}")

        protected_files = [os.path.basename(__file__), 'optimizer_log.txt', 'config.json', 'run_optimizer.bat']
        files_moved = 0

        for filename in os.listdir(target_directory):
            file_path = os.path.join(target_directory, filename)
            
            if os.path.isdir(file_path) or filename in protected_files:
                continue

            extension = os.path.splitext(filename)[1].lower()
            
            for category, extensions in self.rules.items():
                if extension in extensions:
                    dest_dir = os.path.join(target_directory, category)
                    os.makedirs(dest_dir, exist_ok=True)
                    
                    try:
                        shutil.move(file_path, os.path.join(dest_dir, filename))
                        print(f"{Color.GREEN}Moved:{Color.END} {filename} {Color.YELLOW}->{Color.END} {category}")
                        logging.info(f"Moved: {filename} to {category}")
                        files_moved += 1
                    except Exception as e:
                        print(f"{Color.RED}Failed to move {filename}: {e}{Color.END}")
                        logging.error(f"Failed to move {filename}: {e}")

        end_time = datetime.now()
        duration = end_time - start_time
        print(f"\n{Color.PURPLE}--- Summary ---{Color.END}")
        print(f"{Color.BOLD}Files Moved:{Color.END} {Color.GREEN}{files_moved}{Color.END}")
        print(f"{Color.BOLD}Time elapsed:{Color.END} {duration.total_seconds():.2f} seconds")

if __name__ == "__main__":
    # Enable ANSI colors for Windows 10/11 CMD
    os.system('') 
    
    optimizer = FileOptimizerStandard()
    
    print(f"{Color.CYAN}{Color.BOLD}==================================================")
    print("      Omegazyph File Optimizer - CLI Mode")
    print(f"=================================================={Color.END}")
    
    user_input = input(f"\n{Color.YELLOW}Enter folder path to clean (or press Enter for current folder): {Color.END}").strip()
    target = user_input if user_input else BASE_DIR
    
    optimizer.organize(target)
    
    print(f"\n{Color.CYAN}Press Enter to close...{Color.END}")
    input()