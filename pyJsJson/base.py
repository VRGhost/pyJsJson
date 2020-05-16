"""Base classes."""
from abc import (
    ABC,
    abstractmethod,
)

from . import exceptions

class Expandable(ABC):
    """Abstract class for expandable objects."""

    def __init__(self, expansion_loop):
        self.expansion_loop = expansion_loop
        self.expansion_loop.add(self) # Registed with the expansion loop.

    @abstractmethod
    def expandStep(self):
        """Perform a singular attepmt to expand something."""

    @abstractmethod
    def dependsOn(self):
        """Returns a list of Expandable objects that this object is waiting for."""

    def isExpanded(self):
        for child in self.dependsOn():
            if not child.isExpanded():
                return False
        return True

    def tryExpand(self):
        if not self.isExpanded():
            self.expandStep()

    @abstractmethod
    def getResult(self):
        """Return expansion result. Can (but not obliged to) raise an exception if the object is not expanded yet."""


class ExpandableData(Expandable):
    """An expandable object that holds a piece of input data."""

    def getInputData(self):
        return self.__data

    def setInputData(self, value):
        try:
            self.__data
        except AttributeError:
            # All is well - the data was not yet provided.
            self.__data = value
        else:
            raise exceptions.PyJsJsonException("This object had already been seeded with data")
        self.onDataSet()

    def onDataSet(self):
        """A method for child classes to override any processing done on the input data being set."""