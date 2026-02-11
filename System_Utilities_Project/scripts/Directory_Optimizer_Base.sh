#!/bin/bash

# ==============================================================================
# Date:         2026-01-04
# Script Name:  Directory_Optimizer_Base.sh
# Author:       omegazyph
# Updated:      2026-02-11
# Description:  Base template for automated file organization. Categorizes 
#               files into sub-directories based on user-defined mappings.
# ==============================================================================

# --- CONFIGURATION ---
# Default target is Downloads; can be overridden per client request
TARGET_DIR="$HOME/Downloads"
LOG_FILE="organization_log_$(date +%Y%m%d).txt"

# --- UI COLORS ---
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}Starting Directory Optimizer Base Utility...${NC}"

# 1. VALIDATION PHASE
if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${RED}Error: Target directory $TARGET_DIR does not exist.${NC}"
    exit 1
fi

cd "$TARGET_DIR" || exit 1

# 2. MODULAR CATEGORY MAPPING
# Clients often ask for specific folders; edit this array to customize
declare -A CATEGORIES
CATEGORIES=(
    ["Documents"]="*.pdf *.doc* *.txt *.csv *.xlsx"
    ["Images"]="*.jpg *.jpeg *.png *.gif *.svg"
    ["Audio"]="*.mp3 *.wav *.m4a *.flac"
    ["Video"]="*.mp4 *.mov *.avi *.mkv"
    ["Archives"]="*.zip *.tar *.gz *.rar *.7z"
    ["Executables"]="*.exe *.msi *.sh *.deb"
)

# 3. PROCESSING PHASE
echo "Organizing files in: $(pwd)"
echo "----------------------------------------------------"

for FOLDER in "${!CATEGORIES[@]}"; do
    EXTENSIONS=${CATEGORIES[$FOLDER]}
    
    # Check if files exist for these extensions to avoid shell errors
    if ls $EXTENSIONS >/dev/null 2>&1; then
        echo -e "[*] Moving files to ${GREEN}$FOLDER${NC}..."
        
        # Create folder if it doesn't exist
        mkdir -p "$FOLDER"
        
        # Move files and log the action
        mv -v $EXTENSIONS "$FOLDER/" >> "$LOG_FILE" 2>&1
    fi
done

# 4. FINALIZATION
echo "----------------------------------------------------"
echo -e "${GREEN}SUCCESS: Organization protocol complete.${NC}"
echo "Log file generated: $LOG_FILE"