# File Optimizer Basic (CLI Edition)

**Author:** omegazyph  
**Date:** 2026-03-01  
**Updated:** 2026-09-24  
**Description:** Lightweight color-coded CLI utility for Windows 11 file organization utilizing core Python libraries and clean exception handling.

---

## 1. Overview

File Optimizer Basic is a simple, lightweight Command Line Interface (CLI) utility designed to organize loose files into category folders based on their file extensions. It provides standard ANSI color-coded status messages, run logging, and a straight-forward JSON configuration structure.

---

## 2. File Architecture

* `File_Optimizer_Basic.py` - Core Python script containing directory scanning and file-moving logic.

* `config_basic.json` - Direct extension-to-category mapping rules.

* `optimizer_basic_log.txt` - Runtime log file recording scan activity and system messages.

* `README.md` - Technical documentation and quick-start guide.

---

## 3. How to Use

1. Run `python File_Optimizer_Basic.py` directly in your terminal.

2. The terminal will display the welcome header banner.

3. When prompted, enter the target directory:
   * Type or paste a target folder path (e.g., `C:\Users\Name\Downloads`).
   * Press **[ENTER]** without typing a path to default to the script's directory.

4. The script will move files line-by-line while displaying colored status tags:
   * **GREEN `[+]`** - File moved successfully.
   * **YELLOW `[!]`** - File skipped (destination file already exists).
   * **RED `[X]`** - Access or filesystem error encountered.

5. Review the execution summary at the end for the total count of files moved.

---

## 4. Configuration (`config_basic.json`)

The basic edition uses a direct key-value mapping structure for categories and file extension arrays. You can edit categories or add new extensions in any standard text editor:

Images: .jpg, .jpeg, .png, .gif

Documents: .pdf, .docx, .txt, .xlsx,

Videos: .mp4, .mkv, .mov,

Archives: .zip, .rar, .7z

Note: File_Optimizer_Basic.py strictly requires config_basic.json to be present in the same folder to execute.

## 5. Safety & Protection Features

Self-Protection: The script automatically ignores File_Optimizer_Basic.py, config_basic.json, optimizer_basic_log.txt, and run_basic_optimizer.bat.

Top-Level Only: Scans only the top level of the specified directory; existing subdirectories are left untouched.

Granular Exception Handling: Catches file collisions (shutil.Error), locked files (PermissionError), and missing files (FileNotFoundError) without crashing the script.

Audit Trail: Logs every run event and execution summary to optimizer_basic_log.txt.

## 6. Support

For technical questions or custom script requests, contact omegazyph via the Upwork dashboard.
