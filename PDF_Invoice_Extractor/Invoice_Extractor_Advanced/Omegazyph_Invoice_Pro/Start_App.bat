@echo off
title Omegazyph Invoice Pro Launcher
color 0A
echo [SYSTEM]: Checking dependencies...
pip install customtkinter pdfplumber pandas gspread google-auth >nul 2>&1
echo [SYSTEM]: Launching GUI Dashboard...
python Invoice_Extractor_GUI_Advanced.py
pause