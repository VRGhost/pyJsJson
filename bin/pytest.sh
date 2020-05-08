#!/bin/bash -e

source "$(dirname "${BASH_SOURCE[0]}")/env.sh"

ENV_NAME='py-js-json-test'
init_venv "${ENV_NAME}"
source "$(get_venv_root "${ENV_NAME}")/bin/activate"
maybe_run_pip_install "${ENV_NAME}" "${REQUIREMENTS_DIR}/development.txt"

exec python -m pytest -c "${PROJ_ROOT}/pytest.ini"