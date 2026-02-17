@echo off
:: Date:           2026-01-05
:: Script Name:    setup_windows.bat
:: Author:         omegazyph
:: Updated:        2026-02-16
:: Description:    Windows Environment Initializer with ANSI Color UI.

:: Setup ANSI Color Codes for Windows 10/11
set "ESC="
set "BLUE=%ESC%[94m"
set "GREEN=%ESC%[92m"
set "YELLOW=%ESC%[93m"
set "CYAN=%ESC%[96m"
set "RED=%ESC%[91m"
set "BOLD=%ESC%[1m"
set "RESET=%ESC%[0m"

title OMEGAZYPH SUITE: INITIALIZING ENVIRONMENT

echo %BLUE%==================================================%RESET%
echo %GREEN%%BOLD%    OMEGAZYPH SUITE: INITIALIZING ENVIRONMENT     %RESET%
echo %BLUE%==================================================%RESET%

:: 1. Create directory structure
echo %CYAN%Creating project folders...%RESET%
if not exist "logs" mkdir logs
if not exist "config" mkdir config
echo %GREEN%[OK] Folders verified.%RESET%

:: 2. Smart Python Detection
echo %CYAN%Checking Python installation...%RESET%
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%[ERROR] Python not found. Please install Python from python.org.%RESET%
    pause
    exit /b
)
echo %GREEN%[OK] Python detected.%RESET%

:: 3. Verify Requirements File
if exist "requirements.txt" (
    echo %GREEN%[OK] requirements.txt.%RESET%
) else (
    echo %YELLOW%[WARN] requirements.txt missing. Creating default...%RESET%
    echo # OMEGAZYPH File Optimizer Requirements > requirements.txt
    echo os >> requirements.txt
    echo shutil >> requirements.txt
    echo logging >> requirements.txt
    echo json >> requirements.txt
)

echo.
echo %GREEN%%BOLD%Setup complete.%RESET%
echo %BLUE%==================================================%RESET%

:: 4. Auto-Run Prompt
echo %YELLOW%Would you like to run the OMEGAZYPH Optimizer now? (y/n): %RESET%
set /p choice=

if /i "%choice%"=="y" (
    echo.
    echo %GREEN% Launching Advanced_Optimizer.py...%RESET%
    python Advanced_Optimizer.py
) else (
    echo.
    echo %CYAN%Process finished. You can run the program later with: python Advanced_Optimizer.py%RESET%
)

pause