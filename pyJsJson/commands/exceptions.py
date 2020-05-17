from .. import exceptions


class CommandException(exceptions.PyJsJsonException):
    """Generic Command exception."""


class InvalidInputDataError(CommandException):
    """Input data is somehow broken."""


class UnsupportedOperation(CommandException):
    """The command was asked to do something that it can't."""


class ExpansionFailure(CommandException):
    """The expansion was proceeding fine untill something broke down."""


class InvalidReference(ExpansionFailure):
    """An exceotion that is raised when reference is invalid somehow."""

    def __init__(self, ref, missing_el):
        super(InvalidReference, self).__init__("Unable to access element {!r} of reference {!r}".format(
            missing_el, ref,
        ))
        self.ref = ref
        self.key = missing_el