"""
Date:           2026-01-05
Script Name:    Advanced_Optimizer.py
Author:         omegazyph
Updated:        2026-02-16
Description:    Advanced Tier: Professional directory organizer with 
                ANSI color reporting, self-healing JSON configuration, 
                collision detection, and automated activity logging.
"""

import os
import shutil
import logging
import json

# ---------------------------------------------------------
# 1. VISUAL THEMING (ANSI COLORS)
# We use these to make the terminal output look like a 
# real application rather than just plain text.
# ---------------------------------------------------------
class Colors:
    HEADER    = '\033[95m'
    BLUE      = '\033[94m'
    CYAN      = '\033[96m'
    GREEN     = '\033[92m'
    YELLOW    = '\033[93m'
    RED       = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'

# ---------------------------------------------------------
# 2. SETUP, LOGGING, AND CONFIGURATION
# ---------------------------------------------------------

# Using absolute paths so the script works correctly even if 
# called from a different directory (like via a shortcut).
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(SCRIPT_DIR, 'logs')
CONFIG_DIR = os.path.join(SCRIPT_DIR, 'config')

# Ensure our support folders exist before we try to write to them.
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)

# Set up logging to catch "behind the scenes" events.
# We use 'a' (append) so we don't wipe previous history.
log_filename = os.path.join(LOG_DIR, 'organization_activity.log')
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a' 
)

def load_config():
    """Handles the JSON config. If it's missing, we build it from scratch."""
    config_file = os.path.join(CONFIG_DIR, 'config.json')
    
    # Default categorization: The client can change these in the JSON file later.
    default_groups = {
        'Documents':   ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.pptx'],
        'Images':      ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp'],
        'Videos':      ['.mp4', '.mov', '.avi', '.mkv'],
        'Audio':       ['.mp3', '.wav', '.flac', '.m4a'],
        'Compressed':  ['.zip', '.rar', '.7z', '.tar'],
        'Development': ['.py', '.sh', '.html', '.css', '.js', '.md'],
        'Executables': ['.exe', '.msi', '.bat']
    }
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            # If the JSON is broken (e.g., missing a comma), fall back to defaults.
            logging.error(f"Config corrupted: {e}")
            return default_groups
    else:
        try:
            with open(config_file, 'w') as f:
                json.dump(default_groups, f, indent=4)
            logging.info("New config.json created successfully in /config/ folder.")
        except Exception as e:
            logging.error(f"Failed to create config: {e}")
            
    return default_groups

# Load the mapping once at the start of the script.
FILE_GROUPS = load_config()

# ---------------------------------------------------------
# 3. CORE LOGIC FUNCTIONS
# ---------------------------------------------------------

def get_target_folder(file_extension):
    """Simple lookup to find which category a file belongs to."""
    for folder_name, extensions in FILE_GROUPS.items():
        if file_extension in extensions:
            return folder_name
    return "Others" # Catch-all for unknown file types.

def organize_files(target_path):
    """The heavy lifting: scans, renames (if needed), and moves files."""
    if not os.path.exists(target_path):
        print(f"{Colors.RED}❌ Error: Path not found: {target_path}{Colors.ENDC}")
        logging.error(f"Target path not found: {target_path}")
        return 0, {}

    # Hold onto the original location so we can jump back later.
    original_dir = os.getcwd()
    os.chdir(target_path)
    
    count = 0
    stats = {} 
    
    # We only want files. We ignore folders and the script itself to prevent recursion.
    all_items = [f for f in os.listdir(target_path) if os.path.isfile(f) and f != os.path.basename(__file__)]
    
    if not all_items:
        print(f"{Colors.GREEN}✨ Your folder is already clean!{Colors.ENDC}")
        return 0, {}

    print(f"{Colors.BLUE}📂 Scanning {len(all_items)} files at {target_path}...{Colors.ENDC}\n")
    logging.info(f"Starting organization session in: {target_path}")

    for filename in all_items:
        extension = os.path.splitext(filename)[1].lower()
        folder = get_target_folder(extension)

        # Create the sub-category folder if it doesn't already exist.
        os.makedirs(folder, exist_ok=True)
        destination = os.path.join(folder, filename)

        # COLLISION CHECK: If a file with the same name exists, we append '_Copy'.
        # This is safer than just overwriting the client's data!
        if os.path.exists(destination):
            name, ext = os.path.splitext(filename)
            new_name = f"{name}_Copy{ext}"
            destination = os.path.join(folder, new_name)
            logging.warning(f"Collision: {filename} exists in {folder}. Saved as {new_name}")

        try:
            shutil.move(filename, destination)
            # We trim the filename in the terminal so it doesn't break the layout.
            display_name = (filename[:30] + '..') if len(filename) > 30 else filename
            print(f"  {Colors.GREEN}✔{Colors.ENDC} {display_name.ljust(33)} → {Colors.CYAN}{folder}{Colors.ENDC}")
            
            logging.info(f"SUCCESS: Moved {filename} to {folder}")
            count += 1
            stats[folder] = stats.get(folder, 0) + 1
        except Exception as error:
            # We log the error but keep the loop running so one bad file doesn't stop the whole process.
            logging.error(f"FAILURE: Could not move {filename}. Error: {error}")

    # Return to where we started.
    os.chdir(original_dir)
    return count, stats

# ---------------------------------------------------------
# 4. SCRIPT EXECUTION
# ---------------------------------------------------------

if __name__ == "__main__":
    # In a real freelance gig, you might ask the user for a path, 
    # but defaulting to Downloads is a great "Out of the box" experience.
    downloads_path = os.path.expanduser("~/Downloads")
    
    # Header UI: Makes the script look professional immediately upon launch.
    print(f"\n{Colors.BLUE}╔" + "═" * 58 + "╗")
    print(f"║{Colors.HEADER}{Colors.BOLD}          OMEGAZYPH DIRECTORY OPTIMIZER v2.0              {Colors.ENDC}{Colors.BLUE}║")
    print("╚" + "═" * 58 + f"╝{Colors.ENDC}\n")
    
    total_moved, folder_stats = organize_files(downloads_path)
    
    # If we actually moved things, show the final report table.
    if total_moved > 0:
        print(f"\n{Colors.BOLD}{Colors.UNDERLINE}ORGANIZATION SUMMARY{Colors.ENDC}")
        print(f"{Colors.BLUE}┌──────────────────────────────┬──────────┐")
        print("│ Category                     │ Count    │")
        print("├──────────────────────────────┼──────────┤")
        for folder, amount in folder_stats.items():
            print(f"│ {folder.ljust(28)} │ {str(amount).ljust(8)} │")
        print(f"└──────────────────────────────┴──────────┘{Colors.ENDC}")
        
        logging.info(f"Session finished. Total files moved: {total_moved}")
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}  ✅ PROCESS COMPLETE: {total_moved} files relocated.{Colors.ENDC}")
    print(f"{Colors.CYAN}  📄 History saved to: /logs/organization_activity.log{Colors.ENDC}\n")