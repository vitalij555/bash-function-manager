# config.sh

SCRIPT_DIR=$(dirname "$0")
SUB_DIR_PATH=$(realpath "${SCRIPT_DIR}/src")

TARGET_BIN_DIR=/usr/local/bin
TARGET_REGISTRY_DIR=/usr/local/bash_function_registry
REGISTRY_FILE=${TARGET_REGISTRY_DIR}/registry.json
