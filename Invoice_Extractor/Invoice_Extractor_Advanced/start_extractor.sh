#!/bin/bash
# ==============================================================================
# Date:         2026-02-17
# Script Name:  start_extractor.sh
# Author:       omegazyph
# Updated:      2026-02-17
# Description:  Main root launcher for Bash/Linux users.
# ==============================================================================

CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}--- Launching Omegazyph Advanced Extractor ---${NC}"
echo ""

# Run the python script from the scripts folder
python3 -u "scripts/Invoice_Extractor_Advanced.py"
echo "${CYAN}starting the program.${NC}"

echo ""
echo -e "${CYAN}---------------------------------------------${NC}"
read -n 1 -s -r -p "Press any key to close..."
echo ""