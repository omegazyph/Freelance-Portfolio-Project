#!/usr/bin/env python

################################################################################
# Date:         2026-03-01
# Script Name:  File_Optimizer_Basic.py
# Author:       omegazyph
# Updated:      2026-09-24
# Description:  Basic CLI file optimizer using core standard libraries, simple
#               colored output, module-level logging, and explicit exception
#               handling.
#               Strict Dependency: Requires config_basic.json to execute.
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

# Base directory paths for configuration and log tracking
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config_basic.json")
LOG_PATH = os.path.join(BASE_DIR, "optimizer_basic_log.txt")

# Configure root logger parameters
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

# Instantiate module-level logger instance
logger = logging.getLogger(__name__)


# --- Helper Printing Functions ---

def print_message(message_type, message_text=""):
    """
    Prints status messages with simple ANSI color formatting.
    """
    if message_type == "error":
        print(f"{BOLD}{RED}[X] {message_text}{RESET}")
    elif message_type == "info":
        print(f"{BOLD}{BLUE}[*] {message_text}{RESET}")
    elif message_type == "success":
        print(f"{BOLD}{GREEN}[+] {message_text}{RESET}")
    elif message_type == "warning":
        print(f"{BOLD}{YELLOW}[!] {message_text}{RESET}")
    else:
        print(message_text)


# --- Core Class ---

class FileOptimizerBasic:
    def __init__(self):
        """
        Initializes the basic file optimizer and loads rules strictly from config_basic.json.
        """
        self.rules = self.load_config()

    def load_config(self):
        """
        Loads category rules strictly from config_basic.json.
        Terminates execution if the file is missing or corrupted.
        """
        if not os.path.exists(CONFIG_PATH):
            error_message = f"Missing required configuration file: '{CONFIG_PATH}'. Program cannot run without config_basic.json."
            print_message("error", error_message)
            logger.critical(error_message)
            raise FileNotFoundError(error_message)

        try:
            with open(CONFIG_PATH, "r") as file_handle:
                return json.load(file_handle)
        except (json.JSONDecodeError, OSError) as parse_error:
            error_message = f"Failed to parse config_basic.json: {parse_error}"
            print_message("error", error_message)
            logger.critical(error_message)
            raise FileNotFoundError(error_message)

    def organize(self, target_directory):
        """
        Scans target_directory and moves matching extensions to category subfolders.
        """
        target_directory = os.path.abspath(target_directory)

        if not os.path.exists(target_directory):
            error_message = f"The path '{target_directory}' does not exist."
            print_message("error", error_message)
            logger.error(error_message)
            return

        print_message("info", f"Scanning directory: {target_directory}")
        logger.info(f"Started basic scan on: {target_directory}")

        # Protect script files and internal tracking assets
        protected_files = [
            os.path.basename(__file__),
            "optimizer_basic_log.txt",
            "config_basic.json",
            "run_basic_optimizer.bat"
        ]

        files_moved = 0
        start_time = datetime.datetime.now()

        for filename in os.listdir(target_directory):
            file_path = os.path.join(target_directory, filename)

            # Ignore subdirectories and system protected files
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
                        logger.info(f"Moved file '{filename}' to '{category}'")
                        files_moved += 1
                        break
                    except shutil.Error as duplicate_error:
                        error_message = f"Destination file already exists in '{category}': {duplicate_error}"
                        print_message("warning", f"Skipped {filename}: {error_message}")
                        logger.warning(f"Skipped moving '{filename}': {error_message}")
                        break
                    except PermissionError:
                        error_message = f"Permission denied for '{filename}' (file may be open in another application)."
                        print_message("error", f"Failed to move {filename}: {error_message}")
                        logger.error(f"Failed to move '{filename}': {error_message}")
                        break
                    except FileNotFoundError:
                        error_message = f"Source path missing for '{filename}'."
                        print_message("error", f"Failed to move {filename}: {error_message}")
                        logger.error(f"Failed to move '{filename}': {error_message}")
                        break
                    except OSError as os_error:
                        error_message = f"OS level error encountered: {os_error}"
                        print_message("error", f"Failed to move {filename}: {error_message}")
                        logger.error(f"Failed to move '{filename}': {error_message}")
                        break
                    except RuntimeError as unexpected_error:
                        error_message = f"Unexpected runtime error: {unexpected_error}"
                        print_message("error", f"Failed to move {filename}: {error_message}")
                        logger.error(f"Failed to move '{filename}': {error_message}")
                        break

        end_time = datetime.datetime.now()
        duration = end_time - start_time

        logger.info(f"Basic optimization completed. Total files moved: {files_moved}")

        print(f"\n{BOLD}=== Execution Summary ==={RESET}")
        print(f"Files Moved: {GREEN}{files_moved}{RESET}")
        print(f"Time Elapsed: {duration.total_seconds():.2f} seconds")


if __name__ == "__main__":
    # Enable ANSI color rendering in Windows terminals
    os.system("")

    print(f"{BOLD}{PURPLE}===================================================={RESET}")
    print(f"{BOLD}{BLUE}       Omegazyph File Optimizer - Basic CLI        {RESET}")
    print(f"{BOLD}{PURPLE}===================================================={RESET}\n")

    try:
        optimizer = FileOptimizerBasic()
    except RuntimeError:
        input(f"\n{RED}[X] Critical Initialization Error. Press Enter to exit...{RESET}")
        sys.exit(1)

    user_input = input(f"{YELLOW}[!] Enter folder path to clean (or press Enter for current folder): {RESET}").strip()
    target = user_input if user_input else BASE_DIR

    optimizer.organize(target)

    input(f"\n{BLUE}[*] Process completed. Press Enter to close...{RESET}")