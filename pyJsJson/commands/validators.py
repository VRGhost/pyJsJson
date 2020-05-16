
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
