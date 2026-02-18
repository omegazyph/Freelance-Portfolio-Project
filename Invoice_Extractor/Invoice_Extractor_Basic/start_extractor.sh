#!/bin/bash
# ==============================================================================
# Date:         2026-02-17
# Script Name:  start_extractor.sh
# Author:       omegazyph
# Updated:      2026-02-17
# Description:  Main root launcher for Bash/Linux (Basic Tier).
# ==============================================================================

CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}############################################${NC}"
echo -e "${CYAN}#       OMEGAZYPH BASIC EXTRACTOR (BASH)   #${NC}"
echo -e "${CYAN}############################################${NC}"
echo ""

# Run the core logic from the scripts folder
python3 -u "scripts/Invoice_Extractor_Basic.py"

echo ""
echo -e "${CYAN}--------------------------------------------${NC}"
echo "Process Complete. Check /results for your CSV."
read -n 1 -s -r -p "Press any key to close..."
echo ""