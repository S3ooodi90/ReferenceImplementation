"""
Defines the S3Model reference model in Python 3.7
Version 3.1.0
This implementation is not a strict model of the RM. It also contains functionality to manage constraints that are
built into the XML Schema parsers. 
"""
import re
from datetime import datetime, date, time, timedelta
from decimal import Decimal
from collections import OrderedDict
from abc import ABC, abstractmethod
from xml.sax.saxutils import escape
from urllib.parse import quote
from base64 import b64encode
from typing import ByteString

from cuid import cuid
from validator_collection import checkers
import ontology

invlTypes = [int, Decimal, float, date, time, datetime, timedelta]


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
    def ev_name(self):
        """
        A short title or phase for the exceptional type value.
        """
        return self._ev_name

    def __str__(self):
        return(self.__class__.__name__ + ' : ' + self._ev_name)


class NIType(ExceptionalValue):
    """
    No Information : The value is exceptional (missing, omitted, incomplete, improper).
    No information as to the reason for being an exceptional value is provided.
    This is the most general exceptional value. It is also the default exceptional value implemented in tools.
    """

    def __init__(self):
        self._ev_name = 'No Information'


class MSKType(ExceptionalValue):
    """
    Masked : There is information on this item available but it has not been provided by the sender due to security,
    privacy or other reasons. There may be an alternate mechanism for gaining access to this information.
    Warning: Using this exceptional value does provide information that may be a breach of confidentiality,
    even though no detail data is provided. Its primary purpose is for those circumstances where it is necessary to
    inform the receiver that the information does exist without providing any detail.
    """

    def __init__(self):
        self._ev_name = 'Masked'


class INVType(ExceptionalValue):
    """
    Invalid : The value as represented in the instance is not a member of the set of permitted data values in the
    constrained value domain of a variable.
    """

    def __init__(self):
        self._ev_name = 'Invalid'


class DERType(ExceptionalValue):
    """
    Derived : An actual value may exist, but it must be derived from the provided information;
    usually an expression is provided directly.
    """

    def __init__(self):
        self._ev_name = 'Derived'


class UNCType(ExceptionalValue):
    """
    Unencoded : No attempt has been made to encode the information correctly but the raw source information is represented, usually in free text.
    """

    def __init__(self):
        self._ev_name = 'Unencoded'


class OTHType(ExceptionalValue):
    """
    Other: The actual value is not a member of the permitted data values in the variable.
    (e.g., when the value of the variable is not by the coding system)
    """

    def __init__(self):
        self._ev_name = 'Other'


class NINFType(ExceptionalValue):
    """
    Negative Infinity : Negative infinity of numbers
    """

    def __init__(self):
        self._ev_name = 'Negative Infinity'


class PINFType(ExceptionalValue):
    """
    Positive Infinity : Positive infinity of numbers
    """

    def __init__(self):
        self._ev_name = 'Positive Infinity'


class UNKType(ExceptionalValue):
    """
    Unknown : A proper value is applicable, but not known.
    """

    def __init__(self):
        self._ev_name = 'Unknown'


class ASKRType(ExceptionalValue):
    """
    Asked and Refused : Information was sought but refused to be provided (e.g., patient was asked but refused to answer).
    """

    def __init__(self):
        self._ev_name = 'Asked and Refused'


class NASKType(ExceptionalValue):
    """
    Not Asked : This information has not been sought (e.g., patient was not asked)
    """

    def __init__(self):
        self._ev_name = 'Not Asked'


class QSType(ExceptionalValue):
    """
    Sufficient Quantity : The specific quantity is not known, but is known to non-zero and it is not specified because it makes up the bulk of the material;
    Add 10mg of ingredient X, 50mg of ingredient Y and sufficient quantity of water to 100mL.
    """

    def __init__(self):
        self._ev_name = 'Sufficient Quantity'


class TRCType(ExceptionalValue):
    """
    Trace : The content is greater or less than zero but too small to be quantified.
    """

    def __init__(self):
        self._ev_name = 'Trace'


class ASKUType(ExceptionalValue):
    """
    Asked but Unknown : Information was sought but not found (e.g., patient was asked but did not know)
    """

    def __init__(self):
        self._ev_name = 'Asked but Unknown'


class NAVType(ExceptionalValue):
    """
    Not Available: This information is not available and the specific reason is not known.
    """

    def __init__(self):
        self._ev_name = 'Not Available'


class NAType(ExceptionalValue):
    """
    Not Applicable : No proper value is applicable in this context e.g.,the number of cigarettes smoked per day by a non-smoker subject.
    """

    def __init__(self):
        self._ev_name = 'Not Applicable'


