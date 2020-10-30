#!/bin/bash
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color
BASE_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
REQS_PATH="${BASE_PATH}/Python/requirements.txt"

# Ubuntu Dependencies
if [[ "$OSTYPE" == "linux-gnu" ]]; then
	sudo apt update &&
	sudo apt install software-properties-common -y &&
	sudo add-apt-repository ppa:deadsnakes/ppa &&
	sudo apt install python3.7 -y &&
	echo -e "${GREEN}Python dependencies installed.${NC}" &&
	python3.7 -m pip install -U -r ${REQS_PATH} &&
	echo -e "${GREEN}Python libraries installed${NC}" && exit 0 ||
	echo -e "${RED}An issue was encountered when installing the python dependencies.${NC}" &&
	exit 1
# Raspberry Pi Dependencies
elif [[ "$OSTYPE" == "linux-gnueabihf" ]]; then
	sudo apt update &&
	sudo apt install ufw python-scipy libatlas-base-dev -y &&
	sudo ufw enable && sudo ufw allow 8988 && sudo ufw allow 22 && # Open port for graph display
	echo -e "${GREEN}Python dependencies installed.${NC}" &&
	python3 -m pip install -U -r ${REQS_PATH} &&
	echo -e "${GREEN}Python libraries installed${NC}" && exit 0 ||
	echo -e "${RED}An issue was encountered when installing the python dependencies.${NC}" &&
	exit 1
else
	echo -e "${RED}Unsuported OS $OSTYPE. Nothing was installed.${NC}" &&
	exit 1
fi
