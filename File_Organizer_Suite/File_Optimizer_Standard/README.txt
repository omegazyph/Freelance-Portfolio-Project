===========================================================
PROJECT NAME: File Optimizer Standard (CLI Edition)
AUTHOR:       omegazyph
DATE:         2026-03-01
UPDATED:      2026-03-01
DESCRIPTION:  Professional file organization utility for 
              Windows 11 using automated extension mapping.
===========================================================

### 1. OVERVIEW
The File Optimizer Standard is a standalone utility designed to 
automatically categorize and move files into organized subfolders 
based on their file extensions (e.g., .pdf, .jpg, .docx).

### 2. INSTALLATION & SETUP
- This tool is delivered as a standalone executable (.exe). 
- No Python installation is required to run the program.
- Simply place the 'File_Optimizer_Standard.exe' in the folder 
  you wish to organize.

### 3. HOW TO USE
1. Double-click 'File_Optimizer_Standard.exe'.
2. The program will scan all files in its current directory.
3. Files will be moved into folders (Documents, Images, etc.).
4. A log file ('optimizer_log.txt') will be created to track 
   all file movements for your records.

### 4. CUSTOMIZING YOUR FOLDERS (config.json)
On the first run, the program creates a 'config.json' file. 
You can open this file with Notepad to customize your setup:

Example Configuration:
{
    "Work_Projects": [".dwg", ".psd"],
    "Financials": [".csv", ".xlsx"]
}

- Change the name in quotes (left side) to change the Folder Name.
- Add extensions in quotes (right side) to include new file types.
- Save the file and run the .exe again to apply changes.

### 5. DATA SAFETY
- This tool uses "Move" logic. It will NOT overwrite files.
- If an error occurs, the details will be recorded in 'optimizer_log.txt'.
- It is recommended to run a test on a small folder first.

### 6. SUPPORT
For custom extensions or feature requests, please contact 
omegazyph via your Upwork project dashboard.
===========================================================