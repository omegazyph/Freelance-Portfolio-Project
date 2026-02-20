@echo off
:: Date: 2026-02-20
:: Script Name: run_omegamove.bat
:: Author: omegazyph
:: Description: Launcher for the OmegaMove Pro Python service.
::              Ensures the terminal stays open if the script crashes.

title OMEGAMOVE PRO - ACTIVE WATCHER

:: Change directory to where the script is located
cd /d "%~dp0"

echo ======================================================
echo    STARTING OMEGAMOVE PRO SERVICE...
echo ======================================================

:: Run the python script
:: We use 'python' assuming it's in your Windows PATH
python OmegaMove.py

:: If the script stops, this prevents the window from vanishing
echo.
echo [!] Service stopped or crashed.
pause