class XdAnyType(ABC):
    """
    Serves as an abstract common ancestor of all eXtended data-types (Xd*) in S3Model.
    """

    @abstractmethod
    def __init__(self, label):
        self._mcuid = cuid()  # model cuid
        self._acuid = cuid()  # adapter cuid
        self._label = ''

        if checkers.is_string(label, minimum_length=2):
            self._label = label
        else:
            raise TypeError('"label" must be a string type of at least 2 characters. Not a ', type(label))

        self._adapter = True  # flag set to create an XdAdapter for use in a Cluster
        self._docs = ''
        self._definition_url = ''
        self._pred_obj_list = []
        self._act = ''
        self._ev = None
        self._vtb = None
        self._vte = None
        self._tr = None
        self._modified = None
        self._latitude = None
        self._longitude = None
        self._cardinality = {'act': (0, 1), 'ev': (0, None), 'vtb': (0, 1), 'vte': (0, 1), 'tr': (0, 1), 'modified': (0, 1), 'location': (0, 1)}

    @property
    def cardinality(self):
        """
        The cardinality status values. 
        The setter method can be called by each subclass to add cardinality values for each element or change 
        the defaults. Some elements cardinality is not changed. Ex: XdBoolean elements are not modifiable.
        The dictionary uses a string representation of each property name and a tuple as the value.
        The tuple passed into the setter is a tuple with v[0] as a string and v[1] as a tuple containing an
        integer set representing the (minimum, maximum) values. Ex: ('vtb', (1,1)) would set the vtb value to be required.
        The Python value of 'None' represents the 'unbounded' XML Schema value. 
        NOTE: The cardinality for latitude and longitude are combined into one called 'location'.
        """
        return self._cardinality

    @cardinality.setter
    def cardinality(self, v):
        if checkers.is_iterable(v) and len(v) == 2 and isinstance(v[0], str) and isinstance(v[1], tuple):
            if isinstance(v[1][0], (int, None)) and isinstance(v[1][1], (int, None)):
                if isinstance(v[1][0], int) and isinstance(v[1][1], int) and v[1][0] > v[1][1]:
                    raise ValueError("The minimum value must be less than or equal to the maximum value.")
                self._cardinality[v[0]] = v[1]
            else:
                raise ValueError("The cardinality values must be integers or None.")
        else:
            raise ValueError("The cardinality value is malformed.")

    @property
    def mcuid(self):
        """
        The unique identifier of the component.
        """
        return self._mcuid

    @property
    def acuid(self):
        """
        The unique identifier of the wrapping XdAdapter of the component.
        """
        return self._acuid

    @property
    def label(self):
        """
        The semantic name of the component.
        """
        return self._label

    @property
    def docs(self):
        """
        The documentation string.
        """
        return self._docs

    @docs.setter
    def doc(self, v):
        if checkers.is_string(v):
            self._docs = v
        else:
            raise ValueError("the Documentation value must be a string.")

    @property
    def pred_obj_list(self):
        """
        A list of additional predicate object pairs to describe the component.
        Each list item is a tuple where 0 is the predicate and 1 is the object.
        Ex: ('rdf:resource','https://www.niddk.nih.gov/health-information/health-statistics')
        The setter accepts the tuple and appends it to the list.
        """
        return self._pred_obj_list

    @pred_obj_list.setter
    def pred_obj_list(self, v):
        if checkers.is_iterable(v) and len(v) == 2 and isinstance(v[0], str) and isinstance(v[1], str):
            self._pred_obj_list.append(v)
        else:
            raise ValueError("the Predicate Object List value must be a tuple of two strings.")

    @property
    def definition_url(self):
        """
        The primary definition URL for the component.
        Cannot be an IP address. 
        """
        return self._definition_url

    @definition_url.setter
    def definition_url(self, v):
        if checkers.is_url(v):
            self._definition_url = v
        else:
            raise ValueError("the Definition URL value must be a valid URL.")

    @property
    def act(self):
        """
        Access Control Tag. If this is used it must contain a valid term from the Access Control System linked 
        to by the containing Data Model.
        """
        return self._act

    @act.setter
    def act(self, v):
        if checkers.is_string(v):
            self._act = v
        else:
            raise ValueError("the Access Control Tag value must be a string.")

    @property
    def ev(self):
        """
        In an invalid instance, the application can indicate here why data is missing or invalid. 
        The sub-types are based on ISO 21090 NULL Flavors entries, with additions noted from real-world usage.
        """
        return self._ev

    @ev.setter
    def ev(self, v):
        if checkers.is_type(v, 'ExceptionalValue'):
            self._ev = v
        else:
            raise ValueError("the ev value must be an ExceptionalValue.")

    @property
    def vtb(self):
        """
        Valid Time Begin. If present this must be a valid datetime including timezone. 
        It is used to indicate the beginning time that information is considered valid.
        """
        return self._vtb

    @vtb.setter
    def vtb(self, v):
        if checkers.is_datetime(v):
            self._vtb = v
        else:
            raise ValueError("the Valid Time Begin value must be a datetime.")

    @property
    def vte(self):
        """
        Valid Time End. If present this must be a valid date-time including timezone. 
        It is used to indicate the ending time that information is considered valid or the time the information expired or 
        will expire.
        """
        return self._vte

    @vte.setter
    def vte(self, v):
        if checkers.is_datetime(v):
            self._vte = v
        else:
            raise ValueError("the Valid Time End value must be a datetime.")

    @property
    def tr(self):
        """
        Time Recorded. If present this must be a valid date-time. 
        It is used to indicate the the actual date and time the data was recorded.
        """
        return self._tr

    @tr.setter
    def tr(self, v):
        if checkers.is_datetime(v):
            self._tr = v
        else:
            raise ValueError("the Time Recorded value must be a datetime.")

    @property
    def modified(self):
        """
        Time Modified. If present this must be a valid date-time stamp. 
        It is used to indicate the the actual date and time the data was last changed.
        """
        return self._modified

    @modified.setter
    def modified(self, v):
        if checkers.is_datetime(v):
            self._modified = v
        else:
            raise ValueError("the Modified value must be a datetime.")

    @property
    def latitude(self):
        """
        Latitude in decimal format. Value range -90.000000 to 90.000000.
        """
        return self._latitude

    @latitude.setter
    def latitude(self, v):
        if checkers.is_decimal(v, minimum=-90.00, maximum=90.00):
            self._latitude = v
        else:
            raise ValueError("the Latitude value must be a decimal between -90.00 and 90.00.")

    @property
    def longitude(self):
        """
        Longitude in decimal format. Value range -180.000000 to 180.000000.
        """
        return self._longitude

    @longitude.setter
    def longitude(self, v):
        if checkers.is_decimal(v, minimum=-180.00, maximum=180.00):
            self._longitude = v
        else:
            raise ValueError("the Longitude value must be a decimal between -180.00 and 180.00.")

    def __str__(self):
        return(self.__class__.__name__ + ' : ' + self.label + ', ID: ' + self.mcuid)


