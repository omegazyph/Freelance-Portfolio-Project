@echo off
:: Date: 2026-02-11
:: Author: omegazyph
:: Description: One-click launcher for the Basic Invoice Extractor

title omegazyph Basic Extractor
echo ------------------------------------------
echo Initializing Basic Extraction Engine...
echo ------------------------------------------
python Scripts/Invoice_Extractor_Basic.py
echo.
echo Check the 'Output' folder for your CSV.
pause
