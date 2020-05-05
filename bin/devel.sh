#!/bin/bash -xe

BIN_DIR=$(readlink -f $(dirname "${BASH_SOURCE[0]}"))
PROJ_ROOT="${BIN_DIR}/.."
BUILD_DIR="${PROJ_ROOT}/build"
DEV_VENV_DIR="${BUILD_DIR}/devel-env"
PYTHON='python3'

if [ ! -e "${BUILD_DIR}" ]
then
    mkdir -p "${BUILD_DIR}"
fi

if [ ! -e "${DEV_VENV_DIR}" ]
then
    "${PYTHON}" -m venv --prompt 'py-js-json-dev'  "${DEV_VENV_DIR}"
fi

exec bash --rcfile <(echo '. ~/.bashrc;' "cd '${PROJ_ROOT}' ; . '${DEV_VENV_DIR}/bin/activate'")