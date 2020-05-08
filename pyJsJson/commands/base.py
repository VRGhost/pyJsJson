class Base:
    """Base class for commands."""

    key = None  # The key for the command (e.g. '$ref')

    def __init__(self, expander, data):
        self.expander = expander
        self.data = data
        self.expanded = False

    @classmethod
    def match(cls, what):
        """Return True if 'what' is a dictionary represeting this command."""
        assert isinstance(what, dict), what
        if cls.key not in what:
            return False
        return True

    def tryExpand(self):
        if not self.expanded:
            self.expand()

    def expand(self):
        raise NotImplementedError(self.__class__)

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.key)
