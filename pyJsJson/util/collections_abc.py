"""Same as collections.abc but also provides abc.Array that matches any tuple/list/iterable but NOT string."""

from collections.abc import *

Array = (list, tuple) # TODO: think of something more elegant.