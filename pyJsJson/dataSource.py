"""A class that provides input data for the expansion process (e.g. reads files)."""

import os
import logging
import copy
import json

from . import exceptions

logger = logging.getLogger(__name__)


class DataSource:

    def __init__(self):
        self._cache = {}
        self._currentSearchDirs = None

    def _loadJsonFile(self, path):
        try:
            out = self._cache[path]
        except KeyError:
            try:
                with open(path, 'r') as fin:
                    out = json.load(fin)
            except:
                logging.exception("Error loading JSON from file {!r}".format(path))
                raise
            logger.debug('{!r} loaded'.format(path))
            self._cache = out
        return copy.deepcopy(out)

    def searchDirs(self, dirs):
        logger.info("Setting searchDirs to {}".format(dirs))
        return DirSearchContext(self, dirs)

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__, self.search_paths)


class DirSearchContext:

    def __init__(self, dataSource, searchDirs):
        self.dataSource = dataSource
        self.searchDirs = tuple(
            os.path.abspath(pth)
            for pth in searchDirs
        )
        if __debug__:
            assert all(os.path.isdir(pth) for pth in self.searchDirs), self.searchDirs

    def loadJsonFile(self, path):
        for tryRoot in self.searchDirs:
            maybeFile = os.path.join(tryRoot, path)
            if maybeFile.startswith(tryRoot + os.sep) and os.path.isfile(maybeFile):
                return self.dataSource._loadJsonFile(maybeFile)
        else:
            raise exceptions.FsError("File not found: {!r} (checked in {})".format(
                path, self.searchDirs
            ))

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__, self.searchDirs)
