@echo off
:: ==============================================================================
:: Date:         2026-02-17
:: Script Name:  clean_project.bat
:: Author:       omegazyph
:: Updated:      2026-02-17
:: Description:  Professional cleanup utility for the Basic Tier. 
::               Removes Python cache and old extracted CSV data.
:: ==============================================================================

title omegazyph Project Cleaner - Basic
color 0C

echo.
echo  ############################################################
echo  #         omegazyph PROJECT CLEANUP (BASIC)                #
echo  ############################################################
echo.
echo  [SYSTEM]: Preparing folder for client delivery...

:: 1. Remove Python cache folders
if exist "__pycache__" (
    rmdir /s /q "__pycache__"
    echo  [CLEAN]: Removed scripts/__pycache__
)

:: 2. Remove the Basic Tier output file to ensure a fresh start
if exist "..\results\Extracted_Data.csv" (
    del /f /q "..\results\Extracted_Data.csv"
    echo  [CLEAN]: Removed old Extracted_Data.csv from /results
)

echo.
echo  ------------------------------------------------------------
echo  [SUCCESS]: Basic Project folder is now clean and ready!
echo  ------------------------------------------------------------
echo.
pause