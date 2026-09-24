#!/usr/bin/env python

################################################################################
# Date:         2026-03-01
# Script Name:  File_Optimizer_Standard.py
# Author:       omegazyph
# Updated:      2026-09-24
# Description:  Professional CLI file optimizer utilizing core library ANSI colors,
#               unified messaging functions, module-level logging, dynamically
#               centered ASCII banners, and modular JSON configuration settings.
#               Strict Dependency: Requires config.json to execute.
################################################################################

import json
import logging
import os
import shutil
import sys
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

# Instantiate module-level logger instance
logger = logging.getLogger(__name__)


# --- UI Functions ---

def print_ascii_banner(banner_title="Default Title Starting"):
    """
    Prints a dynamically centered starting ASCII banner.
    """
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
    """
    Prints a dynamically centered closing ASCII banner.
    """
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
    """
    Unified message printing function using ANSI color formatting.
    """
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
        """
        Initializes the file optimizer and strictly loads configuration rules.
        """
        self.rules = self.load_config()

        # Pase settings and categories
        self.settings = self.config.get("settings",{})
        self.categories = self.config.get("categories",{})

        # Load specific feature flags with safety defaults
        self.show_summary = self.settings.get()
        self.organize_unmatched = self.settings.get()
        self.unmatched_folder_name = self.settings.get()
        self.user_protected_files = self.settings.get()
        self.protected_extensions = self.settings.get()

    def load_config(self):
        """
        Loads sorting rules strictly from config.json.
        Terinates execution if the configuration file is missing or invalid.
        """
        # step 1: Verify file existence first
        if not os.path.exists(CONFIG_PATH):
            error_message = f"Missing required configuration file: '{CONFIG_PATH}'. Program cannot run without config.json."
            print_message("error", error_message)
            logger.critical(error_message)
            raise FileNotFoundError(error_message)

        try:
            with open(CONFIG_PATH, 'r') as file_handle:
                return json.load(file_handle)
                
        except (OSError, json.JSONDecodeError) as parse_error:
            error_message = f"Failed to parse config.json: {parse_error}"
            print_message("error", error_message)
            logger.critical(error_message)
            raise FileNotFoundError(error_message)

    def organize(self, target_directory):
        """
        Scans the target folder and organizes files based on category rules.
        """
        target_directory = os.path.abspath(target_directory)
        
        if not os.path.exists(target_directory):
            error_message = f"the path '{target_directory}' does not exist."
            print_message("error", error_message)
            logger.error(error_message)
            return

        start_time = datetime.datetime.now()
        print_message("status", f"Scanning target directory: {target_directory}")
        logger.info(f"Started optimization scan on: {target_directory}")

        # system protected files
        internal_protected_files = [
            os.path.basename(__file__),
            'optimizer_log.txt',
            'config.json',
            'run_optimizer.bat'
        ]

        # Combine system protected files with user defined protected files
        all_protected_files = set(internal_protected_files + self.user_protected_files)
        files_moved = 0

        for filename in os.listdir(target_directory):
            file_path = os.path.join(target_directory, filename)

            # skip directories and protected files
            if os.path.isdir(file_path) or filename in all_protected_files:
                continue

            extension = os.path.splitext(filename)[1].lower()

            # Skip files with protected extensions (.tmp, .crdownload, etc.)
            if extension in self.protected_extensions:
                print_message("warning", f"Skipped proected file type: {filename}")
                logger.info(f"Skipped file {filename} dur to protected extension rules")
                continue

            match_category = None

            # Match extension aginst rules
            for category, extensions in self.categories.items():
                if extension in extensions:
                    match_category = category
                    break

            # If unmatched, check if organize_unmatched is enabled
            if not match_category and self.organize_unmatched:
                    match_category = self.unmatched_folder_name

            # Execute file move if category determined
            if match_category:
                    dest_dir = os.path.join(target_directory, match_category)
                    os.makedirs(dest_dir, exist_ok=True)
                    
                    try:
                        shutil.move(file_path, os.path.join(dest_dir, filename))
                        print_message("success", f"Moved: {filename} -> {match_category}")
                        logger.info(f"Moved: {filename} to {match_category}")
                        files_moved += 1

                    except shutil.Error as duplicate_error:
                        error_message = f"Destination file already exists in '{match_category}': {duplicate_error}"
                        print_message("warning", f"Skipped {filename}: {error_message}")
                        logger.warning(f"Skipped {filename}: {error_message}")

                    except PermissionError:
                        error_message = f"Permission denied for '{filename}' (File may be in use or open in another program)."
                        print_message("error", f"Failed to move {filename}: {error_message}")
                        logger.error(f"Failed to move {filename}: {error_message}")

                    except FileNotFoundError:
                        error_message = f"Source path missing for '{filename}'."
                        print_message("error", f"Failed to move {filename}: {error_message}")
                        logger.error(f"Failed to move {filename}: {error_message}")

                    except OSError as os_error:
                        error_message = f"OS level error encountered: {os_error}"
                        print_message("error", f"Failed to move {filename}: OS Error ({os_error})")
                        logger.error(f"Failed to move {filename}: OS Error ({os_error})")

                    except RuntimeError as unexpected_error:
                        error_message = f"Unexpected runtime error: {unexpected_error}"
                        print_message("error", f"Failed to move {filename}: Unexpected Error ({error_message})")
                        logger.error(f"Failed to move {filename}: Unexpected Error ({error_message})")
                        break

        end_time = datetime.datetime.now()
        duration = end_time - start_time
        
        print(f"\n{PURPLE}--- Summary ---{RESET}")
        print(f"{BOLD}Files Moved:{RESET} {GREEN}{files_moved}{RESET}")
        print(f"{BOLD}Time elapsed:{RESET} {duration.total_seconds():.2f} seconds")


if __name__ == "__main__":
    # Enable ANSI colors for Windows CMD / PowerShell terminal sessions
    os.system('') 
    
    # Display the startup header banner
    print_ascii_banner("Omegazyph File Optimizer - CLI Mode")

    try:
        optimizer = FileOptimizerStandard()
    except RuntimeError:
        input(f"\n{RED}[X] Critical Initialization Error. Press Enter to exit...")
        sys.exit(1)

    user_input = input(f"\n{YELLOW}[!] Enter folder path to clean (or press Enter for current folder): {RESET}").strip()
    target = user_input if user_input else BASE_DIR
    
    optimizer.organize(target)
    
    # Display the completion closing banner
    print_ascii_ending("File Optimization Complete")
    
    input(f"\n{CYAN}[*] Press Enter to close...{RESET}")