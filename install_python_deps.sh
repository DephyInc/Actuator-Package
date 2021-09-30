#!/usr/bin/env bash

# Bash output colors for echo
RED="\033[0;31m"
GREEN="\033[0;32m"
NC="\033[0m" # Default Color

function add_user_to_dialout() {
	echo "Adding $USER to dialout" &&
	sudo usermod -a -G dialout "$USER"
}

# Ubuntu Dependencies
if [[ "$OSTYPE" == "linux-gnu" ]]; then
	sudo apt-get update &&
	sudo apt-get install python3.9 -y &&
	add_user_to_dialout &&
	echo -e "${GREEN}Python dependencies installed.${NC}" &&
	exit 0 ||
	echo -e "${RED}An issue was encountered when installing the python dependencies.${NC}" &&
	exit 1
# Raspberry Pi Dependencies
elif [[ "$OSTYPE" == "linux-gnueabihf" ]]; then
	sudo apt-get update &&
	sudo apt-get update
	sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev
	wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tar.xz
	tar xf Python-3.9.0.tar.xz && cd Python-3.9.0  || exit 1
	./configure --prefix=/usr/local/opt/python-3.9.0 && make -j &&
	sudo make altinstall
	cd .. && sudo rm -r Python-3.9.0 && rm Python-3.9.0.tar.xz
	# shellcheck source=/dev/null
	. "${HOME}"/.bashrc
	sudo update-alternatives --config python
	sudo apt-get install ufw python-scipy libatlas-base-dev -y &&
	sudo ufw enable && sudo ufw allow 8988 && sudo ufw allow 22 && # Open port for graph display
	add_user_to_dialout &&
	echo -e "${GREEN}Python dependencies installed.${NC}" &&
	exit 0 ||
	echo -e "${RED}An issue was encountered when installing the python dependencies.${NC}" &&
	exit 1
else
	echo -e "${RED}Unsuported OS $OSTYPE. Nothing was installed.${NC}" &&
	exit 1
fi
