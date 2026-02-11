# Directory Optimizer v1.1.0

    **Automated File Management & Organization Utility**

## 🚀 Overview

Directory Optimizer is a professional-grade Bash utility designed to transform cluttered folders into structured environments. Developed for both performance and readability, it automatically categorizes files into logical sub-directories based on their extensions.

**Author:** omegazyph  
**Updated:** 2026-02-11  
**Environment:** Linux / WSL (Windows Subsystem for Linux) / macOS

---

## ✨ Features

- **Smart Categorization:** Automatically handles Images, Documents, Audio, Video, and Archives.
- **Silent Validation:** Only creates folders and executes moves when relevant files exist, keeping your console clean.
- **Safety First:** Includes directory validation to prevent execution in incorrect paths.
- **Visual Feedback:** Uses ANSI color-coded output for clear status reporting.

---

## 🛠️ Installation & Usage

### 1. Set Permissions

Before running for the first time, ensure the script is executable:

bash
chmod +x Directory_Optimizer.sh

2.Configure Target (Optional)

By default, the script targets your ~/Downloads folder. To change this, edit the TARGET_DIRECTORY variable in the script:
Bash

TARGET_DIRECTORY="/your/custom/path"

3.Run the Script
Bash

./Directory_Optimizer.sh

## 📂 Mapping Protocols

The system is pre-configured with the following logic:

    Documents: .pdf, .docx, .txt, .csv, .xlsx, etc.

    Images: .jpg, .png, .svg, .gif, etc.

    Archives: .zip, .tar.gz, .rar, etc.

## 📝 Customization

Need a custom category for CAD files, code projects, or specific logs? This script is designed to be modular. Simply add a new line to the CATEGORIES associative array in Section 2 of the code.
