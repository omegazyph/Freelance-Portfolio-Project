# Log Monitoring System

## Project Description

The Log Monitoring System is an automated utility designed to manage, analyze, and maintain system log files. This project demonstrates an intermediate level of integration between Bash shell scripting and the Python programming language. The system provides an interactive environment for the user to validate log data, identify critical errors, and perform automated maintenance on generated reports.

## Author Information

* **Author:** omegazyph
* **Date Created:** 2026-02-10
* **Last Updated:** 2026-02-10

## Project Directory Structure

The system is organized into a modular folder structure to ensure that the code and the data remain separate and manageable:

* **LogMonitorPro/**: The main project root directory.
  * **scripts/**: Contains the execution logic, including `monitor_logs.sh` and `analyze_data.py`.
  * **logs/**: The storage location for input data files such as `system_activity.log`.
  * **reports/**: The destination for all generated analysis summaries.

## Core Features

1. **Environment Validation**: The system automatically checks for the existence of required directories and files before execution begins.
2. **Interactive Maintenance**: The Bash script prompts the user to decide if old reports should be deleted based on a thirty-day retention policy.
3. **Path Resolution**: The Python engine utilizes absolute path resolution to ensure it can locate folders regardless of the current working directory.
4. **Detailed Reporting**: Every analysis creates a unique, date-stamped text file that summarizes error counts and specific critical events.

## Technical Requirements

* **Operating System**: Windows 11 Home (utilizing the Windows Subsystem for Linux).
* **Hardware**: Lenovo Legion Laptop.
* **Development Tool**: Visual Studio Code.
* **Languages**: Python (recognized as `python` in the environment) and Bash.

## Instructions For Execution

1. Navigate to the **LogMonitorPro** directory in your terminal.
2. Place your log data into the `logs/system_activity.log` file.
3. Execute the controller script by typing: `bash scripts/monitor_logs.sh`.
4. Follow the interactive prompt to choose whether you wish to perform a cleanup of old reports.
5. Review the final results located in the **reports** folder.

## Functional Workflow

The workflow begins with the Bash script, which captures the user preference for file cleanup. Once the environment is verified, the Bash script executes the Python processor. The Python script "steps out" of the scripts folder to locate the log file, parses the text for the word "ERROR," and generates a human-readable report.
