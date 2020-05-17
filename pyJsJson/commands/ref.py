import os
import posixpath as pp

from ..util import URI, collections_abc

from . import (
    base,
    exceptions,
    validators,
)
from ..base import Expandable
from ..tree import TreeCls

def _parseRefUri(val):
    uri = URI.fromString(val)
    if not uri.scheme and not uri.path and uri.anchor:
        # Only anchor specified => self-reference
        uri = uri.defaults(
            scheme='__tree__',
            path='__self__',
        )
    return uri

class RefSubtreeWalker(Expandable):

    def __init__(self, expansion_loop, parent_ref, tree, path):
        super(RefSubtreeWalker, self).__init__(expansion_loop)
        self.parentRef = parent_ref
        self.currentTarget = tree
        self.fullPath = self.pathRemaining = tuple(path)
        self._result = None

    def dependsOn(self):
        return (
            self.currentTarget,
        )

    def expandStep(self):
        new_remaining = list(self.pathRemaining)
        new_target = self.currentTarget

         # A function to mark if branches that have actually consumed an element of walkable path
        _consumeKey = lambda: new_remaining.pop(0)
        while new_remaining:
            key = new_remaining[0]
            if isinstance(new_target, collections_abc.Mapping):
                try:
                    new_target = new_target[key]
                except KeyError:
                    self._setResult(exceptions.InvalidReference(self.parentRef, key))
                    return
                # No errors
                _consumeKey()
            elif isinstance(new_target, collections_abc.Array):
                try:
                    key = int(key)
                except ValueError:
                    1/0
                2/0
            elif isinstance(new_target, TreeCls):
                # wait for the next expansion step
                try:
                    new_target = self.currentTarget.getPartialResult(key)
                except (KeyError, IndexError, ValueError):
                    self._setResult(exceptions.InvalidReference(self.parentRef, key))
                    return
                _consumeKey()
                break
            elif isinstance(new_target, base.Expandable):
                if new_target.isExpanded():
                    new_target = new_target.getResult()
                break # always wait for the next expansion loop.
            else:
                raise NotImplementedError(new_target)
        print("NT", new_target)
        if new_remaining:
            self.pathRemaining = tuple(new_remaining)
            self.currentTarget = new_target
        else:
            self._setResult(new_target)

    def _setResult(self, result):
        self.pathRemaining = None # Force for the walker to be expanded
        self._result = result

    def getResult(self):
        rv = self._result
        if isinstance(rv, Exception):
            raise rv
        return rv

    def isExpanded(self):
        return super(RefSubtreeWalker, self).isExpanded() and (not self.pathRemaining)

    def __repr__(self):
        return "<{} target={} path {{ remaining={} ; full={} }}>".format(
            self.__class__.__name__, self.currentTarget,
            self.pathRemaining, self.fullPath,
        )

class Ref(base.Base):
    """$ref expander."""

    key = '$ref'

    validator = validators.PrimitiveDataValidator(
        input_type=str,
        cast_func=_parseRefUri,
    )

    _waitingForTree = None

    def expandStep(self):
        uri = self.data
        scheme = uri.scheme
        out_fn = None

        if scheme == 'file':
            subTree = self._expandFile(uri.path)
            self._setSubTreeResult(subTree)
        elif scheme == '__tree__':
            # Direct tree reference.
            #  Only self-references are expected to work like this for now.
            assert uri.path == '__self__', uri.path
            self._setSubTreeResult(self.root)
        else:
            raise exceptions.UnsupportedOperation("I don't know how to expand {!r} scheme ({})".format(
                scheme,
                uri
            ))
        return out_fn

    def _setSubTreeResult(self, subTree):
        """Set an element of subtree as a result."""
        if self.data.anchor:
            result = RefSubtreeWalker(
                expansion_loop=self.expansion_loop,
                parent_ref=self,
                tree=subTree,
                path=(
                    el
                    for el in self.data.anchor.split(pp.sep)
                    if el # remove any empty elements
                ),
            )
        else:
            result = subTree
        self.setResult(result)
        assert self.hasResult()

    def _expandFile(self, uri_path):
        """Expand a file."""
        # A naive way to convert slashes to OS-specific flavour.
        #  TODO: find a better implementation
        os_path = uri_path.replace(pp.sep, os.sep)
        return self.root.loadJsonFile(os_path)
