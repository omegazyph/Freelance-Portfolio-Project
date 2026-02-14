# 🚀 Enterprise Log Intelligence Suite (Advanced Edition)

Author: omegazyph
Project Date: 2026-01-05
Last Updated: 2026-02-14

## 📄 Overview

The Advanced Edition is a professional-grade log parsing engine built for modularity and data portability. This suite transitions from simple text reporting to Structured Data Export (CSV), allowing system administrators to import log analysis directly into Excel, Power BI, or Google Sheets for trend visualization.

## 📂 Project Structure

Plaintext

LogMonitor_Advanced/
├── config.json                # Advanced search & retention settings
├── requirements.txt           # Environment & dependency manifest
├── logs/
│   └── system_activity.log    # Source log file
├── reports/                   # CSV export destination
└── scripts/
    ├── analyze_data.py        # Modular Python engine
    └── monitor_logs.sh        # Advanced Bash controller

## ⚙️ Advanced Configuration (config.json)

The JSON configuration allows for deep customization:

    search_keywords: List as many triggers as needed (e.g., ["CRITICAL", "ERROR", "TIMEOUT"]).

    export_format: Set to "csv" for spreadsheet compatibility.

    retention_policy_days: Define how long logs should be kept (for future automation).

## 🚀 Getting Started

    Installation:
    Open your terminal (Git Bash on Windows) and install optional reporting dependencies:
    Bash

    pip install -r requirements.txt

    Execution:
    Run the controller from the project root:
    Bash

    bash scripts/monitor_logs.sh

    Data Access:
    Navigate to the reports/ folder. You will find a timestamped .csv file.

## 🛠 Advanced Features

    Modular Architecture: The Python engine is broken into functions, making it easy to integrate into larger CI/CD pipelines.

    Data Integrity: Includes environment self-checks to ensure no data is processed if the configuration is corrupted.

    Excel Ready: Output is pre-formatted with headers (Line, Timestamp, Content) for immediate professional use.
