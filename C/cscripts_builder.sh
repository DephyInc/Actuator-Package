#!/bin/bash

# Exit this script immediately upon any error.
set -e

echo "Building C++ programs for plan stack"

# guest host OS
if [[ $1 = "-pi" ]]; then
	HOST_OS="raspberryPi"
elif [[ "$OSTYPE" == "linux-gnu" ]]; then
	HOST_OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
	HOST_OS="mac"
elif [[ "$OSTYPE" == "cygwin" ]]; then
	HOST_OS="windows"
elif [[ "$OSTYPE" == "msys" ]]; then
	HOST_OS="windows"
else
	HOST_OS="linux"
fi

rm -rf build
mkdir -p build
cd build
if  [[ "$HOST_OS" = "raspberryPi" ]]; then
	cmake .. -G Ninja -DCMAKE_TOOLCHAIN_FILE=CMAKE_RASPBERRY_PI_TOOLCHAIN_FILE
elif  [[ "$HOST_OS" = "windows" ]]; then
	cmake .. -G Ninja ..
elif [[ $1 = "proto" ]]; then # protocol buffer test
	# force gcc 7
	cmake -G Ninja -D CMAKE_C_COMPILER=gcc-7 -D CMAKE_CXX_COMPILER=g++-7 \
		-DPROTOCOL_TYPE=PROTOCOL_BUFFERS ..
else
	# force gcc 7
	cmake -G Ninja -D CMAKE_C_COMPILER=gcc-7 -D CMAKE_CXX_COMPILER=g++-7 ..
fi

# run ninja
ninja
# move out of the build directory
cd ..

exit 0