class InvlUnits:
    """
    The units designation for an Interval is slightly different than other complexTypes. This complexType is composed of a units name and a URI because in a ReferenceRange parent there can be different units for different ranges. Example: A XdQuantity of
    temperature can have a range in degrees Fahrenheit and one in degrees Celsius. The derived complexType in the CMC has these values fixed by the modeler.
    """

    def __init__(self, units_name, units_uri):
        self._mcuid = cuid()
        if checkers.is_string(units_name, minimum_length=1):
            self.units_name = units_name
        else:
            raise ValueError("The units_name must be a string of at least one character.")

        if checkers.is_url(units_uri):
            self.units_uri = units_uri
        else:
            raise ValueError("The units_uri must be a valid URL.")

    def __str__(self):
        return(self.__class__.__name__ + ' : ' + self.units_name + ', ID: ' + self.mcuid)


class XdIntervalType(XdAnyType):
    """
    Generic type defining an interval (i.e. range) of a comparable type. An interval is a contiguous subrange of a
    comparable base type. Used to define intervals of dates, times, quantities, etc. Whose datatypes are the same and
    are ordered. In S3Model, they are primarily used in defining reference ranges. The type of upper and lower must be set in the DM.
    """

    def __init__(self, label):
        super().__init__(label)

        self._lower = None
        self._upper = None
        self._lower_included = None
        self._upper_included = None
        self._lower_bounded = None
        self._upper_bounded = None
        self._interval_units = None

    @property
    def lower(self):
        """
        Defines the lower value of the interval.
        """
        return self._lower

    @lower.setter
    def lower(self, v):
        if type(self.v) in invlTypes:
            if type(self._upper) is None:
                self._lower = v
            elif (type(self._upper) == type(self.v)):
                self._lower = v
            else:
                raise ValueError("The lower and upper types must match")
        else:
            raise ValueError("The data type of " + str(v) + " must be a valid interval type.")

    @property
    def upper(self):
        """
        Defines the upper value of the interval.
        """
        return self._upper

    @upper.setter
    def upper(self, v):
        if type(self.v) in invlTypes:
            if type(self._lower) is None:
                self._upper = v
            elif (type(self._lower) == type(self.v)):
                self._upper = v
            else:
                raise ValueError("The lower and upper types must match")
        else:
            raise ValueError("The data type of " + str(v) + " must be a valid interval type.")

    @property
    def lower_included(self):
        """
        Is the lower value of the interval inclusive?
        """
        return self._lower_included

    @lower_included.setter
    def lower_included(self, v):
        if isinstance(v, bool):
            self._lower_included = v
        else:
            raise ValueError("the lower_included value must be a Boolean.")

    @property
    def upper_included(self):
        """
        Is the upper value of the interval inclusive?
        """
        return self._upper_included

    @upper_included.setter
    def upper_included(self, v):
        if isinstance(v, bool):
            self._upper_included = v
        else:
            raise ValueError("the upper_included value must be a Boolean.")

    @property
    def lower_bounded(self):
        """
        Is the lower value of the interval bounded?
        """
        return self._lower_bounded

    @lower_bounded.setter
    def lower_bounded(self, v):
        if isinstance(v, bool):
            self._lower_bounded = v
        else:
            raise ValueError("the lower_bounded value must be a Boolean.")

    @property
    def upper_bounded(self):
        """
        Is the upper value of the interval bounded?
        """
        return self._upper_bounded

    @upper_bounded.setter
    def upper_bounded(self, v):
        if isinstance(v, bool):
            self._upper_bounded = v
        else:
            raise ValueError("the upper_bounded value must be a Boolean.")

    @property
    def interval_units(self):
        """
        Defines the the units for this Interval.
        """
        return self._interval_units

    @interval_units.setter
    def interval_units(self, v):
        if isinstance(v, InvlUnits):
            self._interval_units = v
        else:
            raise ValueError("the interval_units value must be a InvlUnits instance.")

    def __str__(self):
        return(self.__class__.__name__ + ' : ' + self.label + ', ID: ' + self.mcuid + '\n')


