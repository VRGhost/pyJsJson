import os

import pytest


THIS_DIR = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def PROJECT_ROOT():
    return os.path.join(THIS_DIR, os.pardir)


@pytest.fixture
def PY_JS_JSON_ROOT(PROJECT_ROOT):
    return os.path.join(PROJECT_ROOT, 'pyJsJson')
