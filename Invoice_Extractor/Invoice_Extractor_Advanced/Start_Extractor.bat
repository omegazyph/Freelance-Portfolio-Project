@echo off
:: ==============================================================================
:: Date:         2026-02-17
:: Script Name:  Start_Extractor.bat
:: Author:       omegazyph
:: Updated:      2026-02-17
:: Description:  Main root launcher for the Advanced Invoice Extractor.
:: ==============================================================================

title Omegazyph Advanced Extractor
color 0B

echo.
echo  ############################################################
echo  #                                                          #
echo  #         LAUNCHING OMEGAZYPH ADVANCED EXTRACTOR           #
echo  #                                                          #
echo  ############################################################
echo.

:: Launch the core logic from the scripts directory
python -u "scripts/Invoice_Extractor_Advanced.py"

echo.
echo  ------------------------------------------------------------
echo  [SYSTEM]: Session finished. 
pause