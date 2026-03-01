@echo off
:: ==============================================================================
:: Date:         2026-01-05
:: Script Name:  run_standard.bat
:: Author:       omegazyph
:: Updated:      2026-02-16
:: Description:  Smart launcher for Standard Tier. Handles Windows usernames 
::               with spaces and selects between Python or Bash environments.
:: ==============================================================================

:: Set ANSI Color Codes
set "ESC="
set "BLUE=%ESC%[94m"
set "GREEN=%ESC%[92m"
set "CYAN=%ESC%[96m"
set "RED=%ESC%[91m"
set "RESET=%ESC%[0m"

title Standard Optimizer Suite Launcher

echo %BLUE%====================================================%RESET%
echo %GREEN%        OMEGAZYPH STANDARD OPTIMIZER SUITE        %RESET%
echo %BLUE%====================================================%RESET%
echo.
echo 1. Run Python Version (Native Windows - Recommended)
echo 2. Run Bash Version (Requires Git Bash)
echo.

set /p choice="Select your environment (1-2): "

if "%choice%"=="1" goto RUN_PY
if "%choice%"=="2" goto RUN_SH
goto INVALID

:RUN_PY
echo.
echo %CYAN%[+] Launching Python Suite...%RESET%
:: Use double quotes to handle potential spaces in the file path
python "Standard_Optimizer.py"
goto END

:RUN_SH
echo.
echo %CYAN%[+] Locating Git Bash...%RESET%
:: Checking common installation paths 
if exist "C:\Program Files\Git\bin\sh.exe" (
    set SH_PATH="C:\Program Files\Git\bin\sh.exe"
) else if exist "C:\Program Files\Git\usr\bin\sh.exe" (
    set SH_PATH="C:\Program Files\Git\usr\bin\sh.exe"
) else (
    echo.
    echo %RED%[!] ERROR: Git Bash not found in standard locations.%RESET%
    echo Please ensure Git for Windows is installed.
    pause
    exit
)

echo %CYAN%[+] Executing: Standard_Optimizer.sh...%RESET%
:: Execute the script using the discovered path with double quotes 
%SH_PATH% "./Standard_Optimizer.sh"
goto END

:INVALID
echo %RED%Invalid selection. Please run the launcher again.%RESET%
pause
exit

:END
echo.
echo %BLUE%====================================================%RESET%
echo %GREEN%Process Finished.%RESET%
echo %BLUE%====================================================%RESET%
pause