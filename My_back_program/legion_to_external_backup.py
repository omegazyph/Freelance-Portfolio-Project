"""
Date: 2026-01-07
Script Name: legion_to_external_backup.py
Author: omegazyph
Updated: 2026-02-10
Description: Synchronizes multiple folders (Desktop and Portfolio) to 
              the LaCie (Z:) drive. Features a loop-based sync engine 
              and professional console-based status reporting.
"""

import os
import shutil
import time
import sys

def print_console_stream(text, color="\033[1;32m"):
    """
    Outputs text with a sequenced character delay to simulate a 
    live system console stream.
    """
    reset = "\033[0m"
    sys.stdout.write(color)
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.008)
    print(reset)

def sync_folders(source, destination):
    """
    Handles the incremental synchronization logic for specified 
    directory pairs. Returns a tuple of (updated_count, skipped_count).
    """
    updated_count = 0
    skipped_count = 0

    # Validate source path existence
    if not os.path.exists(source):
        print_console_stream(f"[-] ERROR: Source path '{source}' not found. Skipping...", "\033[1;31m")
        return 0, 0

    # Ensure target directory structure exists
    if not os.path.exists(destination):
        os.makedirs(destination)

    # Walk through the directory tree
    for root, directories, files in os.walk(source):
        # Exclude version control metadata to optimize sync speed
        if '.git' in directories:
            directories.remove('.git')

        # Determine relative path for the destination mapping
        relative_path = os.path.relpath(root, source)
        destination_directory = os.path.join(destination, relative_path)

        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)

        for filename in files:
            source_file = os.path.join(root, filename)
            destination_file = os.path.join(destination_directory, filename)

            # Performance check: Only transfer if file is new or modified
            if not os.path.exists(destination_file) or os.path.getmtime(source_file) > os.path.getmtime(destination_file):
                try:
                    # shutil.copy2 preserves original file metadata
                    shutil.copy2(source_file, destination_file)
                    updated_count += 1
                    print(f"\033[1;32m    [+] Synchronized: {filename}\033[0m")
                except Exception as error:
                    print(f"\033[1;31m    [!] IO Error on {filename}: {error}\033[0m")
            else:
                skipped_count += 1
                
    return updated_count, skipped_count

def run_backup_protocol():
    """
    Initializes the primary backup sequence for the Lenovo Legion.
    """
    # Refresh terminal window
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print_console_stream("======================================================")
    print_console_stream("   OMEGAZYPH SYSTEM SYNC PROTOCOL: LACIE_Z_DRIVE      ")
    print_console_stream("======================================================")

    # Hardware connection validation
    if not os.path.exists("Z:\\"):
        print_console_stream("[-] HARDWARE ERROR: LaCie Drive (Z:) is not accessible.", "\033[1;31m")
        return

    # --- CONFIGURATION: DIRECTORY MAPPING ---
    backup_tasks = {
        r"C:\Users\omega\Desktop\omegazyph": r"Z:\Windows\Documents\Git hub projects\omegazyph_back_up",
        r"C:\Users\omega\Desktop\Freelance-Portfolio-Project": r"Z:\Windows\Documents\Git hub projects\Freelance-Portfolio-Project_Back_up"
    }

    total_files_updated = 0
    total_files_skipped = 0

    # Execute synchronization for all mapped directories
    for source_path, destination_path in backup_tasks.items():
        folder_name = os.path.basename(source_path)
        print_console_stream(f"\n[*] INITIALIZING SYNC: {folder_name} -> EXTERNAL_Z")
        
        updates, skips = sync_folders(source_path, destination_path)
        total_files_updated += updates
        total_files_skipped += skips

    # Final Execution Report
    print_console_stream("\n" + "="*40)
    print_console_stream("        DATA SYNCHRONIZATION COMPLETE")
    print_console_stream("="*40)
    print_console_stream(f"  Total Files Processed: {total_files_updated}")
    print_console_stream(f"  Total Files Up-to-date: {total_files_skipped}")
    print_console_stream("="*40)
    print_console_stream("\n>>> SYSTEM SECURE. MONITORING IDLE.")

if __name__ == "__main__":
    try:
        run_backup_protocol()
    except KeyboardInterrupt:
        print("\n\033[1;31m[!] Operation Terminated by User.\033[0m")
        sys.exit()