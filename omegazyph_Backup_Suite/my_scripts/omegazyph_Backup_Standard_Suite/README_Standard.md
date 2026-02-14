# omegazyph Backup & Maintenance Suite (Standard)

**Version:** 1.0  
**Author:** omegazyph  
**Updated:** 2026-02-14

## Description

The Standard Suite is an automated data protection tool designed for hands-off server management. In addition to secure backups, it includes a "Retention Engine" that automatically manages your disk space by rotating out old archives.

## Key Features

* **Automated Compression:** High-efficiency Gzip archiving.
* **Smart Retention:** Automatically deletes backups older than 14 days (customizable).
* **Disk Space Protection:** Prevents server crashes caused by backup-related disk bloat.
* **Detailed Audit Logs:** Tracks both creation and deletion of files.

## Installation & Configuration

1. **Permissions:**
    '''bash
   chmod +x Scripts/backup_standard.sh

    Configuration:
    Open backup_standard.sh in VSCode and adjust:

        SOURCE_DIR: Your data source.

        RETENTION_DAYS: Set how many days of history you want to keep.

    Execution:
    Bash

    ./Scripts/backup_standard.sh