class ReferenceRangeType(XdAnyType):
    """
    Defines a named range to be associated with any ORDERED datum. Each such range is sensitive to the context,
    e.g. sex, age, location, and any other factor which affects ranges.
    May be used to represent high, low, normal, therapeutic, dangerous, critical, etc. ranges that are constrained by an interval.
    """

    def __init__(self, label):
        super().__init__(label)

        self._definition = ''
        self._interval = None
        self._is_normal = False

    @property
    def definition(self):
        """
        Term whose value indicates the meaning of this range, e.g. 'normal', 'critical', 'therapeutic' etc.
        """
        return self._definition

    @definition.setter
    def definition(self, v):
        if checkers.is_string(v):
            self._definition = v
        else:
            raise ValueError("the definition value must be a string.")

    @property
    def interval(self):
        """
        The data range for this reference range.
        """
        return self._interval

    @interval.setter
    def interval(self, v):
        if isinstance(v, XdIntervalType):
            self._interval = v
        else:
            raise ValueError("the interval value must be a XdIntervalType.")

    @property
    def is_normal(self):
        """
        True if this reference range defines values that are considered to be normal. In the context of the value in the definition element.
        """
        return self._is_normal

    @is_normal.setter
    def is_normal(self, v):
        if isinstance(v, bool):
            self._is_normal = v
        else:
            raise ValueError("the is_normal value must be a Boolean.")

    def __str__(self):
        return(self.__class__.__name__ + ' : ' + self.label + ', ID: ' + self.mcuid)


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

    def __init__(self, label):
        super().__init__(label)
        self._true_value = None
        self._false_value = None
        self._options = None

    @property
    def options(self):
        """
        The possible choices for true_value or false_value.
        """
        return(self._options)

    @options.setter
    def options(self, v):
        if isinstance(v, dict):
            k = v.keys()
            if len(k) == 2 and 'trues' in k and 'falses' in k:
                for x in k:
                    if not isinstance(v[x], list):
                        raise ValueError("Values in the options dictionary must be lists.", v[x])

                self._options = v
            else:
                raise ValueError('XdBoolean options dictionary has invalid keys. They should be "trues" and "falses", not ', k)
        else:
            raise TypeError('XdBoolean options must be a dictionary. Not ', type(v))

    @property
    def true_value(self):
        """
        A string that represents a boolean True in the implementation. These are constrained by a set of enumerations.
        """
        return self._true_value

    @true_value.setter
    def true_value(self, v):
        if v in self._options['trues'] and self._false_value == None:
            self._true_value = v
        else:
            raise ValueError("the true_value value must be in the options['trues'] list and the false_value must be None.")

    @property
    def false_value(self):
        """
        A string that represents a boolean False in the implementation. These are constrained by a set of enumerations.
        """
        return self._false_value

    @false_value.setter
    def false_value(self, v):
        if v in self._options['falses'] and self._false_value == None:
            self._false_value = v
        else:
            raise ValueError("the false_value value must be in the options['falses'] list and the true_value must be None.")


class XdLinkType(XdAnyType):
    """
    Used to specify a Universal Resource Identifier. Set the pattern facet to accommodate your needs in the DM. 
    Intended use is to provide a mechanism that can be used to link together Data Models. 
    The relation element allows for the use of a descriptive term for the link with an optional URI pointing to the 
    source vocabulary. In most usecases the modeler will define all three of these using the 'fixed' attribute. 
    Other usecases will have the 'relation' and 'relation-uri' elements fixed and the application will provide the 
    'link-value'.
    """

    def __init__(self, label):
        super().__init__(label)

        self._link = ''
        self._relation = ''
        self._relation_uri = ''
        self.cardinality = ('relation_uri', (0, 1))

    @property
    def link(self):
        """
        A required URI. A URL to another Data Model or just the dm-{uuid}.
        """
        return self._link

    @link.setter
    def link(self, v):
        if checkers.is_string(v):
            self._link = v
        else:
            raise ValueError("the link value must be a string.")

    @property
    def relation(self):
        """
        A required term, normally drawn from a vocabulary or ontology such as the OBO RO.
        """
        return self._relation

    @relation.setter
    def relation(self, v):
        if checkers.is_string(v):
            self._relation = v
        else:
            raise ValueError("the relation value must be a string.")

    @property
    def relation_uri(self):
        """
        A URI where the definition of the relation element term can be found. 
        Normally points to an ontology such as the OBO RO http://purl.obolibrary.org/obo/ro.owl
        """
        return self._relation_uri

    @relation_uri.setter
    def relation_uri(self, v):
        if checkers.is_url(v):
            self._relation_uri = v
        else:
            raise ValueError("the relation_uri value must be a URL.")


