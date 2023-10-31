#!/bin/bash

# Source the configuration file
. ./config.sh

# Ensure the target directory exists
if [[ ! -d ${TARGET_REGISTRY_DIR} ]]; then
    sudo mkdir -p ${TARGET_REGISTRY_DIR}
fi

# Copy the script to the target directory
sudo cp ${SUB_DIR_PATH}/bash_function_manager.py ${TARGET_REGISTRY_DIR}/
sudo cp ${SUB_DIR_PATH}/function_registry.py ${TARGET_REGISTRY_DIR}/
sudo chmod +x ${TARGET_REGISTRY_DIR}/bash_function_manager.py

# Create symbolic links
sudo ln -sf ${TARGET_REGISTRY_DIR}/bash_function_manager.py ${TARGET_BIN_DIR}/register
sudo ln -sf ${TARGET_REGISTRY_DIR}/bash_function_manager.py ${TARGET_BIN_DIR}/list_commands
sudo ln -sf ${TARGET_REGISTRY_DIR}/bash_function_manager.py ${TARGET_BIN_DIR}/edit_command

# Check if registry file exists, if not, create it
if [[ ! -f ${REGISTRY_FILE} ]]; then
    sudo touch ${REGISTRY_FILE}
    sudo chmod 666 ${REGISTRY_FILE}  # Make it readable and writable by everyone
fi
