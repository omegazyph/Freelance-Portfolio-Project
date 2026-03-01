# Date: 2026-03-01
# Script Name: File_Optimizer_Standard.py
# Author: omegazyph
# Updated: 2026-03-01
# Description: A professional CLI-based file organization utility for Windows 11.
# Uses a JSON configuration for easy customization of file categories.

import os
import shutil
import json
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename='optimizer_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class FileOptimizerStandard:
    def __init__(self, config_path='config.json'):
        self.config_path = config_path
        self.rules = self.load_config()

    def load_config(self):
        """Loads the directory rules from a JSON file."""
        default_rules = {
            "Images": [".jpg", ".jpeg", ".png", ".gif"],
            "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
            "Videos": [".mp4", ".mkv", ".mov"],
            "Archives": [".zip", ".rar", ".7z"]
        }
        
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        else:
            # Create default config if missing
            with open(self.config_path, 'w') as f:
                json.dump(default_rules, f, indent=4)
            return default_rules

    def organize(self, target_directory):
        """Iterates through files and moves them based on extension."""
        if not os.path.exists(target_directory):
            print(f"Error: Directory {target_directory} not found.")
            return

        print(f"Starting organization in: {target_directory}")
        logging.info(f"Started cleaning: {target_directory}")

        for filename in os.listdir(target_directory):
            file_path = os.path.join(target_directory, filename)
            
            # Skip directories
            if os.path.isdir(file_path):
                continue

            extension = os.path.splitext(filename)[1].lower()
            
            for category, extensions in self.rules.items():
                if extension in extensions:
                    dest_dir = os.path.join(target_directory, category)
                    os.makedirs(dest_dir, exist_ok=True)
                    
                    try:
                        shutil.move(file_path, os.path.join(dest_dir, filename))
                        print(f"Moved: {filename} -> {category}")
                        logging.info(f"Moved: {filename} to {category}")
                    except Exception as e:
                        logging.error(f"Failed to move {filename}: {e}")

        print("Organization complete. Check optimizer_log.txt for details.")

if __name__ == "__main__":
    # Standard version uses the current directory as default
    optimizer = FileOptimizerStandard()
    current_dir = os.getcwd()
    optimizer.organize(current_dir)