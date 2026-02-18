@echo off
:: ==============================================================================
:: Date:         2026-02-17
:: Script Name:  clean_project.bat
:: Author:       omegazyph
:: Updated:      2026-02-17
:: Description:  Professional cleanup utility to remove cache and temp files.
:: ==============================================================================

title omegazyph Project Cleaner
color 0C

echo.
echo  ############################################################
echo  #         omegazyph PROJECT CLEANUP UTILITY                #
echo  ############################################################
echo.
echo  [SYSTEM]: Removing temporary files and local data...

:: Remove Python cache folders
if exist "..\scripts\__pycache__" (
    rmdir /s /q "..\scripts\__pycache__"
    echo  [CLEAN]: Removed scripts/__pycache__
)

:: Remove old CSV results to ensure a fresh start for the client
if exist "..\results\Standard_Report.csv" (
    del /f /q "..\results\Standard_Report.csv"
    echo  [CLEAN]: Removed old Standard_Report.csv
)

echo.
echo  ------------------------------------------------------------
echo  [SUCCESS]: Project folder is now clean and ready for export!
echo  ------------------------------------------------------------
echo.
pause