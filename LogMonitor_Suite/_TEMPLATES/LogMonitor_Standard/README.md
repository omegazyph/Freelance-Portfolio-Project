# 🛡️ Advanced Log Monitoring Suite (Standard Edition)

Author: omegazyph
Date: 2026-02-14

##📄 Overview

The Standard Edition is a robust, configuration-driven utility designed for professional server environments. Unlike the basic version, this suite utilizes a JSON-based configuration system, allowing users to modify search parameters, file names, and reporting preferences without altering the source code.

## 📂 Project Structure

To ensure the path resolution logic works correctly, please maintain this structure:
Plaintext

LogMonitor_Standard/
├── config.json                # User-defined search settings
├── requirements.txt           # Environment documentation
├── logs/
│   └── system_activity.log    # Target log file
├── reports/                   # Destination for analysis files
└── scripts/
    ├── analyze_data.py        # Python processing engine
    └── monitor_logs.sh        # Bash environment controller

## ⚙️ Configuration (config.json)

You can customize the behavior of the script by editing the config.json file in the root directory:

    search_keywords: An array of strings the script will look for (e.g., ["ERROR", "CRITICAL", "AUTH_FAILURE"]).

    log_filename: The name of the file inside the /logs folder to be analyzed.

    report_prefix: The text that will appear at the start of your generated report filenames.

## 🚀 Execution Instructions

    Prepare the Environment: Ensure your log file is located in the logs/ directory.

    Configure Settings: Update config.json with your desired search terms.

    Run the Controller:
    Open Git Bash (on Windows) or a standard terminal (on Linux) and run:
    Bash

    bash scripts/monitor_logs.sh

    Review: Once the "Success" message appears, navigate to the reports/ folder to view your timestamped analysis.

## 🛠 Features

    Multi-Keyword Support: Scans for multiple error levels in a single pass.

    Environment Validation: The Bash controller automatically verifies that all directories and configuration files exist before execution.

    Absolute Path Mapping: High compatibility across Windows 11 and Linux systems.
    