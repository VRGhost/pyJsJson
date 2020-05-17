"""Classes that represent expansion trees."""

from .base import TreeBase
from .root import JsonTreeRoot
from .sub_trees import DictTree, ListTree
from .construct import construct_tree

TreeCls = (JsonTreeRoot, TreeBase) # A tuple for isinstance() mathcing