class XdStringType(XdAnyType):
    """
    The string data type can contain characters, line feeds, carriage returns, and tab characters. 
    The use cases are for any free form text entry or for any enumerated lists. 
    Additionally the minimum and maximum lengths may be set and regular expression patterns may be specified.
    """

    def __init__(self, label):
        super().__init__(label)

        self._xdstring_value = ''
        self._xdstring_language = ''
        self._enums = []
        self._regex = None
        self._default = None
        self._length = None
        self.cardinality = ('xdstring_value', (0, 1))
        self.cardinality = ('xdstring_language', (0, 1))

    @property
    def xdstring_value(self):
        """
        The string value of the item.
        """
        return self._xdstring_value

    @xdstring_value.setter
    def xdstring_value(self, v):
        if checkers.is_string(v):
            self._xdstring_value = v
        else:
            raise ValueError("the xdstring_value value must be a string.")

    @property
    def xdstring_language(self):
        """
        Optional indicator of the localised language in which this data-type is written. 
        Only required when the language used here is different from the enclosing Data Model.
        """
        return self._xdstring_language

    @xdstring_language.setter
    def xdstring_language(self, v):
        if checkers.is_string(v):
            self._xdstring_language = v
        else:
            raise ValueError("the xdstring_language value must be a string.")

    @property
    def length(self):
        """
        The length constraints on the xdstring_value.
        The value can be an integer which will set the exact length constraint or it can be a tuple of the min/max length pair.
        The values inside the tuple can be integers or the None value wich will cause the min or max value to not be set.
        """
        return self._length

    @length.setter
    def length(self, v):
        if checkers.is_integer(v) and v >= 1:
            self._length = v
        elif checkers.is_iterable(v) and len(v) == 2:
            if not isinstance(v[0], (int, None)) or not isinstance(v[1], (int, None)):
                raise ValueError("The tuple must contain two values of either type, None or integers.")
            elif isinstance(v[0], int) and isinstance(v[1], int) and v[0] > v[1]:
                raise ValueError("Minimum length must be smaller or equal to maximum length.")
            self._length = v
        else:
            raise ValueError("The length value must be an integer (exact length) or a tuple (min/max lengths).")

    @property
    def regex(self):
        """
        A regular expression to constrain the string value. The regualr expression must meet the constraints for XML Schema.
        See: https://www.regular-expressions.info/xml.html 
        """
        return self._regex

    @regex.setter
    def regex(self, v):
        if checkers.is_string(v):
            if self._enums is not None:
                raise ValueError("The elements 'enums' and 'regex' are mutally exclusive. Set one of them to 'None'.")
            try:
                re.compile(v)
                self._regex = v
            except re.error:
                raise ValueError("The value is not a valid regular expression.")

    @property
    def enums(self):
        """
        A list of string values used to constrain the value of the item.
        """
        return self._enums

    @enums.setter
    def enums(self, v):
        if self._regex is not None:
            raise ValueError("The elements 'enums' and 'regex' are mutally exclusive. Set one of them to 'None'.")
        if checkers.is_iterable(v):
            for enum in v:
                if not isinstance(enum, str):
                    raise ValueError("The enumerations must be strings.")
            self._enums = v
        else:
            raise ValueError("The enumerations must be a list of strings.")

    @property
    def default(self):
        """
        The default value for the string value of the item.
        """
        return self._default

    @default.setter
    def default(self, v):
        if checkers.is_string(v):
            self._default = v
        else:
            raise ValueError("The default value must be a string.")


class XdFileType(XdAnyType):
    """
    A type to use for encapsulated content (aka. files) for image, audio and other media types with a defined MIME type. This type provides a choice of embedding the content into the data or using a URL to point to the content.
    """

    def __init__(self, label):
        super().__init__(label)

        self._size = None
        self._encoding = ''
        self._xdfile_language = ''
        self._formalism = ''
        self._media_type = ''
        self._compression_type = ''
        self._hash_result = ''
        self._hash_function = ''
        self._alt_txt = ''
        # choice of uri or media_content
        self._uri = None
        self._media_content = None
        self.cardinality = ('size', (1, 1))
        self.cardinality = ('encoding', (0, 1))
        self.cardinality = ('xdfile_language', (0, 1))
        self.cardinality = ('formalism', (0, 1))
        self.cardinality = ('media_type', (0, 1))
        self.cardinality = ('compression_type', (0, 1))
        self.cardinality = ('hash_result', (0, 1))
        self.cardinality = ('hash_function', (1, 1))
        self.cardinality = ('alt_txt', (1, 1))

    @property
    def size(self):
        """
        Original size in bytes of unencoded encapsulated data. I.e. encodings such as base64, hexadecimal, etc. do not change the value of this element.
        """
        return self._size

    @size.setter
    def size(self, v):
        if checkers.is_integer(v):
            self._size = v
        else:
            raise ValueError("The size value must be an integer.")

    @property
    def encoding(self):
        """
        Name of character encoding scheme in which this value is encoded. 
        Coded from the IANA charcater set table: http://www.iana.org/assignments/character-sets 
        Unicode is the default assumption in S3Model, with UTF-8 being the assumed encoding. 
        This optional element allows for variations from these assumptions.
        """
        return self._encoding

    @encoding.setter
    def encoding(self, v):
        if checkers.is_string(v):
            self._encoding = v
        else:
            raise ValueError("the encoding value must be an string.")

    @property
    def xdfile_language(self):
        """
        Optional indicator of the localised language of the content. 
        Typically remains optional in the CMC and used at runtime when the content is in a different language 
        from the enclosing CMC.
        """
        return self._xdfile_language

    @xdfile_language.setter
    def xdfile_language(self, v):
        if checkers.is_string(v):
            self._xdfile_language = v
        else:
            raise ValueError("the xdfile_language value must be a string.")

    @property
    def formalism(self):
        """
        Name of the formalism or syntax used to inform an application regarding a candidate parser to use on the content. 
        Examples might include: 'ATL', 'MOLA', 'QVT', 'GDL', 'GLIF', etc.
        """
        return self._formalism

    @formalism.setter
    def formalism(self, v):
        if checkers.is_string(v):
            self._formalism = v
        else:
            raise ValueError("the formalism value must be an string.")

    @property
    def media_type(self):
        """
        Media (MIME) type of the original media-content w/o any compression. 
        See IANA registered types: http://www.iana.org/assignments/media-types/media-types.xhtml
        """
        return self._media_type

    @media_type.setter
    def media_type(self, v):
        if checkers.is_string(v):
            self._media_type = v
        else:
            raise ValueError("the media_type value must be an string.")

    @property
    def compression_type(self):
        """
        Compression/archiving mime-type. If this elements does not exist then it means there is no compression/archiving. 
        For a list of common mime-types for compression/archiving see: http://en.wikipedia.org/wiki/List_of_archive_formats.
        """
        return self._compression_type

    @compression_type.setter
    def compression_type(self, v):
        if checkers.is_string(v):
            self._compression_type = v
        else:
            raise ValueError("the compression_type value must be an string.")

    @property
    def hash_result(self):
        """
        Hash function result of the 'media-content'. There must be a corresponding hash function type listed for this 
        to have any meaning. See: http://en.wikipedia.org/wiki/List_of_hash_functions#Cryptographic_hash_functions
        """
        return self._hash_result

    @hash_result.setter
    def hash_result(self, v):
        if checkers.is_string(v):
            self._hash_result = v
        else:
            raise ValueError("the hash_result value must be an string.")

    @property
    def hash_function(self):
        """
        Hash function used to compute hash-result. 
        See: http://en.wikipedia.org/wiki/List_of_hash_functions#Cryptographic_hash_functions
        """
        return self._hash_function

    @hash_function.setter
    def hash_function(self, v):
        if checkers.is_string(v):
            self._hash_function = v
        else:
            raise ValueError("the hash_function value must be an string.")

    @property
    def alt_txt(self):
        """
        Text to display in lieu of multimedia display or execution.
        """
        return self._alt_txt

    @alt_txt.setter
    def alt_txt(self, v):
        if checkers.is_string(v):
            self._alt_txt = v
        else:
            raise ValueError("the alt_txt value must be an string.")

    @property
    def uri(self):
        """
        URI reference to electronic information stored outside the record as a file, database entry etc, 
        if supplied as a reference.
        """
        return self._uri

    @uri.setter
    def uri(self, v):
        if self._media_content == None and checkers.is_url(v):
            self._uri = v
        else:
            raise ValueError("the uri value must be a URL and media_content must be None.")

    @property
    def media_content(self):
        """
        The content, if stored locally. The CMC modeler chooses either a uri or local content element.
        If the passed value is a string it will be converted to bytes and base64 encoded. 
        If it is already bytes then it is just encoded.
        """
        return self._media_content

    @media_content.setter
    def media_content(self, v):
        if self._uri == None:
            if checkers.is_string(v):
                self._media_content = b64encode(bytes(v), 'utf-8')
            elif isinstance(v, ByteString):
                self._media_content = b64encode(v, 'utf-8')
            else:
                raise ValueError("the media_content value must be a string or bytes object that can be Base64 encoded.")
        else:
            raise ValueError("uri must be None.")


