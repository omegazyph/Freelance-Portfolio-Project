# File Optimizer Standard (CLI Edition)

**Author:** omegazyph  
**Date:** 2026-03-01  
**Updated:** 2026-09-24  
**Description:** Professional color-coded CLI utility for Windows 11 file organization utilizing core library UI components and modular logging.

---

## 1. Overview

File Optimizer Standard is a Command Line Interface (CLI) application designed to scan directories and categorize loose files into structured subfolders automatically. It features dynamic ASCII title banners, color-coded status outputs, robust error handling, and configurable folder rules via JSON.

---

## 2. File Architecture

* `File_Optimizer_Standard.py` - Core Python engine containing directory scanning logic and exception handling.
* `config.json` - Local configuration file defining category names and file extension mapping arrays.
* `optimizer_log.txt` - Runtime log file storing timestamped execution details and error events.
* `run_optimizer.bat` - Windows executable batch file for one-click startup execution.
* `README.md` - Technical documentation and operational guide.

---

## 3. How to Use

1. Execute `run_optimizer.bat` or run `python File_Optimizer_Standard.py` directly from your terminal.
2. The interface will render a dynamically centered ANSI header banner.
3. When prompted, specify the folder to optimize:
   * Enter or paste an absolute folder path (e.g., `C:\Users\Name\Downloads`).
   * Press **[ENTER]** without typing a path to default to the script's current directory.
4. The scanner will process files line-by-line, displaying color-coded status indicators:
   * **GREEN `[+]`** - File moved successfully to its target folder.
   * **YELLOW `[!]`** - File skipped (file already exists in target destination).
   * **RED `[X]`** - Access or filesystem error encountered.
5. Review the execution summary displaying the total count of moved files and elapsed processing time.

---

## 4. Customizing Rules (`config.json`)

You can edit file categorization rules at any time by modifying `config.json` in any standard text editor. Example structure:

json

{
  
  "Images": [".jpg", ".jpeg", ".png", ".gif"],

  "Documents": [".pdf", ".docx", ".txt", ".xlsx"],

  "Videos": [".mp4", ".mkv", ".mov"],

  "Archives": [".zip", ".rar", ".7z"]

}

If config.json is deleted or missing, the application automatically generates a fresh configuration file populated with default rules.

## 5. Safety & System Architecture

  Self-Protection Protection: The engine checks file names and automatically excludes File_Optimizer_Standard.py, config.json, optimizer_log.txt, and run_optimizer.bat from being moved.

   Non-Recursive Execution: The scanner only operates on files located at the top level of the target directory; existing subfolders and their contents are never altered or moved.

   Targeted Exception Handling: Specific handlers manage duplicate destination files (shutil.Error), open or locked files (PermissionError), and missing paths (FileNotFoundError) without halting the scan.

   Detailed Logging: All operations and warnings are recorded to optimizer_log.txt using Python's standard logging library for debugging and auditing.

## 6. Support & Feedback

For technical support, custom automation scripts, or feature enhancements, contact omegazyph via the Upwork dashboard.
