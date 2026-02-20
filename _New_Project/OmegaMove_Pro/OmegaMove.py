"""
Date: 2026-02-20
Script Name: OmegaMove.py
Author: omegazyph
Updated: 2026-02-20
Description: Sub-Domain JSON Migration Tool. Reads a list of folders 
              from settings.json, ensures they exist locally, and 
              migrates their contents to matching server folders.
"""

import os
import time
import sys
import subprocess
import shutil
import json
import logging

# =============================================================================
# PATH STABILIZATION
# =============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "settings.json")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

logging.basicConfig(
    filename=os.path.join(LOGS_DIR, "migration_log.txt"),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def print_hacker(text, color="\033[1;32m"):
    """Prints text with the signature typewriter effect."""
    reset = "\033[0m"
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.005)
    print(reset)

def load_config():
    """Loads settings from the JSON file."""
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print_hacker(f"[-] ERROR: Config file not found at {CONFIG_PATH}", "\033[1;31m")
        sys.exit(1)

def run_migration():
    """Main loop for the JSON-defined Sub-Domain service."""
    config = load_config()
    main_drop_zone = config['paths']['drop_zone']
    sub_domains = config['paths']['sub_domains']
    server = f"{config['connection']['username']}@{config['connection']['server_ip']}"
    remote_base = config['paths']['remote_base_directory']
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print_hacker("======================================================")
    print_hacker("   OMEGAMOVE PRO: JSON SUB-DOMAIN MODE                ")
    print_hacker("======================================================")

    # Pre-flight: Ensure the folders in the JSON exist on your Desktop
    for sub in sub_domains:
        local_sub_path = os.path.join(main_drop_zone, sub)
        if not os.path.exists(local_sub_path):
            os.makedirs(local_sub_path)
            print(f"[*] Initialized folder: {sub}")

    while True:
        # Loop through the folders defined in the JSON list
        for sub in sub_domains:
            local_mailbox_path = os.path.join(main_drop_zone, sub)
            
            # Check for files inside this specific sub-domain
            try:
                contents = os.listdir(local_mailbox_path)
            except FileNotFoundError:
                os.makedirs(local_mailbox_path)
                continue
                
            for item_name in contents:
                if item_name.lower() == "desktop.ini":
                    continue

                local_item_path = os.path.join(local_mailbox_path, item_name)
                remote_dest = f"{server}:{remote_base}{sub}/"

                is_dir = os.path.isdir(local_item_path)
                scp_flags = "-rp" if is_dir else "-p"

                print_hacker(f"\n[!] DATA IN {sub.upper()}: {item_name}")
                
                try:
                    # Create matching directory on ThinkCentre
                    subprocess.run(["ssh", server, f"mkdir -p {remote_base}{sub}"], 
                                   check=True, capture_output=True)
                    
                    # Execute Transfer
                    subprocess.run(["scp", scp_flags, local_item_path, remote_dest], 
                                   check=True, capture_output=True)
                    
                    # Cleanup: Remove file/folder inside, keep the sub-domain folder
                    if not config['preferences']['dry_run']:
                        if is_dir:
                            shutil.rmtree(local_item_path)
                        else:
                            os.remove(local_item_path)
                        
                        logging.info(f"SUCCESS: Moved {item_name} from {sub}")
                        print_hacker(f"    [+] {item_name} sent to server/{sub}. Local folder preserved.")
                
                except Exception as e:
                    logging.error(f"TRANSFER ERROR in {sub}: {str(e)}")
                    print(f"    [-] ERROR: {e}")

        time.sleep(config['connection']['check_interval_seconds'])

if __name__ == "__main__":
    try:
        run_migration()
    except KeyboardInterrupt:
        print_hacker("\n[!] Service Terminated.", "\033[1;31m")
        sys.exit()