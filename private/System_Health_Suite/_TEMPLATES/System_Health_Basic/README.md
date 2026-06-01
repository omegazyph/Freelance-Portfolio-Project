# System Health Monitor (Basic Tier)

**Author:** omegazyph  
**Date:** 2026-02-13  
**Description:** Lightweight system check for Linux servers.

## 🚀 Features

* **Disk Check:** Reports usage for all partitions and flags levels over 80%.
* **Memory Check:** Displays used vs. total RAM.
* **CPU Load:** Shows the 1-minute load average.
* **Logging:** Automatically saves every report to the `/Logs` folder.

## 💻 How to Use

1. Give the script execution permissions:
   `chmod +x Scripts/health_check_basic.sh run_check.sh`
2. Run the tool:
   `./run_check.sh`

## 🛠 Requirements

 Linux environment (tested on Parrot OS/Ubuntu).
 Standard utilities: `df`, `free`, `uptime`.
