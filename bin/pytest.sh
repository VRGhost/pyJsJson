#!/bin/bash -e

TEST_ARGS="$@"

source "$(dirname "${BASH_SOURCE[0]}")/env.sh"

if [[ -z "${SKIP_VENV_INIT}" ]]
then
    ENV_NAME='py-js-json-test'
    init_venv "${ENV_NAME}"
    source "$(get_venv_root "${ENV_NAME}")/bin/activate"
    maybe_run_pip_install "${ENV_NAME}" "${REQUIREMENTS_DIR}/development.txt"
fi

cd "${PROJ_ROOT}"
exec python -m pytest -c "${PROJ_ROOT}/pytest.ini" "${TEST_ARGS[@]}"