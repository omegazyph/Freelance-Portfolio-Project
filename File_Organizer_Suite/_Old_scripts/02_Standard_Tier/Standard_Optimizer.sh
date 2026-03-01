#!/bin/bash

# ==============================================================================
# Date:         2026-01-05
# Script Name:  Standard_Optimizer.sh
# Author:       omegazyph
# Updated:      2026-02-16
# Description:  Standard Tier: Advanced directory optimization using 
#               associative arrays and ANSI color reporting. Handles 
#               Windows user paths with spaces automatically.
# ==============================================================================

# 1. VISUAL THEMING (ANSI COLORS)
# These match your Python scripts for a consistent "Suite" feel.
BLUE='\033[0;34m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m' # No Color (Reset)

# 2. DYNAMIC PATH RESOLUTION
# This correctly identifies the 'Wayne Stock' path on your Lenovo Legion.
if [ -n "$USERPROFILE" ]; then
    # Converts C:\Users\Wayne Stock to /c/Users/Wayne Stock
    TARGET_DIR=$(echo "$USERPROFILE/Downloads" | sed 's/\\/\//g' | sed 's/C:/\/c/')
else
    # Fallback for native Linux/Mac environments
    TARGET_DIR="$HOME/Downloads"
fi

# 3. SYSTEM VALIDATION
if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${RED}❌ Error: Target directory not found at: $TARGET_DIR${NC}"
    exit 1
fi

# Move into the directory (wrapped in quotes for spaces)
cd "$TARGET_DIR" || { echo -e "${RED}Fatal Error: Access denied.${NC}"; exit 1; }

# 4. CONFIGURATION (ASSOCIATIVE ARRAY)
declare -A CATEGORIES
CATEGORIES=(
    ["Images"]="jpg jpeg png gif svg"
    ["Documents"]="pdf doc docx txt csv xlsx ods"
    ["Archives"]="zip tar gz rar 7z"
    ["Videos"]="mp4 mov avi mkv wmv"
)

# 5. UI HEADER
echo -e "${BLUE}==================================================${NC}"
echo -e "${GREEN}${BOLD}      OMEGAZYPH STANDARD OPTIMIZER v2.0           ${NC}"
echo -e "${BLUE}==================================================${NC}"
echo -e "${CYAN}📂 Targeting: $TARGET_DIR${NC}\n"

# 6. EXECUTION PHASE
shopt -s nullglob
shopt -s nocaseglob

for FOLDER in "${!CATEGORIES[@]}"; do
    EXTENSIONS=${CATEGORIES[$FOLDER]}
    FILES_FOUND=false
    
    for EXT in $EXTENSIONS; do
        for FILE in *."$EXT"; do
            if [ -f "$FILE" ]; then
                # Ensure the folder exists before moving
                if [ "$FILES_FOUND" = false ]; then
                    mkdir -p "$FOLDER"
                    FILES_FOUND=true
                fi
                
                # Visual feedback matching the Python "Checkmark" style
                echo -e "  ${GREEN}✔${NC} ${FILE} ${CYAN}→ ${FOLDER}/${NC}"
                mv "$FILE" "$FOLDER/"
            fi
        done
    done
done

# 7. FOOTER & CLEANUP
shopt -u nullglob
shopt -u nocaseglob

echo -e "\n${BLUE}--------------------------------------------------${NC}"
echo -e "${GREEN}${BOLD}✅ Optimization Protocol Complete.${NC}"
echo -e "${BLUE}==================================================${NC}"