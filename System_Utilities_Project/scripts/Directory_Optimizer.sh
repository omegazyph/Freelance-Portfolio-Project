#!/bin/bash

# ==============================================================================
# Date:         2026-01-04
# Script Name:  Directory_Optimizer.sh
# Author:       omegazyph
# Updated:      2026-02-11
# Description:  Automated directory management utility designed to categorize 
#               and organize files by extension into structured sub-directories.
# ==============================================================================

# --- CONFIGURATION ---
TARGET_DIRECTORY="$HOME/Downloads"
VERSION="1.1.0"

# --- UI INITIALIZATION ---
echo -e "\033[0;36m" # Cyan
echo "===================================================="
echo "      DIRECTORY OPTIMIZER $VERSION - ACTIVE         "
echo "===================================================="
echo -e "\033[0m" # Reset

# 1. Directory Validation
if [ -d "$TARGET_DIRECTORY" ]; then
    cd "$TARGET_DIRECTORY" || { echo "Fatal Error: Cannot access $TARGET_DIRECTORY"; exit 1; }
else
    echo "Initialization Error: Target directory not found at $TARGET_DIRECTORY"
    exit 1
fi

# 2. File Mapping Definition
# This demonstrates professional modularity for Upwork clients
declare -A CATEGORIES
CATEGORIES=(
    ["Images"]="*.jpg *.jpeg *.png *.gif *.svg"
    ["Documents"]="*.pdf *.doc *.docx *.txt *.pages *.csv *.xlsx"
    ["Audio"]="*.mp3 *.wav *.m4a *.flac"
    ["Video"]="*.mp4 *.mov *.avi *.mkv"
    ["Archives"]="*.zip *.tar *.gz *.rar *.7z"
)

# 3. Execution Phase
echo "Executing synchronization and sorting protocols..."
echo "----------------------------------------------------"

for FOLDER in "${!CATEGORIES[@]}"; do
    EXTENSIONS=${CATEGORIES[$FOLDER]}
    
    # Check if any files matching these extensions actually exist
    # This prevents 'No such file' errors from showing in the console
    if ls $EXTENSIONS >/dev/null 2>&1; then
        echo "[*] Categorizing $FOLDER..."
        mkdir -p "$FOLDER"
        mv -v $EXTENSIONS "$FOLDER/" 2>/dev/null
    fi
done

# 4. Finalization
echo "----------------------------------------------------"
echo -e "\033[0;32mSUCCESS: System optimization completed.\033[0m"
echo "===================================================="