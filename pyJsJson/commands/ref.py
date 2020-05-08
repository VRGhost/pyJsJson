import os

import posixpath as pp

from ..util import URI

from . import (
    base,
    exceptions,
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
                    key=key, out=out, pth=walked, inp=orig_inp
                )
            )
        traversed.append(key)
    return out


class Ref(base.StatefulBase):
    """$ref expander."""

    key = '$ref'

    validator = base.PrimitiveDataValidator(
        input_type=str,
        cast_func=URI.fromString,
    )

    _waitingForTree = None
    _waitingForPath = None

    def expand_start(self):
        uri = self.data
        scheme = uri.scheme
        out_fn = None

        if scheme == 'file':
            subTree = self._expandFile(uri.path)
            self.addDependency(subTree)
            self._waitingForTree = subTree
            out_fn = self.expand_tree
        else:
            raise exceptions.UnsupportedOperation("I don't know how to expand {!r} scheme ({})".format(
                scheme,
                uri
            ))
        return out_fn

    def expand_tree(self):
        assert self._waitingForTree is not None
        assert self._waitingForTree.isExpanded(), 'The tree I am waiting for should be expanded by now'
        sub_tree_path = self.data.anchor
        out = self._waitingForTree.getResult()
        if sub_tree_path:
            sub_tree_path = sub_tree_path.split(pp.sep)

        self.setResult(out)
        return None  # No further transitions

    _expandFn = expand_start

    def _expandFile(self, uri_path):
        """Expand a file."""
        # A naive way to convert slashes to OS-specific flavour.
        #  TODO: find a better implementation
        os_path = uri_path.replace(pp.sep, os.sep)
        return self.parentTree.loadJsonFile(os_path)
