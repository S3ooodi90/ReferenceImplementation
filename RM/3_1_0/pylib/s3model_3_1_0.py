"""
Defines the S3Model RM XSD reference model in Python 3.7
"""
from datetime import datetime, date, time
from decimal import Decimal
from collections import OrderedDict
from abc import ABC, abstractmethod
from ab
from cuid import cuid
from validator_collection.checkers import is_url

import ontology


def units(units, mcuid):
    """
    Create XdStringType model as a Units component.
    units - a XdString object
    mcuid - the id of the containing object.
    """

    indent = 2
    padding = ('').rjust(indent)
    xdstr = padding.rjust(indent) + '<xs:complexType name="mc-' + unitsid + '">\n'
    xdstr += padding.rjust(indent + 2) + '<xs:annotation>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:documentation>\n'
    xdstr += padding.rjust(indent + 6) + 'Unit constraint for: ' + xml_escape(mcuid.strip()) + '\n'
    xdstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'
    xdstr += padding.rjust(indent + 6) + '<rdfs:Class rdf:about="mc-' + unitsid + '">\n'
    xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model_3_1_0.xsd#XdStringType"/>\n'
    xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
    xdstr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + quote(data[10].strip()) + '"/>\n'
    if data[11]:  # are there additional predicate-object definitions?
        for po in data[11].splitlines():
            pred = po.split()[0]
            obj = po[len(pred):].strip()
            xdstr += padding.rjust(indent + 8) + '<' + pred.strip() + ' rdf:resource="' + quote(obj.strip()) + '"/>\n'
    xdstr += padding.rjust(indent + 6) + '</rdfs:Class>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
    xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdStringType">\n'
    xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + data[1].strip() + ' Units"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ExceptionalValue"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vtb" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vte" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="tr" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="modified" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1"  name="xdstring-value" type="xs:string" fixed="' + data[12].strip() + '"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="xdstring-language" type="xs:language" default="en-US"/>\n'
    xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    xdstr += padding.rjust(indent) + '</xs:complexType>\n'

    return(xdstr)


class ExceptionalValue(ABC):
    """
    Subtypes are used to indicate why a value is missing (Null) or is outside a measurable range.
    The element ev-name is fixed in restricted types to a descriptive string. The subtypes defined in the reference model
    are considered sufficiently generic to be useful in many instances.
    Data Models may contain additional ExceptionalValueType restrictions to allow for domain related reasons for
    errant or missing data.
    """

    @abstractmethod
    def __init__(self):
        self._ev_name = ''

    @property
    @abstractmethod
    def ev_name(self):
        """
        A short title or phase for the exceptional type value.
        """
        return self._ev_name


# class NIType(ExceptionalValue):
# """
# No Information : The value is exceptional (missing, omitted, incomplete, improper).
# No information as to the reason for being an exceptional value is provided.
# This is the most general exceptional value. It is also the default exceptional value implemented in tools.
# """
# ev_name: str = field(default='No Information', metadata={'min': 1, 'max': 1})


# class MSKType(ExceptionalValue):
# """
# Masked : There is information on this item available but it has not been provided by the sender due to security,
# privacy or other reasons. There may be an alternate mechanism for gaining access to this information.
# Warning: Using this exceptional value does provide information that may be a breach of confidentiality,
# even though no detail data is provided. Its primary purpose is for those circumstances where it is necessary to
# inform the receiver that the information does exist without providing any detail.
# """
# ev_name: str = field(default='Masked', metadata={'min': 1, 'max': 1})


# class INVType(ExceptionalValue):
# """
# Invalid : The value as represented in the instance is not a member of the set of permitted data values in the
# constrained value domain of a variable.
# """
# ev_name: str = field(default='Invalid', metadata={'min': 1, 'max': 1})


# class DERType(ExceptionalValue):
# """
# Derived : An actual value may exist, but it must be derived from the provided information;
# usually an expression is provided directly.
# """
# ev_name: str = field(default='Derived', metadata={'min': 1, 'max': 1})


