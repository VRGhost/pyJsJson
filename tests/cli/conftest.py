import os

import pytest


@pytest.fixture
def cli_popen_args(PROJECT_ROOT, PY_JS_JSON_ROOT):
    """Return popen args required to call the module as a CLI program."""
    env = os.environ.copy()
    env['PYTHONPATH'] = PROJECT_ROOT
    return {
        'args': ('python', PY_JS_JSON_ROOT),
        'env': env
    }
