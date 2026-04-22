@echo off
:: ==============================================================================
:: Date:         2026-02-17
:: Script Name:  setup_windows.bat
:: Author:       omegazyph
:: Updated:      2026-02-17
:: Description:  Professional setup for Windows 11 (Standard Tier).
::               Updated to find requirements in the /config folder.
:: ==============================================================================

title omegazyph Standard Setup - Windows
color 0B

echo.
echo  ############################################################
echo  #         omegazyph STANDARD SETUP PROTOCOL                #
echo  ############################################################
echo.

:: 1. Install Libraries from the NEW config folder path
echo  [SYSTEM]: Installing Python dependencies from /config...
python -m pip install --upgrade pip >nul 2>&1
:: FIXED PATH BELOW
pip install -r config/requirements.txt >nul 2>&1
echo  [SUCCESS]: pdfplumber and pandas installed.

:: 2. Directory Verification
echo.
echo  [SYSTEM]: Verifying folder structure...
if not exist "Invoices" mkdir Invoices
if not exist "results" mkdir results
echo  [SUCCESS]: Project directories are ready.

echo.
echo  ------------------------------------------------------------
set /p choice="Would you like to run the Standard Extractor now? (Y/N): "

if /i "%choice%"=="Y" (
    echo.
    echo  [SYSTEM]: Launching Engine...
    python -u "scripts/Invoice_Extractor_Standard.py"
    pause
) else (
    echo.
    echo  [SYSTEM]: Setup finished. Use Start_Extractor.bat next time.
    pause
)