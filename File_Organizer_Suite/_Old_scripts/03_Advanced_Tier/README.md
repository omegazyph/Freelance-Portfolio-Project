# 📂 OMEGAZYPH Directory Optimizer v2.0

Professional File Management & Automation Suite

The OMEGAZYPH Directory Optimizer is an advanced Python-based utility designed to solve the problem of digital clutter. Developed for high-performance environments, it transforms unorganized directories into structured, categorized ecosystems with a single click.

## 💎 Premium Features

    🛡️ Data-Safe Collision Detection: Unlike basic scripts that overwrite files, this suite detects naming conflicts and intelligently renames duplicates (e.g., invoice.pdf becomes invoice_Copy.pdf).

    📑 Dynamic Tabular Reporting: View your results in a professional ANSI-colored summary table directly in your terminal.

    ⚙️ Self-Healing Configuration: The script manages its own dependencies. If config.json is missing, the system reconstructs it automatically in the /config folder.

    📜 Audit-Ready Logging: Maintains a persistent history of every file moved, renamed, or failed in /logs/organization_activity.log—perfect for troubleshooting or verification.

    ⚡ Universal Deployment: Native support for both Windows (CMD/PowerShell) and Unix-based systems (Bash/Git Bash/WSL).

## 🛠️ Quick Start

Option A: Windows (Double-Click Setup)

    Locate setup_windows.bat.

    Double-click to run.

    The script will check for Python, verify requirements.txt, and offer to launch the optimizer.

Option B: Linux / macOS / Git Bash

    Open your terminal in the project directory.

    Execute the following:
    Bash

    chmod +x setup_bash.sh && ./setup_bash.sh

## 📁 System Architecture

    File/Folder Purpose
    Advanced_Optimizer.py   The core automation engine (Python 3).
    setup_windows.bat       One-click installer for Windows environments.
    setup_bash.sh           Native installer for Bash-compliant systems.
    config/                 Stores config.json for custom extension mapping.
    logs/                   Stores detailed execution history and error reports.
    requirements.txt        Lists the standard library dependencies for the suite.

## 🛠️ Customization

You can tailor the organization logic without touching the Python code. Simply open config/config.json and modify the extension arrays:
JSON

{
    "Development": [".py", ".sh", ".js", ".html", ".css"],
    "Custom_Category": [".xyz", ".abc"]
}

Author: omegazyph

Updated: 2026-02-16

System Requirements: Python 3.x installed on a Windows 10/11 or Unix-based system.

Developed and Optimized on Lenovo Legion.
