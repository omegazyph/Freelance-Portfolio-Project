# System Health & Auto-Cleanup (Standard Tier)

**Author:** omegazyph  
**Date:** 2026-02-13

## 🌟 Key Features

* **Automated Maintenance:** Automatically clears old files in `/tmp` if disk usage exceeds 80%.
* **Log Management:** Features built-in log rotation to ensure the script never consumes unnecessary disk space.
* **Full Reporting:** Captured metrics include Disk, RAM, and CPU Load averages.

## 💻 Usage

1. Set permissions: `chmod +x Scripts/health_check_standard.sh run_standard.sh`
2. Run the tool: `./run_standard.sh`

## ⚙️ Requirements

 Linux OS (Tested on Parrot/Ubuntu)
 Root/Sudo privileges may be required for certain cleanup tasks.
