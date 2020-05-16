import os

import pytest


@pytest.fixture
def expand_data():
    """Returns a callable to expand an input command."""

    import pyJsJson

    def _doExpand(data):
        expand = pyJsJson.expand.JsonExpand()
        expand.loadCommands(pyJsJson.commands.DEFAULT_COMMANDS)
        tree = expand.loadData(data, search_dirs=[
            os.path.join(os.sep, 'unittest')
        ])
        expand.expandAll()
        return tree.getResult()

    return _doExpand
