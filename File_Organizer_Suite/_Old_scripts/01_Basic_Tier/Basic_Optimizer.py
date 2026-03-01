"""
Date:           2026-01-05
Script Name:    Basic_Optimizer.py
Author:         omegazyph
Updated:        2026-02-16
Description:    Basic Tier: Essential directory cleanup for Windows/Mac/Linux.
                Hardcoded categories for zero-configuration, "plug-and-play" use.
"""

import os
import shutil

# Standard ANSI Colors (Works in VSCode and Windows Terminal)
BLUE = '\033[94m'
GREEN = '\033[92m'
CYAN = '\033[96m'
ENDC = '\033[0m'
BOLD = '\033[1m'

def run_basic():
    # Dynamic Path: Correctly finds 'C:\Users\Wayne Stock\Downloads'
    target = os.path.expanduser("~/Downloads")
    
    # Basic Hardcoded Categories
    groups = {
        "Images":    [".jpg", ".jpeg", ".png", ".gif"],
        "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
        "Videos":    [".mp4", ".mkv", ".mov"]
    }
    
    print(f"{BLUE}=================================================={ENDC}")
    print(f"{GREEN}{BOLD}      OMEGAZYPH BASIC OPTIMIZER (PY)              {ENDC}")
    print(f"{BLUE}=================================================={ENDC}")
    print(f"{CYAN}📂 Targeting: {target}{ENDC}\n")

    if not os.path.exists(target):
        print(f"Error: Could not find {target}")
        return

    # Store original location
    original_dir = os.getcwd()
    os.chdir(target)
    count = 0

    for filename in os.listdir('.'):
        # Ensure we are moving files and not our own script
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
                    except Exception:
                        pass

    os.chdir(original_dir)
    print(f"\n{GREEN}{BOLD}Basic Optimization Complete: {count} files moved.{ENDC}")

if __name__ == "__main__":
    run_basic()