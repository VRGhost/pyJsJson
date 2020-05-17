
import itertools

from ..base import ExpandableData
from .base import convertToResults

class JsonTreeRoot(ExpandableData):
    """An object constructed from raw input json dictionary.

    Has all respective fields replaced with Expandable objects.
    """

    def __init__(self, name: str, expander, commandConstructors, searchDirs):
        super(JsonTreeRoot, self).__init__(expansion_loop=expander.loop)
        self.expander = expander
        self.name = name
        self.searchDirs = tuple(searchDirs)
        self.commandConstructors = commandConstructors
        self._dependsOnRoots = []

    def expandStep(self):
        self.getInputData().tryExpand()

    def dependsOn(self):
        return itertools.chain(
            (
                self.getInputData(),
            ),
            self._dependsOnRoots,
        )

    def getResult(self):
        return convertToResults(self.getInputData())

    def getPartialResult(self, path):
        return self.getInputData().getPartialResult(path)

    def loadJsonFile(self, path):
        # Load another JSON file.
        tree = self.expander.loadJsonFile(
            path,
            self.searchDirs
        )
        self._dependsOnRoots.append(tree)
        return tree

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.name)