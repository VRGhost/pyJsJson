"""Main functional class."""

from . import (
    dataSource,
    tree,
    expansion_loop,
)


class JsonExpand:

    def __init__(self):
        self.fileSource = dataSource.FileSource()
        self.commandConstructors = tuple()
        self.loop = expansion_loop.ExpansionLoop()

    def loadCommands(self, newCommands):
        self.commandConstructors += tuple(newCommands)

    def expandAll(self):
        while not self.loop.allExpanded():
            self.loop.next().tryExpand()
        assert self.loop.allExpanded()

    def loadJsonFile(self, filePath, search_dirs):
        """Expand a particular file.

        search_dirs MUST be provided so the expander knows
        that the file is read from an expected location.
        """
        searcher = self.fileSource.searchDirs(search_dirs)
        raw_json = searcher.loadJsonFile(filePath)
        return self._toTree(
            'input:{}'.format(filePath),
            raw_json,
            searcher
        )

    def loadData(self, data, search_dirs=()):
        searcher = self.fileSource.searchDirs(search_dirs)
        return self._toTree(
            'input:data',
            data,
            searcher
        )

    def _toTree(self, label, data, searcher):
        return tree.construct_tree(
            data,
            name=label,
            expander=self,
            commandConstructors=self.commandConstructors,
            searchDirs=searcher.searchDirs,
        )
