# omegazyph Local Backup Suite (Basic)

**Version:** 1.0  
**Author:** omegazyph  
**Updated:** 2026-02-14

## Description

The Local Backup Suite is a lightweight, reliable Bash automation tool designed to protect your data. It creates timestamped, compressed archives (.tar.gz) of your critical directories and maintains a detailed log of every operation.

## Key Features

* **Automated Compression:** Uses Gzip compression to save disk space.
* **Timestamping:** Every backup is uniquely named (e.g., `backup_2026-02-14_09-00.tar.gz`).
* **Audit Logging:** Success and error messages are recorded in a dedicated log file.
* **Zero Dependencies:** Runs on native Linux tools (Bash and Tar).

## Installation & Usage

1. **Prepare the Script:**
   Move the `backup_local.sh` script to your desired folder.
  
2. **Grant Permissions:**
   Open your terminal and run:
   bash
   chmod +x backup_local.sh

    Configure Paths:
    Open the script in a text editor (like VSCode) and update the following variables to match your system:

        SOURCE_DIR: The folder you want to protect.

        BACKUP_DIR: Where you want the backups stored.

    Run the Backup:
    Bash

    ./backup_local.sh

## File Structure

    backup_local.sh: The main automation script.

    backup_log.txt: Generated log file (created after the first run).