@echo off
:: Date: 2026-02-11
:: Author: omegazyph
:: Description: Advanced Tier Launcher with Google Sheets Sync

title omegazyph Enterprise Extractor
echo ===========================================
echo Initializing Enterprise Sync Engine...
echo ===========================================

python Scripts/Invoice_Extractor_Advanced.py

echo =========================================================
echo Process Complete. Check your Google Sheet for updates.
echo =========================================================
pause