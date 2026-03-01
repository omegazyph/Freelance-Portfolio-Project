# 📂 OMEGAZYPH Standard File Optimizer

**Date:** 2026-01-05  
**Author:** omegazyph  
**Updated:** 2026-02-16  

## 📝 Description

The **Standard Tier** of the omegazyph suite provides a professional, customizable directory optimization solution. Unlike the Basic tier, this version supports external configuration and is built to run natively on both Windows (Python) and Linux/Mac (Bash) environments.

This tool is specifically optimized for high-performance laptops like the **Lenovo Legion** and handles complex Windows file paths (including those with spaces) with ease.

---

## ✨ Features

* **Dual-Language Support:** Includes both `.py` and `.sh` versions.
* **Customizable Categories:** Modify `config/config.json` to define your own file groupings.
* **Space-Safe:** Full support for Windows usernames with spaces (e.g., "Wayne Stock").
* **Zero Dependencies:** Uses Python Standard Libraries—no external installs required.
* **Visual Feedback:** Clean, color-coded terminal interface for progress tracking.

---

## 🚀 How to Use

### 1. Windows (Recommended)

Simply double-click **`run_standard.bat`**.

* Select **Option 1** to run the Python version (requires Python 3 installed).
* Select **Option 2** to run the Bash version (requires Git Bash).

### 2. Manual Execution

* **Python:** `python Standard_Optimizer.py`
* **Bash:** `bash Standard_Optimizer.sh`

---

## ⚙️ Configuration

Upon first run, a `config/` folder will be created. You can edit `config/config.json` to add or remove file extensions from the sorting categories:

json
{
    "Images": [".jpg", ".png", ".svg"],
    "Documents": [".pdf", ".docx", ".txt"]
}

## 📂 File Structure

Plaintext

02_Standard_Tier/
├── Standard_Optimizer.py
├── Standard_Optimizer.sh
├── run_standard.bat
├── requirements.txt
└── config/
    └── config.json

Developed by omegazyph — Efficiency through Automation.
