import copy
import collections
import logging

from . import exceptions

from .. import base as parentBase


logger = logging.getLogger(__name__)


class PrimitiveDataValidator:
    """A class to perform validation of primitive data types (int, str, ...)"""

    def __init__(self, input_type=object, validate_input_fn=None, cast_func=None):
        self.validate_input_fn = validate_input_fn
        self.input_type = input_type
        self.cast_func = cast_func

    def validate(self, inp):
        """Validate user input. Return 'True' if valid, False otherwise."""
        if not isinstance(inp, self.input_type):
            return False
        if self.validate_input_fn is not None:
            if not self.validate_input_fn(inp):
                return False
        return True

    def cast(self, inp):
        """Cast input data to internal struct."""
        if self.cast_func is None:
            out = inp
        else:
            out = self.cast_func(inp)
        return out

    def __repr__(self):
        return "<{} required={} typ={}>".format(
            self.__class__.__name__,
            self.required,
            self.input_type
        )


class DictValidator(PrimitiveDataValidator):
    """A validator that validates input dictionary."""

    def __init__(
        self,
        requiredKeys=(),
        defaults=None,  # key -> value for default keys that are not required.
        inputDataTypes=None,  # key -> callable for user-provided data values
    ):
        super(DictValidator, self).__init__(
            input_type=dict,
            validate_input_fn=self._validateDict,
            cast_func=self._castDict,
        )

        self.requiredKeys = frozenset(requiredKeys)
        self.defaults = defaults or {}
        self.inputTypes = inputDataTypes or {}

    def validate(self, data):
        if not isinstance(data, collections.Mapping):
            return False

        missingReq = self.requiredDataKeys.difference(inp.keys())
        if missingReq:
            logger.error("Missing required keys: {}".format(missingReq))
            return False

        for key in (self.inputTypes.keys() & data.keys):
            1/0

    def cast(self, data):
        1/0


class Base(parentBase.Expandable):
    """Base class for commands."""

    key = None  # The key for the command (e.g. '$ref')
    validator = None  # instance of PrimitiveDataValidator

    def __init__(self, parent_tree, json_el, child_commands):
        self.parentTree = parent_tree
        self._element = json_el
        self._children = tuple(child_commands)
        self._dependsOn = self._children

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
        inp = self._element[self.key]
        if not self.validator.validate(inp):
            raise exceptions.InvalidInputDataError('Invalid input data')
        return self.validator.cast(inp)

    @property
    def dependsOn(self):
        """Return a list of commands that must be expanded BEFORE this command is expandable."""
        return self._dependsOn

    def depsExpanded(self):
        """Return True if all dependencies are ready."""
        for dep in self.dependsOn:
            if not dep.isExpanded():
                return False
        return True

    def tryExpand(self):
        # Only attempt to expand self if all dependencies are ready.
        if self.depsExpanded():
            return super(Base, self).tryExpand()

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
        return "<{} {!r}>".format(self.__class__.__name__, self.key)


class StatefulBase(Base):
    """A command that transitions through multiple implementations of expand() code.

    The implementations of the expand function should return next function to be called or None
    """

    _expandFn = None

    def expandStep(self):
        if callable(self._expandFn):
            assert not self.hasResult(), 'There has to be NO result set if the expand() chain is not done'
            self._expandFn = self._expandFn()
        else:
            assert self.hasResult(), 'There has to be a result set if the expand() chain is done'
