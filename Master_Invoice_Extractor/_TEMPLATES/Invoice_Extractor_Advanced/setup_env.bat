@echo off
:: Date:         2026-02-11
:: Script Name:  setup_env.bat
:: Author:       omegazyph
:: Description:  Automated Virtual Environment setup for Python projects.

echo ==========================================
echo    omegazyph Environment Setup
echo ==========================================

:: 1. Create the Virtual Environment
echo [*] Creating Virtual Environment (venv)...
python -m venv venv

:: 2. Activate the Environment and Install Requirements
echo [*] Installing dependencies from requirements.txt...
call venv\Scripts\activate
pip install -r requirements.txt

echo.
echo [SUCCESS] Environment is ready!
echo You can now run the tool using your launcher.
echo ==========================================
pause