from .. import exceptions

class CommandException(exceptions.PyJsJsonException):
    """Generic Command exception."""

class InvalidInputDataError(CommandException):
    """Input data is somehow broken."""