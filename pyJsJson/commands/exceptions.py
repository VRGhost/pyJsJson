from .. import exceptions


class CommandException(exceptions.PyJsJsonException):
    """Generic Command exception."""


class InvalidInputDataError(CommandException):
    """Input data is somehow broken."""


class UnsupportedOperation(CommandException):
    """The command was asked to do something that it can't."""


class ExpansionFailure(CommandException):
    """The expansion was proceeding fine untill something broke down."""
