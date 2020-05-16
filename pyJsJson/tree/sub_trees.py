"""Sub-tree objects. Trees representing lists and dicts and alike."""

from ..base import Expandable

from . import base


class DictTree(base.TreeBase):
    """A tree that spans a JSON dictionery."""

    def getExpandableChildren(self):
        for el in self.getInputData().values():
            if isinstance(el, Expandable):
                yield el

    def getStructPath(self, path):
        key = path[0]
        tail = path[1:]
        child = self.getInputData()
        1/0

class ListTree(base.TreeBase):
    """A tree that spans a json list."""

    def getExpandableChildren(self):
        for el in self.getInputData():
            if isinstance(el, Expandable):
                yield el

    def getStructPath(self, path):
        1/0