# class UNCType(ExceptionalValue):
# """
# Unencoded : No attempt has been made to encode the information correctly but the raw source information is represented, usually in free text.
# """
# ev_name: str = field(default='Unencoded', metadata={'min': 1, 'max': 1})


# class OTHType(ExceptionalValue):
# """
# Other: The actual value is not a member of the permitted data values in the variable.
# (e.g., when the value of the variable is not by the coding system)
# """
# ev_name: str = field(default='Other', metadata={'min': 1, 'max': 1})


# class NINFType(ExceptionalValue):
# """
# Negative Infinity : Negative infinity of numbers
# """
# ev_name: str = field(default='Negative Infinity', metadata={'min': 1, 'max': 1})


# class PINFType(ExceptionalValue):
# """
# Positive Infinity : Positive infinity of numbers
# """
# ev_name: str = field(default='Positive Infinity', metadata={'min': 1, 'max': 1})


# class UNKType(ExceptionalValue):
# """
# Unknown : A proper value is applicable, but not known.
# """
# ev_name: str = field(default='Unknown', metadata={'min': 1, 'max': 1})


# class ASKRType(ExceptionalValue):
# """
# Asked and Refused : Information was sought but refused to be provided (e.g., patient was asked but refused to answer).
# """
# ev_name: str = field(default='Asked and Refused', metadata={'min': 1, 'max': 1})


# class NASKType(ExceptionalValue):
# """
# Not Asked : This information has not been sought (e.g., patient was not asked)
# """
# ev_name: str = field(default='Not Asked', metadata={'min': 1, 'max': 1})


# class QSType(ExceptionalValue):
# """
# Sufficient Quantity : The specific quantity is not known, but is known to non-zero and it is not specified because it makes up the bulk of the material;
# Add 10mg of ingredient X, 50mg of ingredient Y and sufficient quantity of water to 100mL.
# """
# ev_name: str = field(default='Sufficient Quantity', metadata={'min': 1, 'max': 1})


# class TRCType(ExceptionalValue):
# """
# Trace : The content is greater or less than zero but too small to be quantified.
# """
# ev_name: str = field(default='Trace', metadata={'min': 1, 'max': 1})


# class ASKUType(ExceptionalValue):
# """
# Asked but Unknown : Information was sought but not found (e.g., patient was asked but did not know)
# """
# ev_name: str = field(default='Asked but Unknown', metadata={'min': 1, 'max': 1})


# class NAVType(ExceptionalValue):
# """
# Not Available: This information is not available and the specific reason is not known.
# """
# ev_name: str = field(default='Not Available', metadata={'min': 1, 'max': 1})


# class NAType(ExceptionalValue):
# """
# Not Applicable : No proper value is applicable in this context e.g.,the number of cigarettes smoked per day by a non-smoker subject.
# """
# ev_name: str = field(default='Not Applicable', metadata={'min': 1, 'max': 1})


