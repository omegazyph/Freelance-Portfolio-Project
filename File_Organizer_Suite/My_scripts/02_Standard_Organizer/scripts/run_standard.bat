@echo off
:: ==============================================================================
:: Date:         2026-01-04
:: Script Name:  run_standard.bat
:: Author:       omegazyph
:: Updated:      2026-02-11
:: Description:  Smart launcher that locates Git Bash automatically to 
::               execute the Standard_Optimizer.sh script.
:: ==============================================================================

title Standard Optimizer Launcher

echo ====================================================
echo Checking for Git Bash environment...
echo ====================================================

:: 1. Check common installation paths
if exist "C:\Program Files\Git\bin\sh.exe" (
    set SH_PATH="C:\Program Files\Git\bin\sh.exe"
) else if exist "C:\Program Files\Git\usr\bin\sh.exe" (
    set SH_PATH="C:\Program Files\Git\usr\bin\sh.exe"
) else (
    echo.
    echo [!] ERROR: Git Bash was not found in standard locations.
    echo Please ensure Git for Windows is installed.
    pause
    exit
)

echo [+] Found Git Bash at: %SH_PATH%
echo [+] Running Standard_Optimizer.sh...
echo.

:: 2. Execute the script using the discovered path
%SH_PATH% ./scripts/Standard_Optimizer.sh

echo.
echo ====================================================
echo Process Finished.
echo ====================================================
pause