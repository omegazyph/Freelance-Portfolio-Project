@echo off
:: ==============================================================================
:: Date:         2026-02-11
:: Script Name:  run_extractor.bat
:: Author:       omegazyph
:: Description:  One-click launcher for the Invoice Extractor Python script.
:: ==============================================================================

title omegazyph Invoice Extractor
echo ============================================================
echo        STARTING INVOICE EXTRACTION PROTOCOL...
echo ============================================================
echo.

:: Run the python script located in the Scripts folder
python Scripts/Invoice_Extractor.py

echo.
echo ============================================================
echo        PROCESS COMPLETE. PRESS ANY KEY TO EXIT.
echo ============================================================
pause >nul