class XdAnyType(ABC):
    """
    Serves as an abstract common ancestor of all eXtended data-types (Xd*) in S3Model.
    """

    @abstractmethod
    def __init__(self, label):
        self.mcuid = cuid()  # model cuid
        self.acuid = cuid()  # adapter cuid
        if isinstance(label, str):
            if len(label) > 1:
                self.label = label
            else:
                raise ValueError('label must be at least 2 characters in length')
        else:
            raise TypeError('"label" must be a string type. Not a ', type(label))

        self._adapter = True  # flag set to create an XdAdapter
        self._docs = None
        self._definition_url = None
        self._pred_obj_list = None

        # initially non-required elements are None until they are assigned.
        self._act = None
        self._ev = None
        self._vtb = None
        self._vte = None
        self._tr = None
        self._modified = None
        self._latitude = None
        self._longitude = None

    @property
    @abstractmethod
    def docs(self):
        """
        The documentation string.
        """
        return self._docs

    @docs.setter
    @abstractmethod
    def doc(self, v):
        if isinstance(v, str):
            self._docs = v
        else:
            raise ValueError("the Documentation value must be a string.")

    @property
    @abstractmethod
    def pred_obj_list(self):
        """
        A list of additional predicate object pairs to describe the component.
        """
        return self._pred_obj_list

    @pred_obj_list.setter
    @abstractmethod
    def pred_obj_list(self, v):
        if isinstance(v, list):
            self._pred_obj_list = v
        else:
            raise ValueError("the Predicate Object List value must be a list of strings.")

    @property
    @abstractmethod
    def definition_url(self):
        """
        The primary definition URL for the component.
        """
        return self._definition_url

    @definition_url.setter
    @abstractmethod
    def definition_url(self, v):
        if is_url(v):
            self._definition_url = v
        else:
            raise ValueError("the Definition URL value must be a valid URL.")

    @property
    @abstractmethod
    def act(self):
        """
        Access Control Tag. If this is used it must contain a valid term from the Access Control System linked 
        to by the containing Data Model.
        """
        return self._act

    @act.setter
    @abstractmethod
    def act(self, v):
        if isinstance(v, str):
            self._act = v
        else:
            raise ValueError("the Access Control Tag value must be a string.")

    @property
    @abstractmethod
    def ev(self):
        """
        In an invalid instance, the application can indicate here why data is missing or invalid. 
        The sub-types are based on ISO 21090 NULL Flavors entries, with additions noted from real-world usage.
        """
        return self._ev

    @ev.setter
    @abstractmethod
    def ev(self, v):
        if isinstance(v, ExceptionalValue):
            self._ev = v
        else:
            raise ValueError("the ev value must be an ExceptionalValue.")

    @property
    @abstractmethod
    def vtb(self):
        """
        Valid Time Begin. If present this must be a valid datetime including timezone. 
        It is used to indicate the beginning time that information is considered valid.
        """
        return self._vtb

    @vtb.setter
    @abstractmethod
    def vtb(self, v):
        if isinstance(v, datetime):
            self._vtb = v
        else:
            raise ValueError("the Valid Time Begin value must be a datetime.")

    @property
    @abstractmethod
    def vte(self):
        """
        Valid Time End. If present this must be a valid date-time including timezone. 
        It is used to indicate the ending time that information is considered valid or the time the information expired or 
        will expire.
        """
        return self._vte

    @vte.setter
    @abstractmethod
    def vte(self, v):
        if isinstance(v, datetime):
            self._vte = v
        else:
            raise ValueError("the Valid Time End value must be a datetime.")

    @property
    @abstractmethod
    def tr(self):
        """
        Time Recorded. If present this must be a valid date-time. 
        It is used to indicate the the actual date and time the data was recorded.
        """
        return self._tr

    @tr.setter
    @abstractmethod
    def tr(self, v):
        if isinstance(v, datetime):
            self._tr = v
        else:
            raise ValueError("the Time Recorded value must be a datetime.")

    @property
    @abstractmethod
    def modified(self):
        """
        Time Modified. If present this must be a valid date-time stamp. 
        It is used to indicate the the actual date and time the data was last changed.
        """
        return self._modified

    @modified.setter
    @abstractmethod
    def modified(self, v):
        if isinstance(v, datetime):
            self._modified = v
        else:
            raise ValueError("the Modified value must be a datetime.")

    @property
    @abstractmethod
    def latitude(self):
        """
        Latitude in decimal format. Value range -90.000000 to 90.000000.
        """
        return self._latitude

    @latitude.setter
    @abstractmethod
    def latitude(self, v):
        if isinstance(v, Decimal) and (-90.00 >= v <= 90.00):
            self._latitude = v
        else:
            raise ValueError("the Latitude value must be a decimal between -90.00 and 90.00.")

    @property
    @abstractmethod
    def longitude(self):
        """
        Longitude in decimal format. Value range -180.000000 to 180.000000.
        """
        return self._longitude

    @longitude.setter
    @abstractmethod
    def longitude(self, v):
        if isinstance(v, Decimal) and (-180.00 >= v <= 180.00):
            self._latitude = v
        else:
            raise ValueError("the Longitude value must be a decimal between -180.00 and 180.00.")

    def __str__(self):
        return(self.__class__.__name__ + ' : ' + self.label + ', ID: ' + self.mcuid)


