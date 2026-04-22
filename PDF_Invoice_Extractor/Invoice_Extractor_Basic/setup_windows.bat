@echo off
title omegazyph Basic Setup
color 0B
echo  [SYSTEM]: Installing dependencies from /config...
pip install -r config/requirements.txt
if not exist "Invoices" mkdir Invoices
if not exist "results" mkdir results
echo  [SUCCESS]: Environment Ready.
pause