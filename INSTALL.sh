#!/bin/bash


# Get script's own directory path
SCRIPT_DIR=$(dirname "$0")

# Get absolute path to the src sub-directory
SUB_DIR_PATH=$(realpath "${SCRIPT_DIR}/src")


chmod +x ${SUB_DIR_PATH}/bash_function_manager.py
ln -sf ${SUB_DIR_PATH}/bash_function_manager.py /usr/local/bin/register
ln -sf ${SUB_DIR_PATH}/bash_function_manager.py /usr/local/bin/list_commands
