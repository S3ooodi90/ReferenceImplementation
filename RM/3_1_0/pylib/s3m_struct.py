"""
Structural items.
"""
from abc import ABC, abstractmethod

from cuid import cuid
from validator_collection import checkers

from s3m_xdt import XdAnyType


class ItemType(ABC):
    """
    The abstract parent of ClusterType and XdAdapterType 
    structural representation types.
    """

    @abstractmethod
    def __init__(self):
        pass


class XdAdapterType(ItemType):
    """
    The leaf variant of Item, to which any XdAnyType subtype instance is 
    attached for use in a Cluster. 

    The unique ID for the adapter is part of the value (XdType).
    """

    def __init__(self):
        self._value = None

    @property
    def value(self):
        """
        The XdType contained in an XdAdapter.
        """
        return self._value

    @value.setter
    def value(self, v):
        if isinstance(v, XdAnyType) and self._value == None:
            self._value = v
            self._value.adapter = True
        else:
            raise ValueError("the value must be a XdAnyType subtype. A XdAdapter can only contain one XdType.")

    def __str__(self):
        return(self.__class__.__name__ + ', ID: ' + self.value.acuid + ' contains ' + str(self.value))

    def asXSD(self):
        """
        Return a XML Schema stub for the adapter.
        """
        indent = 2
        padding = ('').rjust(indent)
        xdstr = ''
        xdstr += padding.rjust(indent) + '\n<xs:element name="ms-' + self.value.acuid + '" substitutionGroup="s3m:Items" type="s3m:mc-' + self.value.acuid + '"/>\n'
        xdstr += padding.rjust(indent) + '<xs:complexType name="mc-' + self.value.acuid + '">\n'
        xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdAdapterType">\n'
        xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="unbounded" minOccurs="0" ref="s3m:ms-' + self.value.mcuid + '"/>\n'
        xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
        xdstr += padding.rjust(indent) + '</xs:complexType>\n\n'
        xdstr += self.value.asXSD()
        return(xdstr)


class ClusterType(ItemType):
    """
    The grouping component, which may contain further instances of itself or 
    any eXtended datatype, in an ordered list. 

    This component serves as the root component for arbitrarily complex 
    structures.
    """

    def __init__(self, label):
        """
        The semantic label (name of the model) is required.
        """
        self._mcuid = cuid()  # model cuid
        self._label = ''
        self._items = []

        if checkers.is_string(label, 2):
            self._label = label
        else:
            raise TypeError('"label" must be a string type and at least 2 characters long. Not a ', type(label))

    @property
    def label(self):
        """
        The semantic name of the ClusterType.
        """
        return self._label

    @property
    def mcuid(self):
        """
        The unique identifier of the component.
        """
        return self._mcuid

    @property
    def items(self):
        """
        The items contained in a Cluster.
        """
        return self._items

    @items.setter
    def items(self, v):
        if isinstance(v, ItemType):
            self._items.append(v)
        else:
            raise ValueError("items in a ClusterType must be of type ItemType.")

    def __str__(self):
        return(self.__class__.__name__ + ' : ' + self.label + ', ID: ' + self.mcuid)

    def asXSD(self):
        """
        Return a XML Schema stub for the Cluster.
        """
        indent = 2
        padding = ('').rjust(indent)
        xdstr = ''
        xdstr += padding.rjust(indent) + '\n<xs:element name="ms-' + self.mcuid + '" substitutionGroup="s3m:Items" type="s3m:mc-' + self.mcuid + '"/>\n'
        xdstr += padding.rjust(indent) + '<xs:complexType name="mc-' + self.mcuid + '">\n'
        xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:ClusterType">\n'
        xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + self.label.strip() + '"/>\n'
        for item in self.items:
            xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ms-' + item.value.acuid + '"/>\n'
        xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
        xdstr += padding.rjust(indent) + '</xs:complexType>\n\n'
        for item in self.items:
            xdstr += item.asXSD()

        return(xdstr)


