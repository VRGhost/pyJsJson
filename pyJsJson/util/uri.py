import urllib.parse
import posixpath as pp


class URI:
    """URI object."""

    def __init__(self, scheme, path, anchor):
        self.scheme = scheme
        self.path = path
        self.anchor = anchor

    @classmethod
    def fromString(cls, val):
        parseResult = urllib.parse.urlparse(val)

        full_path = []
        if parseResult.netloc:
            full_path.append(parseResult.netloc)
        if parseResult.path:
            full_path.append(parseResult.path)

        return cls(
            scheme=parseResult.scheme or None,
            path=pp.join(*full_path) if full_path else None,
            anchor=parseResult.fragment or None
        )

    def defaults(self, scheme=None, path=None, anchor=None):
        """Return a new URI object with any missing elements replaced with new defaults."""
        cls = self.__class__
        return cls(
            scheme=self.scheme or scheme,
            path=self.path or path,
            anchor=self.anchor or anchor,
        )

    def toString(self):
        out = []
        if self.scheme:
            out.extend([self.scheme, ':'])
        if self.path:
            out.append(self.path)
        if self.anchor:
            out.extend(['#', self.anchor])
        return ''.join(out)

    def __repr__(self):
        return "<{} '{}'>".format(
            self.__class__.__name__,
            self.toString()
        )
