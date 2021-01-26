#!/usr/bin/env python3
"""Build binary libraries from external repo. Can't run form this repo."""

import os
import sys

IS_WINDOWS = os.name == "nt"
IS_64BITS = sys.maxsize > 2 ** 32

MAKE_CMD = "mingw32-make -j" if IS_WINDOWS else "make"
COPY_CMD = "copy" if IS_WINDOWS else "cp"
CMAKE_CMD = "cmake"

# Paths
ORIGINAL_DIR = os.getcwd()
STACK_BUILD_DIR = os.path.join(ORIGINAL_DIR, "fx_plan_stack", "build")
CSCRIPT_BUILD_DIR = os.path.join(ORIGINAL_DIR, "acpac_cscripts", "build")
PATH_TO_DLL = os.path.join(STACK_BUILD_DIR, "libs", "libfx_plan_stack.dll")

print(STACK_BUILD_DIR)

os.chdir(STACK_BUILD_DIR)
os.system(f"{CMAKE_CMD} .. -DCOMPILE_SHARED=ON")
os.system(MAKE_CMD)

COPY_CMD = f'{COPY_CMD} "{PATH_TO_DLL}" "{CSCRIPT_BUILD_DIR}"'
print(f"Executing:: {COPY_CMD}")
os.system(COPY_CMD)

os.chdir(CSCRIPT_BUILD_DIR)
os.system(f'{CMAKE_CMD} .. -G "MinGW Makefiles"')
os.system(MAKE_CMD)
