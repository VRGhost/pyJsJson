class Base:
    """Base class for commands."""

    key = None  # The key for the command (e.g. '$ref')

    def __init__(self, expander, data):
        self.expander = expander
        self.data = data

    @classmethod
    def match(cls, what):
        """Return True if 'what' is a dictionary represeting this command."""
        assert isinstance(what, dict), what
        if cls.key not in what:
            return False
        return True

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.key)
