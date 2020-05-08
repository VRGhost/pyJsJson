"""Base classes."""

from abc import (
    ABC,
    abstractproperty,
    abstractmethod,
)


class Expandable(ABC):
    """Abstract class for expandable objects."""

    @abstractmethod
    def isExpanded(self):
        """Return True if this object is done expanding, False otherwise."""

    @abstractmethod
    def expandStep(self):
        """Perform a singular attepmt to expand something."""

    def tryExpand(self):
        if not self.isExpanded():
            self.expandStep()

    @abstractmethod
    def getResult(self):
        """Return expansion result. Can (but not obliged to) raise an exception if the object is not expanded yet."""