# class InvlUnits(XdAnyType):
    # """
    # The units designation for an Interval is slightly different than other complexTypes. This complexType is composed of a units name and a URI because in a ReferenceRange parent there can be different units for different ranges. Example: A XdQuantity of
    # temperature can have a range in degrees Fahrenheit and one in degrees Celsius. The derived complexType in the CMC has these values fixed by the modeler.
    # """
    # units_name: str = field(default=None, metadata={'min': 1, 'max': 1, 'lang': 'en-US'})
    # units_uri: str = field(default=None, metadata={'min': 1, 'max': 1})


# class XdIntervalType(XdAnyType):
    # """
    # Generic type defining an interval (i.e. range) of a comparable type. An interval is a contiguous subrange of a
    # comparable base type. Used to define intervals of dates, times, quantities, etc. Whose datatypes are the same and
    # are ordered. In S3Model, they are primarily used in defining reference ranges. The type of upper and lower must be set in the DM.
    # """
    # lower: Any = field(default=None, metadata={'min': 0, 'max': 1})
    # upper: Any = field(default=None, metadata={'min': 0, 'max': 1})
    # lower_included: bool = field(default=None, metadata={'min': 1, 'max': 1})
    # upper_included: bool = field(default=None, metadata={'min': 1, 'max': 1})
    # lower_bounded: bool = field(default=None, metadata={'min': 1, 'max': 1})
    # upper_bounded: bool = field(default=None, metadata={'min': 1, 'max': 1})
    # interval_units: InvlUnits = field(default=None, metadata={'min': 1, 'max': 1})


# class ReferenceRangeType(XdAnyType):
    # """
    # Defines a named range to be associated with any ORDERED datum. Each such range is sensitive to the context,
    # e.g. sex, age, location, and any other factor which affects ranges.
    # May be used to represent high, low, normal, therapeutic, dangerous, critical, etc. ranges that are constrained by an interval.
    # """
    # definition: str = field(default=None, metadata={'min': 1, 'max': 1})
    # interval: XdIntervalType = field(default=None, metadata={'min': 1, 'max': 1})
    # is_normal: bool = field(default=None, metadata={'min': 1, 'max': 1})


