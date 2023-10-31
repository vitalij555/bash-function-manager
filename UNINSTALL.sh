#!/bin/bash

# Source the configuration file
. ./config.sh

# Ask for confirmation
read -p "Are you sure you want to uninstall? This will remove all files and links created by the installer. (yes/no) " confirmation

if [[ $confirmation != "yes" ]]; then
    echo "Uninstallation aborted."
    exit 1
fi

# Remove symbolic links
sudo rm -f ${TARGET_BIN_DIR}/register
sudo rm -f ${TARGET_BIN_DIR}/list_commands
sudo rm -f ${TARGET_BIN_DIR}/edit_command

# Remove the copied python script and the registry directory
sudo rm -f ${TARGET_REGISTRY_DIR}/bash_function_manager.py

# Check if registry file exists, if it does, remove it
if [[ -f ${REGISTRY_FILE} ]]; then
    sudo rm -f ${REGISTRY_FILE}
fi

# If the registry directory is empty, remove it too
if [[ ! "$(ls -A ${TARGET_REGISTRY_DIR})" ]]; then
    sudo rmdir ${TARGET_REGISTRY_DIR}
fi

echo "Uninstallation completed."

