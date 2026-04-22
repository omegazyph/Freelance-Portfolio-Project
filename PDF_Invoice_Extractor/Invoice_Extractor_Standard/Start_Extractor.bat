@echo off
:: ==============================================================================
:: Date:         2026-02-17
:: Script Name:  Start_Extractor.bat
:: Author:       omegazyph
:: Updated:      2026-02-17
:: Description:  Main launcher for the Standard Tier Extractor.
:: ==============================================================================

title Omegazyph Standard Extractor
color 0B

echo.
echo  ############################################################
echo  #         LAUNCHING OMEGAZYPH STANDARD EXTRACTOR           #
echo  ############################################################
echo.

python -u "scripts/Invoice_Extractor_Standard.py"

echo.
echo  ------------------------------------------------------------
echo  [SYSTEM]: Process Complete. Check /Invoices for renamed files.
pause