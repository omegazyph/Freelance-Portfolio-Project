# File Optimizer Pro

**Developer:** omegazyph  
**Build Date:** 2026-02-25  

## 📄 Project Description

File Optimizer Pro is a high-performance desktop utility built for Windows 11. It automates the process of organizing cluttered folders by scanning file extensions and moving them into logically categorized sub-directories (e.g., Documents, Images, Videos, and Code).

## ✨ Features

* **One-Click Optimization:** Instantly sorts hundreds of files.
* **Live Monitor:** A real-time console view showing every file operation as it happens.
* **Self-Contained:** Distributed as a single `.exe` with all assets (logos/icons) embedded.
* **Safety First:** Intelligent renaming prevents overwriting files with the same name.
* **Activity Logging:** Maintains a detailed `file_moves.log` for auditing.

## 📁 Directory Structure

```text
/File_Organizer_Suite/
├── File_Optimizer_Pro.exe  # Standalone Application
├── requirements.txt        # Development dependencies
├── README.md               # Project documentation
├── /config/                # JSON sorting rules
└── /logs/                  # Detailed activity history

🛠️ Technical Stack

    Core: Python 3.12

    Interface: Custom-themed Tkinter (Windows 11 "Mica" aesthetic)

    Imaging: Pillow (PIL) for internal asset rendering

    Packaging: PyInstaller with resource-path embedding

🚀 Usage Instructions

    Run: Open File_Optimizer_Pro.exe.

    Select: Click the "Choose Folder" button to pick your target directory.

    Optimize: Hit "Start Optimization" and watch the Live Monitor.

    Customize: Edit the config.json file in the /config folder to add your own file extensions.
