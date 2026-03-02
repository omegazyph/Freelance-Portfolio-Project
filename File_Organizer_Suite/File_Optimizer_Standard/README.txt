===========================================================
PROJECT NAME: File Optimizer Standard (CLI Edition)
AUTHOR:       omegazyph
DATE:         2026-03-01
UPDATED:      2026-03-01
DESCRIPTION:  Professional Color-Coded CLI Utility for 
              Windows 11 File Organization.
===========================================================

### 1. OVERVIEW
This is a professional Command Line Interface (CLI) tool designed 
to categorize files automatically. It features color-coded status 
updates, execution summaries, and customizable organization rules.

### 2. PACKAGE CONTENTS
- File_Optimizer_Standard.py : The core Python logic.
- run_optimizer.bat          : A one-click Windows launcher.
- config.json                : Your custom organization rules.
- README.txt                 : This instruction manual.

### 3. HOW TO USE
1. Double-click 'run_optimizer.bat'.
2. The terminal will open with a color-coded welcome screen.
3. ENTER TARGET PATH:
   - Type or paste a full path (e.g., C:\Users\Name\Downloads).
   - OR simply press [ENTER] to clean the current folder.
4. The tool will display color-coded "Moved" or "Error" statuses.
5. Review the summary at the end for the total count of files moved.

### 4. CONFIGURATION (config.json)
The 'config.json' file allows you to define folder names and 
extensions. 
- GREEN text in the terminal confirms a successful move.
- YELLOW text shows the direction of the file movement.
- RED text indicates a system error or missing path.

### 5. SAFETY FEATURES
- SELF-PROTECTION: The script is programmed to ignore itself, the 
  batch file, and its log files.
- TOP-LEVEL ONLY: The tool only organizes files in the main folder 
  and will NEVER enter or modify your existing subfolders.
- LOGGING: A detailed 'optimizer_log.txt' is generated in the 
  script directory for every run.

### 6. SUPPORT
For technical support or to request custom feature additions, 
please contact omegazyph via the Upwork dashboard.
===========================================================