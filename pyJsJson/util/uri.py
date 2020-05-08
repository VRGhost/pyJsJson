import urllib.parse
import posixpath as pp


class URI:
    """URI object."""

    def __init__(self, scheme, path, anchor):
        self.scheme = scheme
        self.path = path
        self.anchor = anchor

    @classmethod
    def fromString(self, val):
        parseResult = urllib.parse.urlparse(val)
        return cls(
            scheme=parseResult.scheme or None,
            path=pp.join(parseResult.netloc, parseResult.path) or None,
            anchor=parseResult.fragment or None
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
