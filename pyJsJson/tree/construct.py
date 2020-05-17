from . import (
    JsonTreeRoot,
    DictTree, ListTree,
)

from .. import util

def _construct_subtree(expansion_loop, root, parent, name, data):
    _this_fn = _construct_subtree
    if isinstance(data, util.collections_abc.Mapping):
        # Recurse as deep as possible first, detecting any child objects

        for cls in root.commandConstructors:
            if cls.match(data):
                out_obj = cls(
                    expansion_loop=expansion_loop,
                    root=root,
                )
                break
        else:
            # no command constructed
            out_obj = DictTree(
                expansion_loop=expansion_loop,
                root=root,
                parent=parent,
                name=name,
            )

        rebuilt_payload = dict(
            (
                key,
                _this_fn(
                    expansion_loop=expansion_loop,
                    root=root,
                    parent=out_obj,
                    name="[{}]".format(key),
                    data=value
                )
            )
            for (key, value) in data.items()
        )
        out_obj.setInputData(rebuilt_payload)
    elif isinstance(data, util.collections_abc.Array):
        out_obj = ListTree(
            expansion_loop=expansion_loop,
            root=root,
            parent=parent,
            name=name,
        )
        out_obj.setInputData(tuple(
            _this_fn(
                expansion_loop=expansion_loop,
                root=root,
                parent=out_obj,
                name="[{}]".format(idx),
                data=el
            )
            for (idx, el) in enumerate(data)
        ))
    else:
        # Simple/unknown type. No conversion possible
        out_obj = data
    return out_obj

def construct_tree(data, **kwargs):
    root = JsonTreeRoot(**kwargs)
    struct = _construct_subtree(
        expansion_loop=root.expansion_loop,
        root=root,
        parent=None, name='<ROOT>',
        data=data
    )
    root.setInputData(struct)
    return root