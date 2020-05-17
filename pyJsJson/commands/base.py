import logging

from . import exceptions

from .. import base as parentBase
from .. import util

logger = logging.getLogger(__name__)


def _findAllExpandables(obj):
    iter_in = ()
    if isinstance(obj, parentBase.Expandable):
        yield obj
    elif isinstance(obj, util.collections_abc.Array):
        iter_in = obj
    elif isinstance(obj, util.collections_abc.Mapping):
        iter_in = obj.values()

    for el in iter_in:
        for exp in _findAllExpandables(el):
            yield exp

class Base(parentBase.ExpandableData):
    """Base class for commands."""

    key = None  # The key for the command (e.g. '$ref')
    validator = None  # instance of PrimitiveDataValidator

    def __init__(self, expansion_loop, root):
        super(Base, self).__init__(expansion_loop)
        self.root = root

    @classmethod
    def match(cls, what):
        """Return True if 'what' is a dictionary represeting this command."""
        assert isinstance(what, dict), what
        if cls.key not in what:
            return False
        return True

    @property
    def data(self):
        """Return sanitised version of input arguments."""
        inp = self.getInputData()[self.key]
        if not self.validator.validate(inp):
            raise exceptions.InvalidInputDataError('Invalid input data')
        return self.validator.cast(inp)

    def onDataSet(self):
        self._dependsOn = list(_findAllExpandables(self.getInputData()))

    def dependsOn(self):
        """Return a list of commands that must be expanded BEFORE this command is expandable."""
        return self._dependsOn

    def isExpanded(self):
        return self.hasResult()

    def getResult(self):
        return self._result

    def setResult(self, newVal):
        if self.hasResult():
            raise exceptions.CommandException('The command already has a result')
        self._result = newVal
        assert self.hasResult()

    def addDependency(self, newDep):
        """Add a new dependency that had just been discovered."""
        self._dependsOn += (newDep, )

    def hasResult(self):
        return hasattr(self, '_result')

    def __repr__(self):
        return "<{} {!r} {!r} has_result={} {}>".format(
            self.__class__.__name__, self.key, self.data,
            self.hasResult(),
            id(self)
        )