class XdBooleanType(XdAnyType):
    """
    An enumerated type which represents boolean decisions. Such as true/false or yes/no answers. 
    Useful where it is essential to devise the meanings (often questions in subjective data) carefully so that 
    the only allowed result values result in one the options; true or false but are presented to the user as a list of options. 

    The possible choices for True or False are values in a dictionary. 
    The class defines 'true-value' and 'false-value'. 
    The instance implementation is restricted to only have a value for one of them based on the user choice from options..

    The XdBooleanType should not be used as a replacement for enumerated choice types such as male/female, or similar choice sets. 
    Such values should be modeled as XdStrings with enumerations and may reference a controlled vocabulary. 
    In any case, the choice set often has more than two values.
    """

    def __init__(self, label, options):
        super().__init__(label)
        self.true_value = None
        self.false_value = None
        if isinstance(options, dict):
            k = options.keys()
            if len(k) == 2 and 'trues' in k and 'falses' in k:
                for x in k:
                    if not isinstance(options[x], list):
                        raise ValueError("Values in the options dictionary must be lists.", options[x])

                self.options = options
            else:
                raise ValueError('XdBoolean options dictionary has invalid keys. They should be "trues" and "falses", not ', k)
        else:
            raise TypeError('XdBoolean options must be a dictionary. Not ', type(options))

    def __str__(self):
        return(self.__class__.__name__ + ' : ' + self.label + ', ID: ' + self.mcuid + '\n' + str(self.options) + '\n')

    def asXSD(self):
        """
        Return a XML Schema complexType definition.
        """
        indent = 2
        padding = ('').rjust(indent)
        xdstr = ''
        if self.adapter:
            xdstr += padding.rjust(indent) + '\n<xs:element name="ms-' + self.acuid + '" substitutionGroup="s3m:Items" type="s3m:mc-' + self.acuid + '"/>\n'
            xdstr += padding.rjust(indent) + '<xs:complexType name="mc-' + self.acuid + '">\n'
            xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
            xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdAdapterType">\n'
            xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
            xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="unbounded" minOccurs="0" ref="s3m:ms-' + self.mcuid + '"/>\n'
            xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
            xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
            xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
            xdstr += padding.rjust(indent) + '</xs:complexType>\n'

        xdstr += padding.rjust(indent) + '<xs:element name="ms-' + self.mcuid + '" substitutionGroup="s3m:XdAdapter-value" type="s3m:mc-' + self.mcuid + '"/>\n'
        xdstr += padding.rjust(indent) + '<xs:complexType name="mc-' + self.mcuid + '">\n'
        xdstr += padding.rjust(indent + 2) + '<xs:annotation>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:documentation>\n'
        xdstr += padding.rjust(indent + 6) + xml_escape(self.docs.strip()) + '\n'
        xdstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'

        # add RDF
        xdstr += padding.rjust(indent + 6) + '<rdfs:Class rdf:about="mc-' + self.mcuid + '">\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model_3_1_0.xsd#XdBooleanType"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + quote(self.definition_url.strip()) + '"/>\n'
        if self.pred_obj_list:  # are there additional predicate-object definitions?
            text = os.linesep.join([s for s in self.pred_obj_list.splitlines() if s])  # remove empty lines
            for po in text.splitlines():
                pred = po.split()[0]
                obj = po[len(pred):].strip()
                xdstr += padding.rjust(indent + 8) + '<' + pred.strip() + ' rdf:resource="' + quote(obj.strip()) + '"/>\n'

        xdstr += padding.rjust(indent + 6) + '</rdfs:Class>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
        xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdBooleanType">\n'
        xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + self.label.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="act" type="xs:string" default="' + self.act.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ExceptionalValue"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vtb" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vte" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="tr" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="modified" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="latitude" type="xs:decimal"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="longitude" type="xs:decimal"/>\n'
        xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
        xdstr += padding.rjust(indent) + '</xs:complexType>\n'

        return(xdstr)


# class XdLinkType(XdAnyType):
    # """
    # Used to specify a Universal Resource Identifier. Set the pattern facet to accommodate your needs in the DM. Intended use is to provide a mechanism that can be used to link together Concept Models. The relation element allows for the use of a descriptive
    # term for the link with an optional URI pointing to the source vocabulary. In most usecases the modeler will define all three of these using the 'fixed' attribute. Other usecases will have the 'relation' and 'relation-uri' elements fixed and the application will provide the 'link-value'.
    # """
    # link: str = field(default=None, metadata={'min': 1, 'max': 1})
    # relation: str = field(default=None, metadata={'min': 1, 'max': 1})
    # relation_uri: str = field(default=None, metadata={'min': 0, 'max': 1})


# class XdStringType(XdAnyType):
    # """
    # The string data type can contain characters, line feeds, carriage returns, and tab characters. The use cases are for any free form text entry or for any enumerated lists. Additionally the minimum and maximum lengths may be set and regular expression patterns  may be specified.
    # """
    # xdstring_value: str = field(default=None, metadata={'min': 0, 'max': 1})
    # xdstring_language: str = field(default=None, metadata={'min': 0, 'max': 1})


