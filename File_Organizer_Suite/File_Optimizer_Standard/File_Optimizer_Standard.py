#!/usr/bin/env python

################################################################################
# Date:         2026-03-01
# Script Name:  File_Optimizer_Standard.py
# Author:       omegazyph
# Updated:      2026-09-22
# Description:  Professional CLI file optimizer utilizing core library ANSI colors,
#               unified messaging functions, and dynamically centered ASCII banners.
################################################################################

import json
import logging
import os
import shutil
from datetime import datetime

# --- ANSI Color Codes ---
BLUE = "\033[1;34m"
BOLD = "\033[1m"
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
PURPLE = "\033[1;35m"
RED = "\033[1;31m"
RESET = "\033[0m"
YELLOW = "\033[1;33m"

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


# --- UI Functions ---

def print_ascii_banner(banner_title="Default Title Starting"):
    """Prints a dynamically centered starting ASCII banner."""
    total_width = 80
    title_length = len(banner_title)
    padding = (total_width - title_length) // 2

    # Generate the exact amount of leading spaces for centering
    spaces = " " * padding
    separator_line = "=" * total_width

    print(f"{PURPLE}{separator_line}{RESET}")
    print(f"{BOLD}{BLUE}{spaces}{banner_title}{RESET}")
    print(f"{PURPLE}{separator_line}{RESET}")


def print_ascii_ending(ending_title="Default Title Ending"):
    """Prints a dynamically centered closing ASCII banner."""
    total_width = 80
    title_length = len(ending_title)
    padding = (total_width - title_length) // 2

    # Generate the exact amount of leading spaces for centering
    spaces = " " * padding
    separator_line = "=" * total_width

    print(f"{PURPLE}{separator_line}{RESET}")
    print(f"{BOLD}{BLUE}{spaces}{ending_title}{RESET}")
    print(f"{PURPLE}{separator_line}{RESET}")


def print_message(message_type, message_text=""):
    """Unified message printing function using ANSI color formatting."""
    if message_type == "error":
        print(f"{BOLD}{RED}[X] {message_text}{RESET}")
    elif message_type == "info":
        print(f"{BOLD}{BLUE}[*] {message_text}{RESET}")
    elif message_type == "status":
        print(f"{BOLD}{CYAN}[*] {message_text}{RESET}")
    elif message_type == "success":
        print(f"{BOLD}{GREEN}[+] {message_text}{RESET}")
    elif message_type == "warning":
        print(f"{BOLD}{YELLOW}[!] {message_text}{RESET}")
    else:
        print(message_text)


# --- Application Core ---

class FileOptimizerStandard:
    def __init__(self):
        self.rules = self.load_config()

    def load_config(self):
        """Loads sorting rules from configuration file or initializes defaults."""
        default_rules = {
            "Images": [".jpg", ".jpeg", ".png", ".gif"],
            "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
            "Videos": [".mp4", ".mkv", ".mov"],
            "Archives": [".zip", ".rar", ".7z"]
        }
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, 'r') as file_handle:
                    return json.load(file_handle)
            except FileNotFoundError as load_error:
                print_message("warning", f"Failed to parse config.json, using defaults: {load_error}")
                return default_rules
        else:
            try:
                with open(CONFIG_PATH, 'w') as file_handle:
                    json.dump(default_rules, file_handle, indent=4)
            except FileNotFoundError as save_error:
                print_message("warning", f"Could not save default config.json: {save_error}")
            return default_rules

    def organize(self, target_directory):
        """Scans the target folder and organizes files based on category rules."""
        target_directory = os.path.abspath(target_directory)
        
        if not os.path.exists(target_directory):
            print_message("error", f"The path '{target_directory}' does not exist.")
            return

        start_time = datetime.now()
        print_message("status", f"Scanning: {target_directory}")

        protected_files = [
            os.path.basename(__file__),
            'optimizer_log.txt',
            'config.json',
            'run_optimizer.bat'
        ]
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
                        print_message("success", f"Moved: {filename} -> {category}")
                        logging.info(f"Moved: {filename} to {category}")
                        files_moved += 1
                    except Exception as move_error:
                        print_message("error", f"Failed to move {filename}: {move_error}")
                        logging.error(f"Failed to move {filename}: {move_error}")

        end_time = datetime.now()
        duration = end_time - start_time
        
        print(f"\n{PURPLE}--- Summary ---{RESET}")
        print(f"{BOLD}Files Moved:{RESET} {GREEN}{files_moved}{RESET}")
        print(f"{BOLD}Time elapsed:{RESET} {duration.total_seconds():.2f} seconds")


if __name__ == "__main__":
    # Enable ANSI colors for Windows CMD / PowerShell terminal sessions
    os.system('') 
    
    # Display the startup header banner
    print_ascii_banner("Omegazyph File Optimizer - CLI Mode")
    
    optimizer = FileOptimizerStandard()
    
    user_input = input(f"\n{YELLOW}[!] Enter folder path to clean (or press Enter for current folder): {RESET}").strip()
    target = user_input if user_input else BASE_DIR
    
    optimizer.organize(target)
    
    # Display the completion closing banner
    print_ascii_ending("File Optimization Complete")
    
    input(f"\n{CYAN}[*] Press Enter to close...{RESET}")