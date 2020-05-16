"""Tree base class."""

import functools
import collections.abc

from abc import (
    ABC,
    abstractmethod,
)

from .. import base


def convertToResults(data):
    if isinstance(data, base.Expandable):
        if not data.isExpanded():
            print('VVVVVV')
            print(data)
            for el in data.dependsOn():
                print(el.isExpanded())
            print(data, tuple(data.dependsOn()), id(data))
            1/0
        assert data.isExpanded(), data
        out = convertToResults(
            data.getResult()
        )
    elif isinstance(data, collections.abc.Mapping):
        out = dict(
            (key, convertToResults(value))
            for (key, value) in data.items()
        )
    elif isinstance(data, (list, tuple)):
        out = tuple(convertToResults(el) for el in data)
    else:
        # Must be a primitive object
        out = data
    return out

class TreeBase(base.ExpandableData):

    def __init__(self, expansion_loop, root, parent: base.Expandable, name: str):
        """json_struct is the appropriate json subtree element.
        """
        super(TreeBase, self).__init__(expansion_loop)
        self.root = root
        self.parent = parent
        self.name = name

    @functools.cached_property
    def fqn(self):
        """Fully qualified name."""
        els = []
        if self.parent:
            els.append(self.parent.fqn)
        els.append(self.name)
        return '.'.join(els)

    @abstractmethod
    def getExpandableChildren(self):
        """Return all expandable objects inside this tree."""

    @abstractmethod
    def getStructPath(self, path):
        """Return a subtree/expandable found under the chain of 'path' elements."""

    def dependsOn(self):
        return tuple(self.getExpandableChildren())

    def expandStep(self):
        pass

    def getAllSubTrees(self):
        """Return all trees inside this one."""
        for el in self.getExpandables():
            if isinstance(el, TreeBase):
                yield el

    def __repr__(self):
        try:
            payload = self.getInputData()
        except AttributeError:
            payload = '!!! UNINITIALISED !!!'

        return "<{} {!r} {}>".format(self.__class__.__name__, self.fqn, payload)

    def getResult(self):
        return convertToResults(self.getInputData())