# class XdFileType(XdAnyType):
    # """
    # A type to use for encapsulated content (aka. files) for image, audio and other media types with a defined MIME type. This type provides a choice of embedding the content into the data or using a URL to point to the content.
    # """
    # size: int = field(default=None, metadata={'min': 1, 'max': 1})
    # encoding: str = field(default=None, metadata={'min': 0, 'max': 1})
    # xdfile_language: str = field(default=None, metadata={'min': 0, 'max': 1})
    # formalism: str = field(default=None, metadata={'min': 0, 'max': 1})
    # media_type: str = field(default=None, metadata={'min': 0, 'max': 1})
    # compression_type: str = field(default=None, metadata={'min': 0, 'max': 1})
    # hash_result: str = field(default=None, metadata={'min': 0, 'max': 1})
    # hash_function: str = field(default=None, metadata={'min': 0, 'max': 1})
    # alt_txt: str = field(default=None, metadata={'min': 0, 'max': 1})
    # choice of uri or media_content
    # uri: str = field(default=None, metadata={'min': 1, 'max': 1})
    # media_content: bytes = field(default=None, metadata={'min': 1, 'max': 1})


# class XdOrderedType(XdAnyType):
    # """
    # Serves as an abstract common ancestor of all ordered types
    # """
    # referencerange: ReferenceRangeType = field(default=None, metadata={'min': 0, 'max': 1})
    # normal_status: str = field(default=None, metadata={'min': 0, 'max': 1})


# class XdOrdinalType(XdOrderedType):
    # """
    # Models rankings and scores, e.g., pain, Apgar values, educational level, and the Likert Scale where there is;

        # * implied ordering,
        # * no implication that the distance between each value is constant, and
        # * the total number of values is finite.

        # Note that the term ‘ordinal’ in mathematics means natural numbers only. In this case, any decimal is allowed since negative, and zero values are used by medical and other professionals for centering values around a neutral point. Also, decimal values are sometimes used such as 0.5 or .25

        # Examples of sets of ordinal values are;

        # * -3, -2, -1, 0, 1, 2, 3 -- reflex response values
        # * 0, 1, 2 -- Apgar values

        # Also used for recording any clinical or other data which is customarily recorded using symbolic values. Examples;

        # * the results on a urinalysis strip, e.g. {neg, trace, +, ++, +++} are used for leukocytes, protein, nitrites etc;
        # * for non-haemolysed blood {neg, trace, moderate};
        # * for haemolysed blood {neg, trace, small, moderate, large}.

        # Elements *ordinal* and *symbol* MUST have the same number of enumerations in the RMC.
    # """
    # ordinal: Decimal = field(default=None, metadata={'min': 1, 'max': 1})
    # symbol: str = field(default=None, metadata={'min': 1, 'max': 1})


# class XdQuantifiedType(XdOrderedType):
    # """
    # Serves as an abstract common ancestor of all quantifiable types
    # """
    # constrained to list [None,'equal','less_than', 'greater_than', 'less_than_or_equal', 'greater_than_or_equal', 'approximate']
    # magnitude_status: str = field(default=None, metadata={'min': 0, 'max': 1})
    # error: int = field(default=None, metadata={'min': 0, 'max': 1})
    # accuracy: Decimal = field(default=None, metadata={'min': 0, 'max': 1})


# class XdCountType(XdQuantifiedType):
    # """
    # Countable quantities. Used for countable types such as pregnancies and steps (taken by a physiotherapy patient), number of cigarettes smoked in a day, etc. The thing(s) being counted must be represented in the units element. Misuse:Not used for amounts of physical entities (which all have standardized units).
    # """
    # xdcount_value: int = field(default=None, metadata={'min': 0, 'max': 1})
    # xdcount_units: XdStringType = field(default=None, metadata={'min': 1, 'max': 1})


# class XdQuantityType(XdQuantifiedType):
    # """
    # Quantified type representing specific quantities, i.e. quantities expressed as a magnitude and units. Can also be used for time durations, where it is more convenient to treat these as simply a number of individual seconds, minutes, hours, days, months, years, etc. when no temporal calculation is to be performed.
    # """
    # xdquantity_value: int = field(default=None, metadata={'min': 0, 'max': 1})
    # xdquantity_units: XdStringType = field(default=None, metadata={'min': 1, 'max': 1})


# class XdFloatType(XdQuantifiedType):
    # """
    # Quantified type representing specific a value as a floating point number and optional units.
    # """
    # xdfloat_value: float = field(default=None, metadata={'min': 0, 'max': 1})
    # xdfloat_units: XdStringType = field(default=None, metadata={'min': 1, 'max': 1})


