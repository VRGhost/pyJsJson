import os

import posixpath as pp

from ..util import URI

from . import (
    base,
    exceptions,
    validators,
)


def walk_path_in_dict(target, path):
    traversed = []
    orig_inp = target
    out = target
    for key in path:
        try:
            out = out[key]
        except KeyError:
            raise exceptions.ExpansionFailure(
                "Failed to access key {key!r} in {out}. "
                "Path traversed so far: {pth}, original input: {inp}".format(
                    key=key, out=out, pth=traversed, inp=orig_inp
                )
            )
        traversed.append(key)
    return out


def _parseRefUri(val):
    uri = URI.fromString(val)
    if not uri.scheme and not uri.path and uri.anchor:
        # Only anchor specified => self-reference
        uri = uri.defaults(
            scheme='__tree__',
            path='__self__',
        )
    return uri

class Ref(base.StatefulBase):
    """$ref expander."""

    key = '$ref'

    validator = validators.PrimitiveDataValidator(
        input_type=str,
        cast_func=_parseRefUri,
    )

    _waitingForTree = None

    def expand_start(self):
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
            raise NotImplementedError
            self._waitingForTreeFuture = self.root.expander.getFutureResult(self.data.anchor)
            out_fn = self.waiting_for_tree_future
        else:
            raise exceptions.UnsupportedOperation("I don't know how to expand {!r} scheme ({})".format(
                scheme,
                uri
            ))
        return out_fn

    _expandFn = expand_start

    def _setSubTreeResult(self, subTree):
        """Set an element of subtree as a result."""
        if self.data.anchor:
            raise NotImplementedError
        else:
            result = subTree
        self.setResult(result)
        print(self, id(self))
        assert self.hasResult()

    def _expandFile(self, uri_path):
        """Expand a file."""
        # A naive way to convert slashes to OS-specific flavour.
        #  TODO: find a better implementation
        os_path = uri_path.replace(pp.sep, os.sep)
        return self.root.loadJsonFile(os_path)