class XdOrderedType(XdAnyType):
    """
    Serves as an abstract common ancestor of all ordered types
    """
    @abstractmethod
    def __init__(self, label):
        super().__init__(label)

        self._referencerange = None
        self._normal_status = None
        self.cardinality = ('referencerange', (0, None))
        self.cardinality = ('normal_status', (0, 1))

    @property
    def referencerange(self):
        """
        Optional list of ReferenceRanges for this value in its particular measurement context.
        """
        return self._referencerange

    @referencerange.setter
    def referencerange(self, v):
        if checkers.is_iterable(v):
            for i in v:
                if not checkers.is_type(i, "ReferenceRangeType"):
                    raise ValueError("The referencerange value must be a list of ReferenceRangeType items.")
            self._referencerange = v
        else:
            raise ValueError("The referencerange value must be a list of ReferenceRangeType items.")

    @property
    def normal_status(self):
        """
        Optional normal status indicator of value with respect to normal range for this value. 
        Often used in situations such as medical lab results when coded by ordinals in series 
        such as; HHH, HH, H, (nothing), L, LL, LLL, etc.
        """
        return self._normal_status

    @normal_status.setter
    def normal_status(self, v):
        if checkers.is_string(v):
            self._normal_status = v
        else:
            raise ValueError("the normal_status value must be an string.")


class XdOrdinalType(XdOrderedType):
    """
    Models rankings and scores, e.g., pain, Apgar values, educational level, and the Likert Scale where there is;

        * implied ordering,
        * no implication that the distance between each value is constant, and
        * the total number of values is finite.

        Note that the term ‘ordinal’ in mathematics means natural numbers only. In this case, any decimal is allowed since negative, and zero values are used by medical and other professionals for centering values around a neutral point. Also, decimal values are sometimes used such as 0.5 or .25

        Examples of sets of ordinal values are;

        * -3, -2, -1, 0, 1, 2, 3 -- reflex response values
        * 0, 1, 2 -- Apgar values

        Also used for recording any clinical or other data which is customarily recorded using symbolic values. Examples;

        * the results on a urinalysis strip, e.g. {neg, trace, +, ++, +++} are used for leukocytes, protein, nitrites etc;
        * for non-haemolysed blood {neg, trace, moderate};
        * for haemolysed blood {neg, trace, small, moderate, large}.

        Elements *ordinal* and *symbol* MUST have the same number of enumerations in the RMC.
    """

    def __init__(self, label):
        super().__init__(label)

        self._ordinal = None
        self._symbol = None
        self._choices = None
        self.cardinality = ('ordinal', (1, 1))
        self.cardinality = ('symbol', (1, 1))

    @property
    def ordinal(self):
        """
        Value in ordered enumeration of values. 
        The base decimal is zero with any number of decimal values used to order the symbols. 
        Example 1: 0 = Trace, 1 = +, 2 = ++, 3 = +++, etc. Example 2: 0 = Mild, 1 = Moderate, 2 = Severe
        """
        return self._ordinal

    @ordinal.setter
    def ordinal(self, v):
        if checkers.is_decimal(v):
            self._ordinal = v
        else:
            raise ValueError("the ordinal value must be a decimal.")

    @property
    def symbol(self):
        """
        Coded textual representation of this value in the enumeration, which may be strings made from “+” symbols, 
        or other enumerations of terms such as “mild”, “moderate”, “severe”, or even the same number series as the 
        values, e.g. “1”, “2”, “3”.
        """
        return self._symbol

    @symbol.setter
    def symbol(self, v):
        if checkers.is_string(v):
            self._symbol = v
        else:
            raise ValueError("the symbol value must be a decimal.")

    @property
    def choices(self):
        """
        The choices dictionary must have decimals (or integers) as keys to be used as the ordinals and the values as strings
        to be used as the symbols.
        """
        return self._choices

    @choices.setter
    def choices(self, v):
        if checkers.is_dict(v):
            self._choices = v
        else:
            raise ValueError("the choices value must be a dictionary with the keys as decimals and the values as strings.")


