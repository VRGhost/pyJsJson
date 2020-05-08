"""Main functional class."""
import collections

from . import dataSource

class JsonTree:
    """An object constructed from raw input json dictionary.

    Has all respective fields replaced with Expandable objects.
    """

    def __init__(self, raw_json, commandConstructors):
        self.commandConstructors = commandConstructors
        (
            self._tree,
            self._allExpandableObjs,
        ) = self._buildSourceTree(raw_json)

        self._allExpandableObjs = list(self._allExpandableObjs)

    def expand(self):
        """Expand this tree until done."""
        while not self.expanded:
            self._expandStep()

    def _expandStep(self):
        # FIXME: just a tmp implementation (circular buffer).
        # Takes the first expandable element, attempts to expand it
        # and puts it back into the list last
        if not self._allExpandableObjs:
            return

        target = self._allExpandableObjs.pop(0)
        target.tryExpand()
        self._allExpandableObjs.append(target)

    @property
    def expanded(self):
        """Return True when all expandable objects had been expanded."""
        return all(obj.expanded for obj in self._allExpandableObjs)


    def _buildSourceTree(self, data):
        """Convert 'data' object to a rich object with command handlers in place.

        Returns (output_struct, [<all expandable objs>]) tuple
        """
        if isinstance(data, collections.Mapping):
            # Recurse as deep as possible first, detecting any child objects
            rebuilt_dict = {}
            out_expandable = []
            for (key, value) in data.items():
                (sub_val, sub_expandable) = self._buildSourceTree(value)
                out_expandable.extend(sub_expandable)
                rebuilt_dict[key] = sub_val

            for cls in self.commandConstructors:
                if cls.match(rebuilt_dict):
                    out_obj = cls(
                        self, rebuilt_dict,
                        child_commands=tuple(out_expandable),
                    )
                    out_expandable.append(out_obj)
                    break
            else:
                # no command constructed
                out_obj = rebuilt_dict

        elif isinstance(data, (list, tuple)):
            out_obj = []
            out_expandable = []

            for sub_el in data:
                (sub_obj, sub_expandable) = self._buildSourceTree(sub_el)
                out_obj.append(sub_obj)
                out_expandable.extend(sub_expandable)

            # Replace with immutable types. Just in case.
            out_obj = tuple(out_obj)
            out_expandable = out_expandable
        else:
            # Simple/unknown type. No conversion possible
            out_obj = data
            out_expandable = ()
        return (out_obj, tuple(out_expandable))


    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__, self._tree)

class JsonExpand:

    def __init__(self):
        self.fileSource = dataSource.FileSource()
        self.commandConstructors = tuple()

    def loadCommands(self, newCommands):
        self.commandConstructors += tuple(newCommands)

    def expandFile(self, filePath, search_dirs):
        """Expand a particular file.

        search_dirs MUST be provided so the expander knows
        that the file is read from an expected location.
        """
        searcher = self.fileSource.searchDirs(search_dirs)
        raw_json = searcher.loadJsonFile(filePath)
        return self._expandRawData(raw_json, searcher)

    def expandData(self, data, search_dirs=()):
        searcher = self.fileSource.searchDirs(search_dirs)
        return self._expandRawData(data, searcher)

    def _expandRawData(self, data, searcher):
        tree = JsonTree(
            data,
            self.commandConstructors,
        )
        print(tree)
        tree.expand()
        print(tree)
        1/0

