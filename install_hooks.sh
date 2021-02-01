#!/usr/bin/env bash

# exit when any command fails
set -e

echo This will install the precommit hooks.
echo This means a script is going to run before a commit can be completed
echo The script will take a few minutes to run the first time.
echo To run the hooks manually use \"pre-commit run --all-files\"
echo To avoid running the hook, use \"--no-verify\" when committing.
echo ""

python3 -m pip install pre-commit
pre-commit install
pre-commit autoupdate
pre-commit run --all-files
