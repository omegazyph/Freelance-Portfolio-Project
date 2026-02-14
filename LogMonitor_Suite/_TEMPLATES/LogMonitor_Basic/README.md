# LOG MONITORING SYSTEM

Author: omegazyph
Date: 2026-02-14

## 📄 Description

This is an automated log analysis tool designed to streamline server maintenance. It uses a Bash Controller to validate the environment and manage report cleanup, while a Python Engine performs high-speed keyword extraction from system logs.

## 📂 Project Structure

For the script to function correctly on your system, please maintain the following file hierarchy:
Plaintext

LogMonitor_Project/
├── logs/
│   └── system_activity.log        # Your source log file goes here
├── reports/                       # Generated analysis reports go here
└── scripts/
    ├── analyze_data.py            # Python analysis engine
    └── monitor_logs.sh            # Primary Bash controller

## 🛠 Prerequisites

    Python 3.x: Ensure Python is installed and added to your system PATH.

    Bash Environment: * Windows: Use Git Bash (recommended for VS Code).

        Linux/Mac: Standard Terminal.

## 🚀 How to Use

    Place your log file (system_activity.log) inside the logs folder.

    Open your terminal and navigate to the scripts directory.

    Execute the Bash controller:
    Bash

    bash monitor_logs.sh

    Follow the on-screen prompts to either perform a cleanup of old reports or proceed with the analysis.

    Check the reports folder for your timestamped summary.

## ⚙️ Features

    Path Independence: Uses absolute path resolution so scripts can be executed from any directory without breaking.

    Smart Cleanup: Optional automated deletion of reports older than 30 days.

    Error Extraction: Specifically targets and catalogs ERROR and CRITICAL events for quick review.
