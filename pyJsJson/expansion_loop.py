"""Expansion loop(s)."""


class ExpansionLoop:
    """An object that successively calls expansions of any expandable objects it is tracking."""

    def __init__(self):
        self._loop = []
        self._lastElIdx = 0
        self._needsSort = True

    def extend(self, els):
        self._loop.extend(els)
        self._needsSort = True

    def add(self, el):
        self._loop.append(el)
        self._needsSort = True

    def next(self):
        """Return next element to be expanded."""
        if self._needsSort:
            self._sort()

        startIdx = self._nextIdx()
        if startIdx is None:
            return None
        return self._loop[startIdx]

    def _nextIdx(self):
        """Increment and return next element index."""
        if not self._loop:
            return None

        out = self._lastElIdx + 1
        out = max(0, out) % len(self._loop)
        self._lastElIdx = out
        return out

    def _sort(self):
        """Sort elements in the loop."""
        # TODO
        pass
        self._lastElIdx = 0
        self._needsSort = False

    def allExpanded(self):
        for el in self._loop:
            if not el.isExpanded():
                return False
        return True

    def allEls(self):
        return tuple(self._loop)

    def __repr__(self):
        return "<{} ({} elements)>".format(
            self.__class__.__name__, len(self._loop)
        )
