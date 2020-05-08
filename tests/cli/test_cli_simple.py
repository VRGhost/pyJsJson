"""Simple CLI tests.

Can the module be called?
Is there a help string available?
"""

import subprocess

import pytest


@pytest.mark.parametrize('arg', [
    '-h', '--help'
])
def test_cli_called(cli_popen_args, arg):
    cli_popen_args['args'] += (arg, )
    out = subprocess.check_output(**cli_popen_args)
    assert out.startswith(b'usage: pyJsJson [-h]')
