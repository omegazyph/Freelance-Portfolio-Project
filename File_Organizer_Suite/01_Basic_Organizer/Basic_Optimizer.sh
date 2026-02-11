#!/bin/bash

# ==============================================================================
# Date:         2026-01-04
# Script Name:  Basic_Optimizer.sh
# Author:       omegazyph
# Updated:      2026-02-11
# Description:  Entry-level script designed to sort common file types into 
#               primary organizational folders for simplified management.
# ==============================================================================

# Use full words for the directory variable
TARGET_DIRECTORY="$HOME/Downloads"

# 1. Validation and Directory Entry
# Check if the directory exists first
if [ ! -d "$TARGET_DIRECTORY" ]; then
    echo "Error: The folder $TARGET_DIRECTORY was not found."
    exit 1
fi

cd "$TARGET_DIRECTORY" || { echo "Error: Could not access directory."; exit 1; }

# 2. Preparation
# Create the primary category folders
mkdir -p Images Documents Media

echo "Initializing basic sorting in $TARGET_DIRECTORY..."
echo "----------------------------------------------------"

# 3. Primary Sorting Logic
# We use individual commands here for maximum clarity and ease of editing.

# Move Image files
mv *.jpg *.jpeg *.png *.gif Images/ 2>/dev/null

# Move Document files
mv *.pdf *.doc *.docx *.txt Documents/ 2>/dev/null

# Move Media and Archive files
mv *.mp3 *.mp4 *.mov *.zip *.rar Media/ 2>/dev/null

# 4. Finalization
echo "Sorting Complete."
echo "Files have been categorized into: Images, Documents, and Media."
echo "===================================================="