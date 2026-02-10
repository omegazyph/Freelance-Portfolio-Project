# Log Monitor Pro

## Project Description

This project is a comprehensive automation tool designed to bridge the gap between system administration and data analysis. It utilizes a Bash script to manage the environment and file system operations, which then triggers a Python engine to perform deep text parsing and report generation. This structure ensures that the system is both efficient at the OS level and powerful at the data processing level.

## Author Information

* **Author:** omegazyph
* **Date Created:** 2026-02-10
* **Last Updated:** 2026-02-10

## File Structure

The project is organized into a specific directory hierarchy to maintain cleanliness and scalability:

* **LogMonitorPro/**: The main project root directory.

  * **scripts/**: Contains the executable Bash and Python files.
  * **logs/**: The destination for raw system log files to be analyzed.
  * **reports/**: The output directory where the final analysis summaries are generated.

## Technical Requirements

To run this project, the following environment is recommended:

1. **Operating System:** Windows 11 (utilizing Windows Subsystem for Linux) or a native Linux distribution.
2. **Code Editor:** Visual Studio Code.
3. **Language Versions:** Python version 3.x and Bash version 4.0 or higher.

## How To Use

1. Place your raw log files into the **logs** directory and ensure the file is named **system_activity.log**.
2. Navigate to the project root directory in your terminal.
3. Execute the Bash script by typing: `bash scripts/monitor_logs.sh`.
4. Once the process is finished, view the generated summary in the **reports** directory.

## Implementation Details

The Bash script acts as the "Collector" by verifying that all necessary directories and files exist before execution. The Python script acts as the "Analyzer" by reading the log data, identifying critical errors, and formatting that data into a human-readable text report.