# class XdRatioType(XdQuantifiedType):
    # """
    # Models a ratio of values, i.e. where the numerator and denominator are both pure numbers. Should not be used to represent things like blood pressure which are often written using a ‘/’ character, giving the misleading impression that the item is a ratio,
    # when in fact it is a structured value. Similarly, visual acuity, often written as (e.g.) “20/20” in clinical notes is not a ratio but an ordinal (which includes non-numeric symbols like CF = count fingers etc). Should not be used for formulations. Used for modeling; ratios, rates or proportions.
    # """
    # constrained to list ['ratio','rate', 'proportion']
    # ratio_type: str = field(default=None, metadata={'min': 1, 'max': 1})
    # numerator: float = field(default=None, metadata={'min': 0, 'max': 1})
    # denominator: float = field(default=None, metadata={'min': 0, 'max': 1})
    # xdratio_value: float = field(default=None, metadata={'min': 0, 'max': 1})
    # numerator_units: XdStringType = field(default=None, metadata={'min': 0, 'max': 1})
    # denominator_units: XdStringType = field(default=None, metadata={'min': 0, 'max': 1})
    # xdratio_units: XdStringType = field(default=None, metadata={'min': 0, 'max': 1})


# class XdTemporalType(XdOrderedType):
    # """
    # Type defining the concept of date and time types. Must be constrained in DMs to be one or more of the below elements. This gives the modeler the ability to optionally allow full or partial dates at run time. Setting both maxOccurs and minOccurs to zero cause the element to be prohibited.
    # """
    # TODO: fix the types
    # xdtemporal_date: date = field(default=None, metadata={'min': 0, 'max': 1})
    # xdtemporal_time: time = field(default=None, metadata={'min': 0, 'max': 1})
    # xdtemporal_datetime: datetime = field(default=None, metadata={'min': 0, 'max': 1})
    # xdtemporal_day: date = field(default=None, metadata={'min': 0, 'max': 1})
    # xdtemporal_month: date = field(default=None, metadata={'min': 0, 'max': 1})
    # xdtemporal_year: date = field(default=None, metadata={'min': 0, 'max': 1})
    # xdtemporal_year_month: date = field(default=None, metadata={'min': 0, 'max': 1})
    # xdtemporal_month_day: date = field(default=None, metadata={'min': 0, 'max': 1})
    # xdtemporal_duration: date = field(default=None, metadata={'min': 0, 'max': 1})


# class ItemType(object):
    # """
    # The abstract parent of ClusterType and XdAdapterType structural representation types.
    # """
    # mcuid: str = field(default_factory=cuid, init=False)


# class XdAdapterType(ItemType):
    # """
    # The leaf variant of Item, to which any XdAnyType subtype instance is attached for use in a Cluster.
    # """
    # XdAdapter_value: XdAnyType = field(default=None, metadata={'min': 0, 'max': 100})  # max is technically unbounded however a proactical limit is well under 100


# class ClusterType(ItemType):
    # """
    # The grouping component, which may contain further instances of itself or any eXtended datatype, in an ordered list. This can serve as the root component for arbitrarily complex structures.
    # """
    # label: str = field(metadata={'min': 1, 'max': 1})
    # items: ItemType = field(default=None, metadata={'min': 0, 'max': 100}, repr=False)  # max is technically unbounded however a proactical limit is well under 100


# class PartyType(object):
    # """
    # Description of a party, including an optional external link to data for this party in a demographic or other identity management system. An additional details element provides for the inclusion of information related to this party directly. If the party
    # information is to be anonymous then do not include the details element.
    # """
    # mcuid: str = field(default_factory=cuid, init=False)
    # label: str = field(default=None, metadata={'min': 1, 'max': 1})
    # party_name: str = field(default=None, metadata={'min': 0, 'max': 1})
    # party_ref: XdLinkType = field(default=None, metadata={'min': 0, 'max': 1})
    # party_details: ClusterType = field(default=None, metadata={'min': 0, 'max': 1})


