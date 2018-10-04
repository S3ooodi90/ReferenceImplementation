"""
Structural items.
"""
from abc import ABC, abstractmethod


class ItemType(ABC):
    """
    The abstract parent of ClusterType and XdAdapterType structural representation types.
    """

    @abstractmethod
    def __init__(self, label):
        self._mcuid = cuid()  # model cuid
        self._label = ''

        if checkers.is_string(label, 2):
            self._label = label
        else:
            raise TypeError('"label" must be a string type and at least 2 characters long. Not a ', type(label))

    @property
    def label(self):
        """
        The semantic name of the component.
        """
        return self._label

    def __str__(self):
        return(self.__class__.__name__ + ' : ' + self.label + ', ID: ' + self.mcuid)


class XdAdapterType(ItemType):
    """
    The leaf variant of Item, to which any XdAnyType subtype instance is attached for use in a Cluster.
    """

    def __init__(self, label):
        """
        The semantic label (name of the model) is required.
        """
        super().__init__(label)

        self._XdAdapter_value = None


class ClusterType(ItemType):
    """
    The grouping component, which may contain further instances of itself or any eXtended datatype, in an ordered list. This can serve as the root component for arbitrarily complex structures.
    """

    def __init__(self, label):
        """
        The semantic label (name of the model) is required.
        """
        super().__init__(label)

        self._items = None


