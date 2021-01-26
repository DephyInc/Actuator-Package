#!/bin/bash
# Install dependencies to build the c++ examples
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "Installing Build Dependencies" &&
sudo apt update &&
sudo apt install cmake g++-7 gcc-7 ninja-build -y &&
echo -e "${GREEN}Dependencies successfuly installed.${NC}" ||
echo -e "${RED}Problem encountered installing dependencies.${NC}"