# class AuditType(object):
    # """
    # AuditType provides a mechanism to identify the who/where/when tracking of instances as they move from system to system.
    # """
    # mcuid: str = field(default_factory=cuid, init=False)
    # label: str = field(default=None, metadata={'min': 1, 'max': 1})
    # system_id: XdStringType = field(default=None, metadata={'min': 0, 'max': 1})
    # system_user: PartyType = field(default=None, metadata={'min': 0, 'max': 1})
    # location: ClusterType = field(default=None, metadata={'min': 0, 'max': 1})
    # timestamp: datetime = field(default=None, metadata={'min': 1, 'max': 1})


# class AttestationType(object):
    # """
    # Record an attestation by a party of the DM content. The type of attestation is recorded by the reason attribute, which my be coded.
    # """
    # mcuid: str = field(default_factory=cuid, init=False)
    # label: str = field(default=None, metadata={'min': 1, 'max': 1})
    # view: XdFileType = field(default=None, metadata={'min': 0, 'max': 1})
    # proof: XdFileType = field(default=None, metadata={'min': 0, 'max': 1})
    # reason: XdStringType = field(default=None, metadata={'min': 0, 'max': 1})
    # committer: PartyType = field(default=None, metadata={'min': 0, 'max': 1})
    # committed: datetime = field(default=None, metadata={'min': 0, 'max': 1})
    # pending: bool = field(default=None, metadata={'min': 1, 'max': 1})


# class ParticipationType(object):
    # """
    # Model of a participation of a Party (any Actor or Role) in an activity. Used to represent any participation of a Party in some activity, which is not explicitly in the model, e.g. assisting nurse. Can be used to record past or future participations.
    # """
    # mcuid: str = field(default_factory=cuid, init=False)
    # label: str = field(default=None, metadata={'min': 1, 'max': 1})
    # performer: PartyType = field(default=None, metadata={'min': 0, 'max': 1})
    # function: XdStringType = field(default=None, metadata={'min': 0, 'max': 1})
    # mode: XdStringType = field(default=None, metadata={'min': 0, 'max': 1})
    # start: datetime = field(default=None, metadata={'min': 0, 'max': 1})
    # end: datetime = field(default=None, metadata={'min': 0, 'max': 1})


# class DMType(object):
    # """
    # This is the root node of a Data Model (DM)
    # """

    # def __init__(self):
        #self.mcuid = cuid()
        #self.metadata = self.genMD()
        #self.data = ClusterType()
        #self.label = self.metadata['title']
        #self.dm_language = self.metadata['language']
        #self.dm_encoding = 'utf-8'
        #self.current_state = ''
        #self.subject = None
        #self.provider = None
        #self.participations = list()
        #self.protocol = None
        #self.workflow = None
        #self.acs = None
        #self.audits = list()
        #self.attestations = list()
        #self.links = list()

    # def __str__(self):
        # return("S3Model Data Model\n" + "ID: " + self.mcuid + "\n" + self.showMetadata(self.metadata))

    # def showMetadata(self):
        #mdStr = ''
        # for k, v in self.metadata.items():
        #mdStr += k + ': ' + repr(v) + '\n'
        # return(mdStr)

    # def genMD(self):
        # """
        # Create a metadata dictionary for the DM if one isn't passed in.
        # """
        #md = OrderedDict()
        #md['title'] = 'New Data Model'
        #md['creator'] = 'Joe Smith'
        #md['subject'] = 'S3M DM'
        #md['rights'] = 'Creative Commons'
        #md['relation'] = 'None'
        #md['coverage'] = 'Global'
        #md['type'] = 'S3Model Data Model (DM)'
        #md['identifier'] = 'dm-' + self.mcuid
        #md['description'] = 'Needs a description'
        #md['publisher'] = 'Data Insights, Inc.'
        #md['date'] = '{0:%Y-%m-%dT%H:%M:%S}'.format(datetime.now())
        #md['format'] = 'text/xml'
        #md['language'] = 'en-US'

        # return(md)
