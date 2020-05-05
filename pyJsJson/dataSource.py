"""A class that provides input data for the expansion process (e.g. reads files)."""

import os

class DataSource:

    def __init__(self, search_paths=()):
        self.search_paths = tuple(
            os.path.abspath(el) for el in search_paths
        )

        for pth in self.search_paths:
            assert os.path.isdir(pth), pth

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__, self.search_paths)