"""
Date:           2026-01-04
Script Name:    Advanced_Optimizer.py
Author:         omegazyph
Updated:        2026-02-11
Description:    Advanced Tier: Professional directory organizer with 
                collision detection, logging, and visual progress reporting.
"""

import os
import shutil
import logging

# 1. SETUP AND CONFIGURATION
# ---------------------------------------------------------
# Set logging to only show Errors for a clean user experience
logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')

FILE_GROUPS = {
    'Documents':   ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.pptx'],
    'Images':      ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp'],
    'Videos':      ['.mp4', '.mov', '.avi', '.mkv'],
    'Audio':       ['.mp3', '.wav', '.flac', '.m4a'],
    'Compressed':  ['.zip', '.rar', '.7z', '.tar'],
    'Development': ['.py', '.sh', '.html', '.css', '.js', '.md'],
    'Executables': ['.exe', '.msi', '.bat']
}

# 2. CORE LOGIC FUNCTIONS
# ---------------------------------------------------------

def get_target_folder(file_extension):
    """Matches a file extension to its corresponding category folder."""
    for folder_name, extensions in FILE_GROUPS.items():
        if file_extension in extensions:
            return folder_name
    return "Others"

def organize_files(target_path):
    """Scans the directory and relocates files to categorized folders."""
    if not os.path.exists(target_path):
        print(f"❌ Error: Path not found: {target_path}")
        return 0

    os.chdir(target_path)
    count = 0
    
    # Filter for files only, excluding the script itself if it is in the same folder
    all_items = [f for f in os.listdir(target_path) if os.path.isfile(f) and f != os.path.basename(__file__)]
    
    if not all_items:
        print("✨ Your folder is already clean!")
        return 0

    print(f"📂 Scanning {len(all_items)} files at {target_path}...\n")

    for filename in all_items:
        extension = os.path.splitext(filename)[1].lower()
        folder = get_target_folder(extension)

        # Ensure the category folder exists
        os.makedirs(folder, exist_ok=True)
        destination = os.path.join(folder, filename)

        # Collision Check: Prevent overwriting files with the same name
        if os.path.exists(destination):
            name, ext = os.path.splitext(filename)
            destination = os.path.join(folder, f"{name}_Copy{ext}")

        try:
            shutil.move(filename, destination)
            # Visual feedback with string slicing for long filenames
            display_name = (filename[:30] + '..') if len(filename) > 30 else filename
            print(f"  → Moved: {display_name.ljust(33)} to [{folder}]")
            count += 1
        except Exception as error:
            logging.error(f"Could not move {filename}: {error}")

    return count

# 3. SCRIPT EXECUTION
# ---------------------------------------------------------

if __name__ == "__main__":
    # Default path for Windows users (Wayne's Legion setup)
    # Using expanduser ensures 'C:/Users/omega/' works for your specific profile
    downloads_path = os.path.expanduser("C:/Users/omega/Downloads")
    
    print("\n" + "⭐" * 50)
    print("      OMEGAZYPH DIRECTORY OPTIMIZER v2.0")
    print("⭐" * 50 + "\n")
    
    total_moved = organize_files(downloads_path)
    
    print("\n" + "─" * 50)
    print(f"✅ DONE! {total_moved} files have been organized.")
    print("─" * 50 + "\n")