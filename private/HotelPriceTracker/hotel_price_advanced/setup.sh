#!/bin/bash

# Date: 2026-01-05
# Script Name: setup.sh
# Author: omegazyph
# Updated: 2026-02-15
# Description: Automated environment setup with path-awareness.

# ANSI Color Codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# THE FIX: Move into the directory where the script is located
cd "$(dirname "$0")"

echo -e "${YELLOW}Starting omegazyph Project Setup...${NC}"
echo -e "Working directory: $(pwd)"

# Verify Python
if ! command -v python &> /dev/null
then
    echo -e "${RED}Error: Python could not be found.${NC}"
    exit 1
fi

# Check for requirements.txt in the script's folder
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}Error: requirements.txt not found in $(pwd)${NC}"
    exit 1
fi

echo -e "${GREEN}Installing Python libraries...${NC}"

# Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}Setup Complete!${NC}"
    echo -e "Run the tracker: ${YELLOW}python hotel_price_advanced.py${NC}"
else
    echo -e "${RED}Setup failed.${NC}"
fi