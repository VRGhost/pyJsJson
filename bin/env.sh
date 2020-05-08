#!/bin/bash

# Utility functions/vars


BIN_DIR=$(readlink -f $(dirname "${BASH_SOURCE[0]}"))

PROJ_ROOT="${BIN_DIR}/.."
BUILD_DIR="${PROJ_ROOT}/build"
REQUIREMENTS_DIR="${PROJ_ROOT}/requirements"

PYTHON='python3'

function get_venv_root() {
    # Return path to the venv
    ENV_NAME="$1"
    echo "${BUILD_DIR}/venv-${ENV_NAME}"
}

function init_venv() {
    # Init an mew 'venv' (name $1) if it does not exist yet

    ENV_NAME="$1"
    DEV_VENV_DIR=$(get_venv_root "${ENV_NAME}")

    if [ ! -e "${BUILD_DIR}" ]
    then
        mkdir -p "${BUILD_DIR}"
    fi

    if [ ! -e "${DEV_VENV_DIR}" ]
    then
        "${PYTHON}" -m venv --prompt "${ENV_NAME}"  "${DEV_VENV_DIR}"
    fi
}

function maybe_run_pip_install() {
    # Run pip install for $2 IF the files in requirements/* had been changed
    ENV_NAME="$1"
    REQ_FILE_TO_INSTALL="$2"

    ENV_ROOT=$(get_venv_root "${ENV_NAME}")
    OLD_REQ_FILE_HASH_FILE="${ENV_ROOT}/requirements-hashes.txt"
    NEW_REQ_HASHES=$(sha1sum ${REQUIREMENTS_DIR}/* | sort)

    if [[ "${NEW_REQ_HASHES}" != "$(cat "${OLD_REQ_FILE_HASH_FILE}")" ]]
    then
        # Change detected. Update.
        "${ENV_ROOT}/bin/pip" install -r "${REQ_FILE_TO_INSTALL}"
        echo -n "${NEW_REQ_HASHES}" > "${OLD_REQ_FILE_HASH_FILE}"
    fi
}