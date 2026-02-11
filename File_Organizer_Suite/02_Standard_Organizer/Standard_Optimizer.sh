#!/bin/bash

# ==============================================================================
# Date:         2026-01-04
# Script Name:  Standard_Optimizer.sh
# Author:       omegazyph
# Updated:      2026-02-11
# Description:  Advanced directory optimization utility. Categorizes images, 
#               documents, archives, and videos using associative arrays.
# ==============================================================================

# Explicit Windows path for the Lenovo Legion
TARGET_DIRECTORY="/c/Users/omega/Downloads"

# Associative array for modular category management
declare -A CATEGORIES
CATEGORIES=(
    ["Images"]="jpg jpeg png gif svg"
    ["Documents"]="pdf doc docx txt csv xlsx ods"
    ["Archives"]="zip tar gz rar 7z"
    ["Videos"]="mp4 mov avi mkv wmv"
)

# 1. System Validation
if [ ! -d "$TARGET_DIRECTORY" ]; then
    echo "Error: The target directory $TARGET_DIRECTORY is unreachable."
    exit 1
fi

cd "$TARGET_DIRECTORY" || { echo "Fatal Error: Access denied."; exit 1; }

# 2. Shell Environment Configuration
# nullglob: Prevents the script from seeing "*.ext" as a literal string if no files exist
# nocaseglob: Allows the script to find both .mp4 and .MP4
shopt -s nullglob
shopt -s nocaseglob

echo "Initializing System Optimization for $TARGET_DIRECTORY..."
echo "----------------------------------------------------"

# 3. Execution Phase
# 
for FOLDER in "${!CATEGORIES[@]}"; do
    EXTENSIONS=${CATEGORIES[$FOLDER]}
    FILES_FOUND=false
    
    # Check each extension in the category
    for EXT in $EXTENSIONS; do
        for FILE in *."$EXT"; do
            if [ -f "$FILE" ]; then
                # Only create the directory if at least one matching file is found
                if [ "$FILES_FOUND" = false ]; then
                    mkdir -p "$FOLDER"
                    FILES_FOUND=true
                fi
                
                echo "[+] Relocating: $FILE -> $FOLDER/"
                mv "$FILE" "$FOLDER/"
            fi
        done
    done
    
    if [ "$FILES_FOUND" = true ]; then
        echo "[*] Category '$FOLDER' successfully organized."
    fi
done

# Reset shell options to default
shopt -u nullglob
shopt -u nocaseglob

echo "----------------------------------------------------"
echo "Optimization Protocol Complete."
echo "===================================================="