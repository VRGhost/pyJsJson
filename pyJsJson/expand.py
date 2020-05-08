"""Main functional class."""
import collections


class JsonExpand:

    def __init__(self, dataSource, rootFileSearcher):
        self.dataSource = dataSource
        self.fileSearcher = rootFileSearcher
        self.commandConstructors = tuple()

    def loadCommands(self, newCommands):
        self.commandConstructors += tuple(newCommands)

    def expandData(self, data):
        tree = self._buildSourceTree(data)
        print(tree)

    def _buildSourceTree(self, data):
        """Convert 'data' object to a rich object with command handlers in place."""
        if isinstance(data, collections.Mapping):
            # Recurse as deep as possible first, detecting any child objects
            rebuiltData = dict(
                (key, self._buildSourceTree(value))
                for (key, value) in data.items()
            )
            for cls in self.commandConstructors:
                if cls.match(rebuiltData):
                    out = cls(self, data)
                    break
            else:
                # no command constructed
                out = rebuiltData
        elif isinstance(data, (list, tuple)):
            out = tuple(
                self._buildSourceTree(el)
                for el in data
            )
        else:
            # Simple/unknown type. No conversion possible
            out = data
        return out