class XdQuantifiedType(XdOrderedType):
    """
    Serves as an abstract common ancestor of all quantifiable types
    """

    def __init__(self, label):
        super().__init__(label)

        self._magnitude_status = ''
        self._error = None
        self._accuracy = None
        self.cardinality = ('magnitude_status', (0, 1))
        self.cardinality = ('error', (0, 1))
        self.cardinality = ('accuracy', (0, 1))

    @property
    def magnitude_status(self):
        """
        MagnitudeStatus provides a general indication of the accuracy of the magnitude expressed in the XdQuantified 
        subtypes. Should be used to inform users and not for decision support uses.
        Must be one of: None,'equal','less_than', 'greater_than', 'less_than_or_equal', 'greater_than_or_equal', 'approximate'
        """
        return self._magnitude_status

    @magnitude_status.setter
    def magnitude_status(self, v):
        if isinstance(v, (str, None)) and v in [None, 'equal', 'less_than', 'greater_than', 'less_than_or_equal', 'greater_than_or_equal', 'approximate']:
            self._magnitude_status = v
        else:
            raise ValueError("The magnitude_status value must be one of: None,'equal','less_than', 'greater_than', 'less_than_or_equal', 'greater_than_or_equal', 'approximate'.")

    @property
    def error(self):
        """
        Error margin of measurement, as an integer indicating error in the recording method or instrument (+/- %). 
        A logical value of 0 indicates 100% accuracy, i.e. no error.
        """
        return self._error

    @error.setter
    def error(self, v):
        if isinstance(v, int) and 0 <= v <= 100:
            self._error = v
        else:
            raise ValueError("The error value must be an integer 0 - 100.")

    @property
    def accuracy(self):
        """
        Accuracy of the value in the magnitude attribute in the range 0% to (+/-)100%. 
        A value of 0 means that the accuracy is unknown.
        """
        return self._accuracy

    @accuracy.setter
    def accuracy(self, v):
        if isinstance(v, int) and 0 <= v <= 100:
            self._error = v
        else:
            raise ValueError("The accuracy value must be an integer 0 - 100.")


class XdCountType(XdQuantifiedType):
    """
    Countable quantities. Used for countable types such as pregnancies and steps (taken by a physiotherapy patient), 
    number of cigarettes smoked in a day, etc. The thing(s) being counted must be represented in the units element. 
    Misuse: Not used for amounts of physical entities (which all have standardized units).
    """

    def __init__(self, label):
        super().__init__(label)

        self._xdcount_value = None
        self._xdcount_units = None


class XdQuantityType(XdQuantifiedType):
    """
    Quantified type representing specific quantities, i.e. quantities expressed as a magnitude and units. Can also be used for time durations, where it is more convenient to treat these as simply a number of individual seconds, minutes, hours, days, months, years, etc. when no temporal calculation is to be performed.
    """

    def __init__(self, label):
        super().__init__(label)

        self._xdquantity_value = None
        self._xdquantity_units = None


class XdFloatType(XdQuantifiedType):
    """
    Quantified type representing specific a value as a floating point number and optional units.
    """

    def __init__(self, label):
        super().__init__(label)

        self._xdfloat_value = None
        self._xdfloat_units = None


class XdRatioType(XdQuantifiedType):
    """
    Models a ratio of values, i.e. where the numerator and denominator are both pure numbers. Should not be used to represent things like blood pressure which are often written using a ‘/’ character, giving the misleading impression that the item is a ratio,
    when in fact it is a structured value. Similarly, visual acuity, often written as (e.g.) “20/20” in clinical notes is not a ratio but an ordinal (which includes non-numeric symbols like CF = count fingers etc). Should not be used for formulations. Used for modeling; ratios, rates or proportions.
    """

    def __init__(self, label):
        super().__init__(label)

        # constrained to list ['ratio','rate', 'proportion']
        self._ratio_type = None
        self._numerator = None
        self._denominator = None
        self._xdratio_value = None
        self._numerator_units = None
        self._denominator_units = None
        self._xdratio_units = None


class XdTemporalType(XdOrderedType):
    """
    Type defining the concept of date and time types. Must be constrained in DMs to be one or more of the below elements. This gives the modeler the ability to optionally allow full or partial dates at run time. Setting both maxOccurs and minOccurs to zero cause the element to be prohibited.
    """

    def __init__(self, label):
        super().__init__(label)

        # TODO: fix the types
        self._xdtemporal_date = None
        self._xdtemporal_time = None
        self._xdtemporal_datetime = None
        self._xdtemporal_day = None
        self._xdtemporal_month = None
        self._xdtemporal_year = None
        self._xdtemporal_year_month = None
        self._xdtemporal_month_day = None
        self._xdtemporal_duration = None


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
        super().__init__(label)

        self._XdAdapter_value = None


