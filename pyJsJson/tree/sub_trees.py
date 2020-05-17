"""Sub-tree objects. Trees representing lists and dicts and alike."""

from ..base import Expandable

from . import base


class DictTree(base.TreeBase):
    """A tree that spans a JSON dictionery."""

    def getExpandableChildren(self):
        for el in self.getInputData().values():
            if isinstance(el, Expandable):
                yield el

    def getPartialResult(self, key):
        child = self.getInputData()
        return child[key]

class ListTree(base.TreeBase):
    """A tree that spans a json list."""

    def getExpandableChildren(self):
        for el in self.getInputData():
            if isinstance(el, Expandable):
                yield el

    def getPartialResult(self, key):
        child = self.getInputData()
        return child[int(key)]