# Legion System Backup Utility (LaCie Z:)

**Author:** omegazyph  
**Date:** January 07, 2026  
**Updated:** February 10, 2026

## Description

This Python-based utility is designed for high-integrity data synchronization between the Lenovo Legion workstation and the LaCie external storage unit (Z:). The program utilizes an incremental synchronization engine to ensure data redundancy while minimizing unnecessary write operations. It features a specialized console output for real-time monitoring of file transfers.

## Core Functionality

* **Dictionary-Driven Architecture:** Managed via a centralized mapping system for multi-directory support.
* **Incremental Processing:** Utilizes file metadata comparison to identify and transfer only modified or new data.
* **Streamlined Console UI:** Implements a character-sequenced output for clear, readable execution logs during active sessions.
* **Repository Optimization:** Automatically excludes version control directories (e.g., `.git`) to maintain backup efficiency.

## Configuration & Scaling

To extend the backup scope, include the directory pairs within the `backup_tasks` dictionary located in the script:

```python
backup_tasks = {
    r"C:\Users\Source_Folder": r"Z:\Backups\Target_Folder",
}
