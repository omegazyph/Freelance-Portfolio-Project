#!/bin/bash
# Date:           2026-01-05
# Script Name:    setup.sh
# Author:         omegazyph
# Updated:        2026-02-16
# Description:    Environment initializer with Cross-Platform Python detection.

# Get the directory where the script is located
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Set colors for Bash output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}==================================================${NC}"
echo -e "${GREEN}    OMEGAZYPH SUITE: INITIALIZING ENVIRONMENT     ${NC}"
echo -e "${BLUE}==================================================${NC}"

# 1. Create directory structure
echo -e "Creating project folders..."
mkdir -p "$BASE_DIR/logs" "$BASE_DIR/config"
echo -e "${GREEN}✔ Folders verified.${NC}"

# 2. Smart Python Detection (Checks for python3 then python)
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo -e "${GREEN}✔ Python 3 detected.${NC}"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo -e "${GREEN}✔ Python detected (Windows environment).${NC}"
else
    echo -e "${RED}❌ Python not found. Please install Python to continue.${NC}"
fi

# 3. Verify Requirements File
if [ -f "$BASE_DIR/requirements.txt" ]; then
    echo -e "${GREEN}✔ requirements.txt found.${NC}"
else
    echo -e "⚠️  requirements.txt not detected. Creating default..."
    cat <<EOT > "$BASE_DIR/requirements.txt"
# OMEGAZYPH File Optimizer Requirements
os
shutil
logging
json
EOT
fi

# 4. Set permissions
chmod +x "$BASE_DIR"/*.sh
echo -e "${GREEN}✔ Permissions updated.${NC}"

echo -e "\n${BLUE}Setup complete.${NC}"

# 5. AUTO-RUN PROMPT (Using detected PYTHON_CMD)
if [ -n "$PYTHON_CMD" ]; then
    echo -e "${YELLOW}Would you like to run the OMEGAZYPH Optimizer now? (y/n)${NC}"
    read -r choice

    if [[ "$choice" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo -e "${GREEN}🚀 Launching Advanced_Optimizer.py using $PYTHON_CMD...${NC}\n"
        $PYTHON_CMD "$BASE_DIR/Advanced_Optimizer.py"
    else
        echo -e "Process finished. Run later with: $PYTHON_CMD Advanced_Optimizer.py"
    fi
else
    echo -e "${RED}Manual intervention required: Install Python to run the script.${NC}"
fi