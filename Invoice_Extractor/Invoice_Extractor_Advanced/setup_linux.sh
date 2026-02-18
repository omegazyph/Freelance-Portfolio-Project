#!/bin/bash
# ==============================================================================
# Date:         2026-02-17
# Script Name:  setup_linux.sh
# Author:       omegazyph
# Updated:      2026-02-17
# Description:  Professional setup for Linux/Parrot. 
#               Points to /config for dependencies.
# ==============================================================================

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}--- omegazyph Enterprise Setup (BASH) ---${NC}"

# Install dependencies from config folder
echo -e "[${CYAN}SYSTEM${NC}]: Installing dependencies from /config..."
python3 -m pip install --upgrade pip > /dev/null 2>&1
pip3 install -r config/requirements.txt > /dev/null 2>&1
echo -e "[${GREEN}SUCCESS${NC}]: Dependencies installed."

# Check for JSON in config folder
if [ -f "config/credentials.json" ]; then
    echo -e "[${GREEN}SYSTEM${NC}]: credentials.json found in /config."
else
    echo -e "[${YELLOW}WARNING${NC}]: credentials.json missing in /config."
fi

echo ""
read -p "Would you like to run the Invoice Extractor now? (y/n): " choice

case "$choice" in 
  y|Y ) 
    python3 -u "scripts/Invoice_Extractor_Advanced.py"
    ;;
  * ) 
    echo "Setup finished."
    ;;
esac

echo ""
read -n 1 -s -r -p "Press any key to close..."
echo ""