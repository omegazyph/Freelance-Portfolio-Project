#!/bin/bash

# ==============================================================================
# Date:         2026-01-05
# Script Name:  Basic_Optimizer.sh
# Author:       omegazyph
# Updated:      2026-02-16
# Description:  Basic Tier: Essential directory cleanup. No external 
#               configuration required. Optimized for Windows/Git Bash.
# ==============================================================================

# 1. VISUAL THEMING
BLUE='\033[0;34m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# 2. DYNAMIC PATH RESOLUTION
# This handles the space in 'Wayne Stock' by using the Windows USERPROFILE.
if [ -n "$USERPROFILE" ]; then
    TARGET_DIR=$(echo "$USERPROFILE/Downloads" | sed 's/\\/\//g' | sed 's/C:/\/c/')
else
    TARGET_DIR="$HOME/Downloads"
fi

# 3. SYSTEM VALIDATION
if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${BLUE}Error: Target directory not found at $TARGET_DIR${NC}"
    exit 1
fi

# Move into the directory (wrapped in quotes for spaces)
cd "$TARGET_DIR" || { echo "Access denied."; exit 1; }

# 4. UI HEADER
echo -e "${BLUE}==================================================${NC}"
echo -e "${GREEN}${BOLD}      OMEGAZYPH BASIC OPTIMIZER v1.0              ${NC}"
echo -e "${BLUE}==================================================${NC}"
echo -e "${CYAN}📂 Targeting: $TARGET_DIR${NC}"
echo -e "--------------------------------------------------"

# 5. EXECUTION PHASE
# Standard hardcoded categories for the Basic Tier
shopt -s nullglob
shopt -s nocaseglob

# Organize Images
if ls *.jpg *.jpeg *.png *.gif *.svg &>/dev/null; then
    mkdir -p Images
    mv *.jpg *.jpeg *.png *.gif *.svg Images/ 2>/dev/null
    echo -e "  ${GREEN}✔${NC} Categorized Image files."
fi

# Organize Documents
if ls *.pdf *.doc* *.txt *.xls* &>/dev/null; then
    mkdir -p Documents
    mv *.pdf *.doc* *.txt *.xls* Documents/ 2>/dev/null
    echo -e "  ${GREEN}✔${NC} Categorized Document files."
fi

# Organize Videos
if ls *.mp4 *.mov *.avi *.mkv &>/dev/null; then
    mkdir -p Videos
    mv *.mp4 *.mov *.avi *.mkv Videos/ 2>/dev/null
    echo -e "  ${GREEN}✔${NC} Categorized Video files."
fi

# 6. FOOTER
shopt -u nullglob
shopt -u nocaseglob

echo -e "--------------------------------------------------"
echo -e "${GREEN}${BOLD}Basic Optimization Complete.${NC}"
echo -e "${BLUE}==================================================${NC}"