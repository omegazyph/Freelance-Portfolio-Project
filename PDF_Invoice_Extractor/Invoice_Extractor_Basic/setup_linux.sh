#!/bin/bash
# ==============================================================================
# Date:         2026-02-17
# Script Name:  setup_linux.sh
# Author:       omegazyph
# Updated:      2026-02-17
# Description:  Professional setup for Linux/Parrot (Basic Tier).
#               Installs core PDF and Data Processing libraries.
# ==============================================================================

CYAN='\033[0;36m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${CYAN}--- omegazyph Basic Setup (BASH) ---${NC}"

# 1. Install dependencies from the config folder
echo -e "[${CYAN}SYSTEM${NC}]: Installing dependencies from /config..."
python3 -m pip install --upgrade pip > /dev/null 2>&1
pip3 install -r config/requirements.txt > /dev/null 2>&1
echo -e "[${GREEN}SUCCESS${NC}]: pdfplumber and pandas installed."

# 2. Directory Verification
mkdir -p Invoices results
echo -e "[${GREEN}SUCCESS${NC}]: Project directories are ready."

echo ""
read -p "Would you like to run the Basic Extractor now? (y/n): " choice

case "$choice" in 
  y|Y ) 
    python3 -u "scripts/Invoice_Extractor_Basic.py"
    ;;
  * ) 
    echo "Setup finished. Use ./start_extractor.sh to run."
    ;;
esac

echo ""
read -n 1 -s -r -p "Press any key to close..."
echo ""