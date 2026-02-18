@echo off
:: ==============================================================================
:: Date:         2026-02-17
:: Script Name:  setup_windows.bat
:: Author:       omegazyph
:: Updated:      2026-02-17
:: Description:  Professional setup for Windows 11. 
::               Points to /config for dependencies.
:: ==============================================================================

title omegazyph Setup - Windows
color 0B

echo.
echo  ############################################################
echo  #         omegazyph ENTERPRISE SETUP PROTOCOL              #
echo  ############################################################
echo.

:: 1. Install Libraries from the config folder
echo  [SYSTEM]: Installing Python dependencies from /config...
python -m pip install --upgrade pip >nul 2>&1
pip install -r config/requirements.txt >nul 2>&1
echo  [SUCCESS]: Libraries installed.

:: 2. Check Credentials inside the config folder
echo.
if exist "config\credentials.json" (
    echo  [SYSTEM]: credentials.json detected in /config.
) else (
    echo  [WARNING]: credentials.json NOT found in /config folder.
    if exist "config\credentials_example.json" (
        echo            Template 'credentials_example.json' is available.
    )
)

echo.
echo  ------------------------------------------------------------
set /p choice="Would you like to run the Invoice Extractor now? (Y/N): "

if /i "%choice%"=="Y" (
    echo.
    echo  [SYSTEM]: Launching...
    python -u "scripts/Invoice_Extractor_Advanced.py"
    pause
) else (
    echo.
    echo  [SYSTEM]: Setup finished.
    pause
)