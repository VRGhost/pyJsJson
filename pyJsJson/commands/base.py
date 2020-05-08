import copy

from . import exceptions

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

    def __init__(self):
        super(DictValidator, self).__init__(
            input_type=dict,
            validate_input_fn=self._validateDict,
            cast_func=self._castDict,
        )

class Base:
    """Base class for commands."""

    key = None  # The key for the command (e.g. '$ref')

    requiredDataKeys = frozenset([]) # What keys MUST be provided in the input data
    defaultDataValues = {} # key -> value for default keys that are not required.
    inputDataTypes = {} # key -> callable for user-provided data values

    def __init__(self, expander, json_el, child_commands):
        self.expander = expander
        self._element = json_el
        self._children = tuple(child_commands)
        self._expanded = False  # Set to 'True' when expansion of the current element is complete

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

        missingReq = self.requiredDataKeys.difference(inp.keys())
        if missingReq:
            raise exceptions.InvalidInputDataError("Missing required keys: {}".format(missingReq))

        out = copy.deepcopy(self.defaultDataValues)

        for (key, value) in inp.items():
            if key in self.inputDataTypes:
                cast_fn = self.inputDataTypes[key]
                cast_val = cast_fn(value)
            else:
                cast_val = value
            out[key] = cast_val

        return out

    @property
    def dependsOn(self):
        """Return a list of commands that must be expanded BEFORE this command is expandable."""
        return self._children

    @property
    def expanded(self):
        for dep in self.dependsOn:
            if not dep.expanded:
                return False

        return self._expanded

    def tryExpand(self):
        if not self.expanded:
            self.expand()
            self._expanded = True

    def expand(self):
        raise NotImplementedError(self.__class__)

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.key)