class ClusterType(ItemType):
    """
    The grouping component, which may contain further instances of itself or any eXtended datatype, in an ordered list. This can serve as the root component for arbitrarily complex structures.
    """

    def __init__(self, label):
        super().__init__(label)

        self._items = None


class PartyType:
    """
    Description of a party, including an optional external link to data for this party in a demographic or other identity management system. An additional details element provides for the inclusion of information related to this party directly. If the party
    information is to be anonymous then do not include the details element.
    """

    def __init__(self, label):
        self._mcuid = cuid()  # model cuid
        self._label = ''

        if checkers.is_string(label, 2):
            if len(label) > 1:
                self._label = label
            else:
                raise ValueError('label must be at least 2 characters in length')
        else:
            raise TypeError('"label" must be a string type. Not a ', type(label))

        self._party_name = None
        self._party_ref = None
        self._party_details = None

    @property
    def label(self):
        """
        The semantic name of the component.
        """
        return self._label

    def __str__(self):
        return(self.__class__.__name__ + ' : ' + self.label + ', ID: ' + self.mcuid)


class AuditType:
    """
    AuditType provides a mechanism to identify the who/where/when tracking of instances as they move from system to system.
    """

    def __init__(self, label):
        self._mcuid = cuid()  # model cuid
        self._label = ''

        if checkers.is_string(label, 2):
            if len(label) > 1:
                self._label = label
            else:
                raise ValueError('label must be at least 2 characters in length')
        else:
            raise TypeError('"label" must be a string type. Not a ', type(label))

        self._system_id = None
        self._system_user = None
        self._location = None
        self._timestamp = None

    @property
    def label(self):
        """
        The semantic name of the component.
        """
        return self._label

    def __str__(self):
        return(self.__class__.__name__ + ' : ' + self.label + ', ID: ' + self.mcuid)


class AttestationType:
    """
    Record an attestation by a party of the DM content. The type of attestation is recorded by the reason attribute, which my be coded.
    """

    def __init__(self, label):
        self._mcuid = cuid()  # model cuid
        self._label = ''

        if checkers.is_string(label, 2):
            if len(label) > 1:
                self._label = label
            else:
                raise ValueError('label must be at least 2 characters in length')
        else:
            raise TypeError('"label" must be a string type. Not a ', type(label))

        self._view = None
        self._proof = None
        self._reason = None
        self._committer = None
        self._committed = None
        self._pending = None

    @property
    def label(self):
        """
        The semantic name of the component.
        """
        return self._label

    def __str__(self):
        return(self.__class__.__name__ + ' : ' + self.label + ', ID: ' + self.mcuid)


class ParticipationType:
    """
    Model of a participation of a Party (any Actor or Role) in an activity. Used to represent any participation of a Party in some activity, which is not explicitly in the model, e.g. assisting nurse. Can be used to record past or future participations.
    """

    def __init__(self, label):
        self._mcuid = cuid()  # model cuid
        self._label = ''

        if checkers.is_string(label, 2):
            if len(label) > 1:
                self.label = label
            else:
                raise ValueError('label must be at least 2 characters in length')
        else:
            raise TypeError('"label" must be a string type. Not a ', type(label))

        self._performer = None
        self._function = None
        self._mode = None
        self._start = None
        self._end = None

    @property
    def label(self):
        """
        The semantic name of the component.
        """
        return self._label

    def __str__(self):
        return(self.__class__.__name__ + ' : ' + self.label + ', ID: ' + self.mcuid)


class DMType:
    """
    This is the root node of a Data Model (DM)
    """

    def __init__(self):
        self._mcuid = cuid()
        self.metadata = self.genMD()
        self._data = ClusterType()
        self._label = self.metadata['title']
        self._dm_language = self.metadata['language']
        self._dm_encoding = 'utf-8'
        self._current_state = ''
        self._subject = None
        self._provider = None
        self._participations = list()
        self._protocol = None
        self._workflow = None
        self._acs = None
        self._audits = list()
        self._attestations = list()
        self._links = list()

    def __str__(self):
        return("S3Model Data Model\n" + "ID: " + self.mcuid + "\n" + self.showMetadata(self.metadata))

    def showMetadata(self):
        mdStr = ''
        for k, v in self.metadata.items():
            mdStr += k + ': ' + repr(v) + '\n'
        return(mdStr)

    def genMD(self):
        """
        Create a metadata dictionary for the DM if one isn't passed in.
        """
        md = OrderedDict()
        md['title'] = 'New Data Model'
        md['creator'] = 'Joe Smith'
        md['subject'] = 'S3M DM'
        md['rights'] = 'Creative Commons'
        md['relation'] = 'None'
        md['coverage'] = 'Global'
        md['type'] = 'S3Model Data Model (DM)'
        md['identifier'] = 'dm-' + self.mcuid
        md['description'] = 'Needs a description'
        md['publisher'] = 'Data Insights, Inc.'
        md['date'] = '{0:%Y-%m-%dT%H:%M:%S}'.format(datetime.now())
        md['format'] = 'text/xml'
        md['language'] = 'en-US'

        return(md)
