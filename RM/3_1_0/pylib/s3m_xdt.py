"""
Defines the S3Model reference model in Python 3.7
Version 3.1.0
This implementation is not a strict model of the RM. 
It also contains functionality to manage constraints that are
built into the XML Schema parsers. 
"""
import re
import random
import json
from datetime import datetime, date, time, timedelta
from decimal import Decimal
from collections import OrderedDict
from abc import ABC, abstractmethod
from xml.sax.saxutils import escape
from urllib.parse import quote
from base64 import b64encode
from typing import ByteString, Dict, List, Tuple, Iterable

import xmltodict
import pytz
import exrex
from lxml import etree
from cuid import cuid
from validator_collection import checkers

import s3m_ontology
from s3m_ev import ExceptionalValue

ex_acs = ['Private', 'Public', 'Super Secret']  # example access control tags for instance examples

invlTypes = [int, float, date, time, datetime, timedelta]


class XdAnyType(ABC):
    """
    Serves as an abstract common ancestor of all eXtended data-types (Xd*) in S3Model.
    """

    @abstractmethod
    def __init__(self, label: str):
        """
        Initialization for Xd* datatypes in S3Model.
        
        The semantic label (name of the model) is required.
        """
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
        
        The setter method can be called by each subclass to add cardinality 
        values for each element or change the defaults. 
        Some elements cardinality may not be changed. 
        Ex: XdBoolean elements are not modifiable.
        
        The cardinality dictionary uses a string representation of each 
        property name and a tuple as the value.
        
        The value passed into the setter is a tuple with v[0] as a string (key) and 
        v[1] as a tuple containing an integer set representing the 
        (minimum, maximum) values. The entire tuple is replaced in the dictionary. 
        
        Examples
        --------
        
        ('vtb', (1,1)) will set the vtb value to be required.
        
                
        NOTES
        -----
        
        The cardinality for latitude and longitude are combined into one 
        setting called 'location'.

        The Python value of 'None' represents the 'unbounded' XML Schema value.
        The 'unbounded' value is allowed on only a few attributes.

        """
        return self._cardinality

    @cardinality.setter
    def cardinality(self, v):
        if isinstance(v, tuple) and len(v) == 2 and isinstance(v[0], str) and isinstance(v[1], tuple):
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
        The human readable documentation string describing the purpose of 
        the model.
        """
        return self._docs

    @docs.setter
    def docs(self, v: str):
        if checkers.is_string(v):
            self._docs = v
        else:
            raise ValueError("the Documentation value must be a string.")

    @property
    def pred_obj_list(self):
        """
        A list of additional predicate object pairs to describe the component.
        
        Each list item is a tuple where 0 is the predicate and 1 is the object.
        
        Example: 
        ('rdf:resource','https://www.niddk.nih.gov/health-information/health-statistics')
        The setter accepts the tuple and appends it to the list.
        If an empty list is supplied it resets the value to the empty list.
        """
        return self._pred_obj_list

    @pred_obj_list.setter
    def pred_obj_list(self, v: Iterable):
        if isinstance(v, list) and len(v) == 0:
            self._pred_obj_list = []
        elif isinstance(v, tuple) and len(v) == 2 and isinstance(v[0], str) and isinstance(v[1], str):
            self._pred_obj_list.append(v)
        else:
            raise ValueError("the Predicate Object List value must be a tuple of two strings or an empty list.")

    @property
    def definition_url(self):
        """
        The primary definition URL for the model.
        Cannot be an IP address. 
        """
        return self._definition_url

    @definition_url.setter
    def definition_url(self, v: str):
        if checkers.is_url(v):
            self._definition_url = v
            self._docs += '\n\nDefinition: ' + quote(v)
        else:
            raise ValueError("the Definition URL value must be a valid URL.")

    @property
    def act(self):
        """
        Access Control Tag. If this is used it must contain a valid term from 
        the Access Control System linked to by the containing Data Model 
        'acs' attribute.
        """
        return self._act

    @act.setter
    def act(self, v: str):
        if checkers.is_string(v):
            self._act = v
        else:
            raise ValueError("the Access Control Tag value must be a string.")

    @property
    def ev(self):
        """
        In an invalid instance, the application can indicate here why data is 
        missing or invalid. 
        The sub-types are based on ISO 21090 NULL Flavors entries, with 
        additions noted from real-world usage.
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
        It is used to indicate the ending time that information is considered valid 
        or the time the information expired or will expire.
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
        It is used to indicate the initial date and time the data was recorded.
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
        It is used to indicate the date and time the data was last changed.
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
    An enumerated type which represents boolean decisions such as true/false 
    or yes/no answers. 
    
    Useful where it is essential to devise the meanings (often questions in 
    subjective data) carefully so that the only allowed result values result 
    in one of the options; true or false but are presented to the user as 
    a list of options. 

    The possible choices for True or False are values in a dictionary. 
    The class defines 'true_value' and 'false_value'. 
    The instance implementation is restricted to only have a value for one of 
    them based on the user choice from the options dictionary.

    The XdBooleanType should not be used as a replacement for enumerated choice 
    types such as male/female, or similar choice sets. 
    Such values should be modeled as XdStrings with enumerations and may reference 
    a controlled vocabulary. 
    In any case, the choice set often has more than two values.   
    """

    def __init__(self, label: str, opt: dict):
        """
        Create an instance of a XdBooleanType.
        
        Parameters
        ----------
        label: str
            A human readable name lending semantics to the purpose of the model.
        opt: dictionary
            A dictionary where the two allowed keys are 'trues' and 'falses'.
            The items associated with these keys are a list of options for the user to 
            choose from.        
        """
        super().__init__(label)
        self._true_value = None
        self._false_value = None
        if isinstance(opt, dict) and list(opt.keys()) == ['trues','falses']:
            if isinstance(opt['trues'], list) and isinstance(opt['falses'], list):
                self._options = opt
            else:
                raise ValueError("The values of 'trues' and 'falses' must be a list of strings.")
        else:
            raise ValueError("The the options value must be a dictionary with two keys; 'trues' and 'falses'. Their items must be a list of strings.")


    @property
    def true_value(self):
        """
        A string that represents a boolean True in the implementation. 
        These are constrained by a set of enumerations.
        """
        return self._true_value

    @true_value.setter
    def true_value(self, v):
        if v == None:
            self._true_value = None 
        elif v in self._options['trues'] and self._false_value == None:
            self._true_value = v
        else:
            raise ValueError("the true_value value must be in the options['trues'] list and the false_value must be None.")

    @property
    def false_value(self):
        """
        A string that represents a boolean False in the implementation. 
        These are constrained by a set of enumerations.
        """
        return self._false_value

    @false_value.setter
    def false_value(self, v):
        if v == None:
            self._false_value = None 
        elif v in self._options['falses'] and self._true_value == None:
            self._false_value = v
        else:
            raise ValueError("the false_value value must be in the options['falses'] list and the true_value must be None.")

    def asXSD(self):
        """
        Return a XML Schema complexType definition.
        """
        trues = self._options['trues']
        falses = self._options['falses']
        indent = 2
        padding = ('').rjust(indent)
        xdstr = ''
        if self._adapter:
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
        xdstr += padding.rjust(indent + 6) + escape(self.docs.strip()) + '\n'
        xdstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'

        # add RDF
        xdstr += padding.rjust(indent + 6) + '<rdfs:Class rdf:about="mc-' + self.mcuid + '">\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model_3_1_0.xsd#XdBooleanType"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:label rdf:resource="' + self.label.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + quote(self.definition_url.strip()) + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:comment rdf:resource="' + self.docs.strip() + '"/>\n'
        if len(self.pred_obj_list) > 0:  # are there additional predicate-object definitions?
            for po in self.pred_obj_list:
                pred = po[0]
                obj = po[1]
                xdstr += padding.rjust(indent + 8) + '<' + pred.strip() + ' rdf:resource="' + quote(obj.strip()) + '"/>\n'
        xdstr += padding.rjust(indent + 6) + '</rdfs:Class>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
        xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdBooleanType">\n'
        xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
        # XdAny
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + self.label.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['act'][0]) + '" name="act" type="xs:string" default="' + self.act.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ExceptionalValue"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['vtb'][0]) + '" name="vtb" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['vte'][0]) + '" name="vte" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['tr'][0]) + '" name="tr" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['modified'][0]) + '" name="modified" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['location'][0]) + '" name="latitude" type="xs:decimal"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['location'][0]) + '" name="longitude" type="xs:decimal"/>\n'
        # XdBooleanType
        xdstr += padding.rjust(indent + 8) + ("<xs:choice maxOccurs='1' minOccurs='1'>\n")
        xdstr += padding.rjust(indent + 8) + ("<xs:element name='true-value'>\n")
        xdstr += padding.rjust(indent + 10) + ("<xs:simpleType>\n")
        xdstr += padding.rjust(indent + 12) + ("<xs:restriction base='xs:string'>\n")
        for n in range(len(trues)):
            xdstr += padding.rjust(indent + 16) + ("<xs:enumeration value='" + trues[n].strip() + "'/>\n")
        xdstr += padding.rjust(indent + 12) + ("</xs:restriction>\n")
        xdstr += padding.rjust(indent + 10) + ("</xs:simpleType>\n")
        xdstr += padding.rjust(indent + 8) + ("</xs:element>\n")
        xdstr += padding.rjust(indent + 8) + ("<xs:element name='false-value'>\n")
        xdstr += padding.rjust(indent + 10) + ("<xs:simpleType>\n")
        xdstr += padding.rjust(indent + 12) + ("<xs:restriction base='xs:string'>\n")
        for n in range(len(falses)):
            xdstr += padding.rjust(indent + 16) + ("<xs:enumeration value='" + falses[n].strip() + "'/>\n")
        xdstr += padding.rjust(indent + 12) + ("</xs:restriction>\n")
        xdstr += padding.rjust(indent + 10) + ("</xs:simpleType>\n")
        xdstr += padding.rjust(indent + 8) + ("</xs:element>\n")
    
        xdstr += padding.rjust(indent + 8) + ("</xs:choice>\n")
        
        xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
        xdstr += padding.rjust(indent) + '</xs:complexType>\n'

        return(xdstr)
    
    def asXML(self):
        """
        Return an example XML fragment for this model.
        """
        # randomly choose an option
        tf = random.choice(list(self._options.keys()))
        choice = random.choice(self._options[tf])
        act = random.choice(ex_acs)
        
        indent = 2
        padding = ('').rjust(indent)
        xmlstr = ''
        xmlstr += padding.rjust(indent) + '<ms-' + self.mcuid + '>\n'
        xmlstr += padding.rjust(indent + 2) + '<label>' + self.label + '</label>\n'
        if self.cardinality['act'][0] > 0:
            xmlstr += padding.rjust(indent + 2) + '<act>' + act + '</act>\n'
        if self.cardinality['vtb'][0] > 0:
            xmlstr += padding.rjust(indent + 2) + '<vtb>2006-06-04T18:13:51.0</vtb>\n'
        if self.cardinality['vte'][0] > 0:
            xmlstr += padding.rjust(indent + 2) + '<vte>2026-05-04T18:13:51.0</vte>\n'
        if self.cardinality['tr'][0] > 0:
            xmlstr += padding.rjust(indent + 2) + '<tr>2006-05-04T18:13:51.0</tr>\n'
        if self.cardinality['modified'][0] > 0:
            xmlstr += padding.rjust(indent + 2) + '<modified>2006-05-04T18:13:51.0</modified>\n'
        if self.cardinality['location'][0] > 0:
            xmlstr += padding.rjust(indent + 2) + '<latitude>-22.456</latitude>\n'
            xmlstr += padding.rjust(indent + 2) + '<longitude>123.654</longitude>\n'
        if tf == 'trues':
            xmlstr += padding.rjust(indent + 2) + '<true-value>' + choice + '</true-value>\n'
        elif tf == 'falses':
            xmlstr += padding.rjust(indent + 2) + '<false-value>' + choice + '</false-value>\n'
        else:
            xmlstr += padding.rjust(indent + 2) + '** ERROR GENERATING EXAMPLE **\n'
            
            
        xmlstr += padding.rjust(indent) + '</ms-' + self.mcuid + '>\n'
        
        # check for well-formed XML
        parser = etree.XMLParser()
        tree = etree.XML(xmlstr, parser)
        
        return(xmlstr)
    
    def asJSON(self):
        """
        Return an example JSON fragment for this model.
        """
        xml = self.asXML()
        parsed = xmltodict.parse(xml, encoding='UTF-8', process_namespaces=False)
        return(json.dumps(parsed, indent=2, sort_keys=False)) 

    def asXMLex(self):
        """
        Return an example XML fragment for this model.
        
        The core elements are included even though they may not be 
        required via cardinality. Therefore this example may be considerably 
        larger than an actual implementation. 
        """
        # randomly choose an option
        tf = random.choice(list(self._options.keys()))
        choice = random.choice(self._options[tf])
        act = random.choice(ex_acs)
        
        indent = 2
        padding = ('').rjust(indent)
        xmlstr = ''
        xmlstr += padding.rjust(indent) + '<ms-' + self.mcuid + '>\n'
        xmlstr += padding.rjust(indent + 2) + '<label>' + self.label + '</label>\n'
        xmlstr += padding.rjust(indent + 2) + '<act>' + act + '</act>\n'
        xmlstr += padding.rjust(indent + 2) + '<OTH>\n'
        xmlstr += padding.rjust(indent + 4) + '<ev-name>Other</ev-name>  # example exceptional value\n'
        xmlstr += padding.rjust(indent + 2) + '</OTH>\n'
        xmlstr += padding.rjust(indent + 2) + '<vtb>2006-06-04T18:13:51.0</vtb>\n'
        xmlstr += padding.rjust(indent + 2) + '<vte>2026-05-04T18:13:51.0</vte>\n'
        xmlstr += padding.rjust(indent + 2) + '<tr>2006-05-04T18:13:51.0</tr>\n'
        xmlstr += padding.rjust(indent + 2) + '<modified>2006-05-04T18:13:51.0</modified>\n'
        xmlstr += padding.rjust(indent + 2) + '<latitude>-22.456</latitude>\n'
        xmlstr += padding.rjust(indent + 2) + '<longitude>123.654</longitude>\n'
        if tf == 'trues':
            xmlstr += padding.rjust(indent + 2) + '<true-value>' + choice + '</true-value>\n'
        elif tf == 'falses':
            xmlstr += padding.rjust(indent + 2) + '<false-value>' + choice + '</false-value>\n'
        else:
            xmlstr += padding.rjust(indent + 2) + '** ERROR GENERATING EXAMPLE **\n'
            
            
        xmlstr += padding.rjust(indent) + '</ms-' + self.mcuid + '>\n'
        
        # check for well-formed XML
        parser = etree.XMLParser()
        tree = etree.XML(xmlstr, parser)
        
        return(xmlstr)
    
    def asJSONex(self):
        """
        Return an example JSON fragment for this model based on the asXMLex method.
        """
        xml = self.asXMLex()
        parsed = xmltodict.parse(xml, encoding='UTF-8', process_namespaces=False)
        return(json.dumps(parsed, indent=2, sort_keys=False)) 


class XdLinkType(XdAnyType):
    """
    Used to specify a Universal Resource Identifier. Set the pattern facet to accommodate your needs in the DM. 
    Intended use is to provide a mechanism that can be used to link together Data Models. 
    The relation element allows for the use of a descriptive term for the link with an optional URI pointing to the 
    source vocabulary. In most usecases the modeler will define all three of these using the 'fixed' attribute. 
    Other usecases will have the 'relation' and 'relation-uri' elements fixed and the application will provide the 
    'link-value'.
    """

    def __init__(self, label: str, link: str, relation: str):
        """
        The semantic label (name of the model) is required.
        """
        super().__init__(label)

        self._link = link
        self._relation = relation
        self._relation_uri = None
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
        A required term, normally drawn from a vocabulary or ontology such as the rdf:label of OBO RO.
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

    def asXSD(self):
        """
        Return a XML Schema complexType definition.
        """
        indent = 2
        padding = ('').rjust(indent)
        xdstr = ''
        if self._adapter:
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
        xdstr += padding.rjust(indent + 6) + escape(self.docs.strip()) + '\n'
        xdstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'

        # add RDF
        xdstr += padding.rjust(indent + 6) + '<rdfs:Class rdf:about="mc-' + self.mcuid + '">\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model_3_1_0.xsd#XdLinkType"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + quote(self.definition_url.strip()) + '"/>\n'
        if len(self.pred_obj_list) > 0:  # are there additional predicate-object definitions?
            for po in self.pred_obj_list:
                pred = po[0]
                obj = po[1]
                xdstr += padding.rjust(indent + 8) + '<' + pred.strip() + ' rdf:resource="' + quote(obj.strip()) + '"/>\n'
        xdstr += padding.rjust(indent + 6) + '</rdfs:Class>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
        xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdLinkType">\n'
        xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
        # XdAny
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + self.label.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['act'][0]) + '" name="act" type="xs:string" default="' + self.act.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ExceptionalValue"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['vtb'][0]) + '" name="vtb" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['vte'][0]) + '" name="vte" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['tr'][0]) + '" name="tr" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['modified'][0]) + '" name="modified" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['location'][0]) + '" name="latitude" type="xs:decimal"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['location'][0]) + '" name="longitude" type="xs:decimal"/>\n'
        # XdLinkType
        if not self.link:
            raise ValueError("You must create a link URI value.")
        else:
            xdstr += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='link' type='xs:anyURI'fixed='" + escape(self.link.strip()) + "'/>\n")
        if not self.relation:
            raise ValueError("You must add a relationship.")
        else:
            xdstr += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='relation' type='xs:string' fixed='" + escape(self.relation.strip()) + "'/>\n")
        if not self.relation_uri:
            raise ValueError("You must add a URI for the relationship location.")
        else:
            xdstr += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='relation-uri' type='xs:anyURI' fixed='" + escape(self.relation_uri.strip()) + "'/>\n")       
        xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
        xdstr += padding.rjust(indent) + '</xs:complexType>\n'

        return(xdstr)
    
    
    def asXML(self):
        """
        Return an example XML fragment for this model.
        """
        
        act = random.choice(ex_acs)
        
        indent = 2
        padding = ('').rjust(indent)
        xmlstr = ''
        xmlstr += padding.rjust(indent) + '<ms-' + self.mcuid + '>\n'
        xmlstr += padding.rjust(indent + 2) + '<label>' + self.label + '</label>\n'
        if self.cardinality['act'][0] > 0:
            xmlstr += padding.rjust(indent + 2) + '<act>' + act + '</act>\n'
        if self.cardinality['vtb'][0] > 0:
            xmlstr += padding.rjust(indent + 2) + '<vtb>2006-06-04T18:13:51.0</vtb>\n'
        if self.cardinality['vte'][0] > 0:
            xmlstr += padding.rjust(indent + 2) + '<vte>2026-05-04T18:13:51.0</vte>\n'
        if self.cardinality['tr'][0] > 0:
            xmlstr += padding.rjust(indent + 2) + '<tr>2006-05-04T18:13:51.0</tr>\n'
        if self.cardinality['modified'][0] > 0:
            xmlstr += padding.rjust(indent + 2) + '<modified>2006-05-04T18:13:51.0</modified>\n'
        if self.cardinality['location'][0] > 0:
            xmlstr += padding.rjust(indent + 2) + '<latitude>-22.456</latitude>\n'
            xmlstr += padding.rjust(indent + 2) + '<longitude>123.654</longitude>\n'
        xmlstr += padding.rjust(indent + 2) + '<link>' + self.link + '</link>\n'
        xmlstr += padding.rjust(indent + 2) + '<relation>' + self.relation + '</relation>\n'
        xmlstr += padding.rjust(indent + 2) + '<relation-uri>' + self.relation_uri + '</relation-uri>\n'
            
        xmlstr += padding.rjust(indent) + '</ms-' + self.mcuid + '>\n'
        
        # check for well-formed XML
        parser = etree.XMLParser()
        tree = etree.XML(xmlstr, parser)
        
        return(xmlstr)
    
    def asJSON(self):
        """
        Return an example JSON fragment for this model.
        """
        xml = self.asXML()
        parsed = xmltodict.parse(xml, encoding='UTF-8', process_namespaces=False)
        return(json.dumps(parsed, indent=2, sort_keys=False)) 


class XdStringType(XdAnyType):
    """
    The string data type can contain characters, line feeds, carriage returns, and tab characters. 
    The use cases are for any free form text entry or for any enumerated lists. 
    Additionally the minimum and maximum lengths may be set and regular expression patterns may be specified.
    """

    def __init__(self, label):
        """
        The semantic label (name of the model) is required.
        """
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
        if v == None:
            self._length = v
        else:
            if len(self._enums) > 0 or self.regex is not None:
                raise ValueError("The elements 'length', 'enums' and 'regex' are mutally exclusive.  Set length and regex to 'None' or enums to '[]'.")
            if checkers.is_integer(v) and v >= 1:
                self._length = v
            elif isinstance(v, tuple) and len(v) == 2:
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
        if v == None:
            self._regex = v            
        elif checkers.is_string(v):
            if len(self._enums) > 0 or self.length is not None:
                raise ValueError("The elements 'length', 'enums' and 'regex' are mutally exclusive.  Set length and regex to 'None' or enums to '[]'.")
            try:
                re.compile(v)
                self._regex = v
            except re.error:
                raise ValueError("The value is not a valid regular expression.")

    @property
    def enums(self):
        """
        A list of two member tuples (enumeration, URI semantics for the enumeration). 
        
        The enumerations are string values used to constrain the value of the item.
        The URI semantics for the enumeration provides a definition (preferable a URL) for the enumeration.
        Example: ('Blue','http://www.color-wheel-pro.com/color-meaning.html#Blue')
        """
        return self._enums

    @enums.setter
    def enums(self, v):
        if v == []:
            self._enums = v
            
        if self.regex is not None or self.length is not None:
            raise ValueError("The elements 'length', enums' and 'regex' are mutally exclusive. Set length and regex to 'None' or enums to '[]'.")
        
        if isinstance(v, list):
            for enum in v:
                print(enum)
                if not isinstance(enum, tuple):
                    raise ValueError("The enumerations and definitions must be strings.")
                
                if not isinstance(enum[0], str) or not isinstance(enum[1], str):
                    raise ValueError("The enumerations and definitions must be strings.")
            
            self._enums = v
        else:
            raise ValueError("The enumerations must be a list of tuples.")

    @property
    def default(self):
        """
        The default value for the string value of the item.
        """
        return self._default

    @default.setter
    def default(self, v):
        if v == None:
            self._length = v
        elif checkers.is_string(v):
            self._default = v
        else:
            raise ValueError("The default value must be a string or None.")

    def asXSD(self):
        """
        Return a XML Schema complexType definition.
        """
        indent = 2
        padding = ('').rjust(indent)
        xdstr = ''
        if self._adapter:
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
        xdstr += padding.rjust(indent + 6) + escape(self.docs.strip()) + '\n'
        xdstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'

        # add RDF
        xdstr += padding.rjust(indent + 6) + '<rdfs:Class rdf:about="mc-' + self.mcuid + '">\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model_3_1_0.xsd#XdStringType"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + quote(self.definition_url.strip()) + '"/>\n'
        if len(self.pred_obj_list) > 0:  # are there additional predicate-object definitions?
            for po in self.pred_obj_list:
                pred = po[0]
                obj = po[1]
                xdstr += padding.rjust(indent + 8) + '<' + pred.strip() + ' rdf:resource="' + quote(obj.strip()) + '"/>\n'
        xdstr += padding.rjust(indent + 6) + '</rdfs:Class>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
        xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdStringType">\n'
        xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
        # XdAny
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + self.label.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['act'][0]) + '" name="act" type="xs:string" default="' + self.act.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ExceptionalValue"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['vtb'][0]) + '" name="vtb" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['vte'][0]) + '" name="vte" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['tr'][0]) + '" name="tr" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['modified'][0]) + '" name="modified" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['location'][0]) + '" name="latitude" type="xs:decimal"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['location'][0]) + '" name="longitude" type="xs:decimal"/>\n'
        # XdStringType
        if isinstance(self.regex, str):
            xdstr += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='xdstring-value'>\n")
            xdstr += padding.rjust(indent + 12) + ("<xs:simpleType>\n")
            xdstr += padding.rjust(indent + 14) + ("<xs:restriction base='xs:string'>\n")
            xdstr += padding.rjust(indent + 16) + ("<xs:pattern value='" + self.regex.strip() + "'/>\n")
            xdstr += padding.rjust(indent + 14) + ("</xs:restriction>\n")
            xdstr += padding.rjust(indent + 12) + ("</xs:simpleType>\n")
            xdstr += padding.rjust(indent + 10) + ("</xs:element>\n")
        if not self.length == None:
            if isinstance(self.length, int):
                xdstr += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='xdstring-value'>\n")
                xdstr += padding.rjust(indent + 10) + ("<xs:simpleType>\n")
                xdstr += padding.rjust(indent + 12) + ("<xs:restriction base='xs:string'>\n")
                xdstr += padding.rjust(indent + 14) + ("<xs:length value='" + str(self.length).strip() + "'/>\n")
                xdstr += padding.rjust(indent + 12) + ("</xs:restriction>\n")
                xdstr += padding.rjust(indent + 10) + ("</xs:simpleType>\n")
                xdstr += padding.rjust(indent + 8) + ("</xs:element>\n")
            elif (self.length, tuple) and len(self.length) == 2:
                xdstr += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='xdstring-value'>\n")
                xdstr += padding.rjust(indent + 12) + ("<xs:simpleType>\n")
                xdstr += padding.rjust(indent + 14) + ("<xs:restriction base='xs:string'>\n")
                if isinstance(self.length[0], int):
                    xdstr += padding.rjust(indent + 16) + ("<xs:minLength value='" + str(self.length[0]).strip() + "'/>\n")
                if isinstance(self.length[1], int):
                    xdstr += padding.rjust(indent + 16) + ("<xs:maxLength value='" + str(self.length[1]).strip() + "'/>\n")
                xdstr += padding.rjust(indent + 14) + ("</xs:restriction>\n")
                xdstr += padding.rjust(indent + 12) + ("</xs:simpleType>\n")
                xdstr += padding.rjust(indent + 10) + ("</xs:element>\n")            
        elif self.default is not None and self.regex == None:
            xdstr += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='xdstring-value' type='xs:string' default='" + escape(self.default) + "'/>\n")
        else:
            xdstr += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='xdstring-value' type='xs:string'/>\n")
    
        # Process Enumerations
        if len(self.enums) > 0:    
            xdstr += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='xdstring-value'>\n")
            xdstr += padding.rjust(indent + 12) + ("<xs:simpleType>\n")
            xdstr += padding.rjust(indent + 14) + ("<xs:restriction base='xs:string'>\n")
            for n in range(len(self.enums)):
                xdstr += padding.rjust(indent + 16) + ("<xs:enumeration value='" + escape(self.enums[n][0].strip()) + "'>\n")
                xdstr += padding.rjust(indent + 16) + ("<xs:annotation>\n")
                xdstr += padding.rjust(indent + 18) + ("<xs:appinfo>\n")
                xdstr += padding.rjust(indent + 20) + ("<rdfs:Class rdf:about='mc-" + self.mcuid + "/xdstring-value/" + quote(self.enums[n][0].strip()) + "'>\n")
                xdstr += padding.rjust(indent + 20) + ("  <rdfs:subPropertyOf rdf:resource='mc-" + self.mcuid + "'/>\n")
                xdstr += padding.rjust(indent + 20) + ("  <rdfs:label>" + self.enums[n][0].strip() + "</rdfs:label>\n")
                xdstr += padding.rjust(indent + 20) + ("  <rdfs:isDefinedBy>" + self.enums[n][1].strip() + "</rdfs:isDefinedBy>\n")
                xdstr += padding.rjust(indent + 20) + ("</rdfs:Class>\n")
                xdstr += padding.rjust(indent + 18) + ("</xs:appinfo>\n")
                xdstr += padding.rjust(indent + 16) + ("</xs:annotation>\n")
                xdstr += padding.rjust(indent + 16) + ("</xs:enumeration>\n")
            xdstr += padding.rjust(indent + 14) + ("</xs:restriction>\n")
            xdstr += padding.rjust(indent + 12) + ("</xs:simpleType>\n")
            xdstr += padding.rjust(indent + 10) + ("</xs:element>\n")
    
        xdstr += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='0' name='xdstring-language' type='xs:language' default='" + self.xdstring_language + "'/>\n")
        
        xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
        xdstr += padding.rjust(indent) + '</xs:complexType>\n'

        return(xdstr)

    def asXML(self):
        """
        Return an example XML fragment for this model.
        """
        
        if len(self.enums) > 0:
            if self.default is not None:
                str_val = self.default
            else:
                str_val = random.choice(self.enums)[0]
        elif isinstance(self.length, int):
            str_val = 'w' * self.length
        elif isinstance(self.length, tuple):
            str_val = 'd' * self.length[0]  # insure to meet the minimum
        elif self.default is not None:
            str_val = self.default
        elif self.regex is not None:
            try:
                str_val = exrex.getone(self.regex)
            except:
                str_val = "Could not generate a valid example for the regex."
        else:
            str_val = 'Default String' # just a default
        
        act = random.choice(ex_acs)
        
        indent = 2
        padding = ('').rjust(indent)
        xmlstr = ''
        xmlstr += padding.rjust(indent) + '<ms-' + self.mcuid + '>\n'
        xmlstr += padding.rjust(indent + 2) + '<label>' + self.label + '</label>\n'
        if self.cardinality['act'][0] > 0:
            xmlstr += padding.rjust(indent + 2) + '<act>' + act + '</act>\n'
        if self.cardinality['vtb'][0] > 0:
            xmlstr += padding.rjust(indent + 2) + '<vtb>2006-06-04T18:13:51.0</vtb>\n'
        if self.cardinality['vte'][0] > 0:
            xmlstr += padding.rjust(indent + 2) + '<vte>2026-05-04T18:13:51.0</vte>\n'
        if self.cardinality['tr'][0] > 0:
            xmlstr += padding.rjust(indent + 2) + '<tr>2006-05-04T18:13:51.0</tr>\n'
        if self.cardinality['modified'][0] > 0:
            xmlstr += padding.rjust(indent + 2) + '<modified>2006-05-04T18:13:51.0</modified>\n'
        if self.cardinality['location'][0] > 0:
            xmlstr += padding.rjust(indent + 2) + '<latitude>-22.456</latitude>\n'
            xmlstr += padding.rjust(indent + 2) + '<longitude>123.654</longitude>\n'
        xmlstr += padding.rjust(indent + 2) + '<xdstring-value>' + str_val + '</xdstring-value>\n'
        if self.xdstring_language:
            xmlstr += padding.rjust(indent + 2) + '<xdstring-language>' + self.xdstring_language + '</xdstring-language>\n'
            
        xmlstr += padding.rjust(indent) + '</ms-' + self.mcuid + '>\n'
        
        # check for well-formed XML
        parser = etree.XMLParser()
        tree = etree.XML(xmlstr, parser)
        
        return(xmlstr)
    
    def asJSON(self):
        """
        Return an example JSON fragment for this model.
        """
        xml = self.asXML()
        parsed = xmltodict.parse(xml, encoding='UTF-8', process_namespaces=False)
        return(json.dumps(parsed, indent=2, sort_keys=False)) 


class XdFileType(XdAnyType):
    """
    A type to use for encapsulated content (aka. files) for image, audio and 
    other media types with a defined MIME type. 
    
    This type provides a choice of embedding the content into the data or using 
    a URL to point to the content.
    """

    def __init__(self, label):
        """
        The semantic label (name of the model) is required.
        """
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
        self.cardinality = ('hash_function', (0, 1))
        self.cardinality = ('alt_txt', (0, 1))

    @property
    def size(self):
        """
        Original size in bytes of unencoded encapsulated data. I.e. encodings 
        such as base64, hexadecimal, etc. 
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
        
        Coded from the IANA charcater set table: 
        http://www.iana.org/assignments/character-sets 
        
        Unicode is the default assumption in S3Model, with UTF-8 being the 
        assumed encoding. 
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
        
        Typically remains optional in the CMC and used at runtime when the 
        content is in a different language from the enclosing CMC.
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
        Name of the formalism or syntax used to inform an application regarding 
        a candidate parser to use on the content. 
        
        Examples might include: 'ATL', 'MOLA', 'QVT', 'GDL', 'GLIF', 'XML', etc.
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
        
        See IANA registered types: 
        http://www.iana.org/assignments/media-types/media-types.xhtml
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
        Compression/archiving mime-type. 
        
        If this elements does not exist then it means there is no 
        compression/archiving. 
        
        For a list of common mime-types for compression/archiving see: 
        http://en.wikipedia.org/wiki/List_of_archive_formats.
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
        Hash function result of the 'media-content'. 
        
        There must be a corresponding hash function type listed for this 
        to have any meaning. 
        
        See: http://en.wikipedia.org/wiki/List_of_hash_functions#Cryptographic_hash_functions
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
        URI reference to electronic information stored outside the record 
        as a file, database entry etc.; if supplied as a reference.
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
        The content, if stored locally. 
        
        The CMC modeler chooses either a uri or local content element.
        If the passed value is a string it will be converted to bytes and 
        base64 encoded. 
        
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

    def asXSD(self):
        """
        Return a XML Schema complexType definition.
        """
        indent = 2
        padding = ('').rjust(indent)
        xdstr = ''
        if self._adapter:
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
        xdstr += padding.rjust(indent + 6) + escape(self.docs.strip()) + '\n'
        xdstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'

        # add RDF
        xdstr += padding.rjust(indent + 6) + '<rdfs:Class rdf:about="mc-' + self.mcuid + '">\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model_3_1_0.xsd#XdFileType"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + quote(self.definition_url.strip()) + '"/>\n'
        if len(self.pred_obj_list) > 0:  # are there additional predicate-object definitions?
            for po in self.pred_obj_list:
                pred = po[0]
                obj = po[1]
                xdstr += padding.rjust(indent + 8) + '<' + pred.strip() + ' rdf:resource="' + quote(obj.strip()) + '"/>\n'
        xdstr += padding.rjust(indent + 6) + '</rdfs:Class>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
        xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdFileType">\n'
        xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
        # XdAny
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + self.label.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['act'][0]) + '" name="act" type="xs:string" default="' + self.act.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ExceptionalValue"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['vtb'][0]) + '" name="vtb" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['vte'][0]) + '" name="vte" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['tr'][0]) + '" name="tr" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['modified'][0]) + '" name="modified" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['location'][0]) + '" name="latitude" type="xs:decimal"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['location'][0]) + '" name="longitude" type="xs:decimal"/>\n'
        # XdFile
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="size" type="xs:int"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['encoding'][0]) + '" name="encoding" type="xs:string"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['xdfile_language'][0]) + '" name="xdfile-language" type="xs:language"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['formalism'][0]) + '" name="formalism" type="xs:string"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['media_type'][0]) + '" name="media-type" type="xs:string"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['compression_type'][0]) + '" name="compression-type" type="xs:string"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['hash_result'][0]) + '" name="hash-result" type="xs:string"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['hash_function'][0]) + '" name="hash-function" type="xs:string"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['alt_txt'][0]) + '" name="alt-txt" type="xs:string"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="uri" type="xs:anyURI"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="media-content" type="xs:base64Binary"/>\n'
        
        xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
        xdstr += padding.rjust(indent) + '</xs:complexType>\n'

        return(xdstr)

    def asXML(self):
        """
        Return an example XML fragment for this model.
        """
        
        act = random.choice(ex_acs)
        
        indent = 2
        padding = ('').rjust(indent)
        xmlstr = ''
        xmlstr += padding.rjust(indent) + '<ms-' + self.mcuid + '>\n'
        xmlstr += padding.rjust(indent + 2) + '<label>' + self.label + '</label>\n'
        if self.cardinality['act'][0] > 0:
            xmlstr += padding.rjust(indent + 2) + '<act>' + act + '</act>\n'
        if self.cardinality['vtb'][0] > 0:
            xmlstr += padding.rjust(indent + 2) + '<vtb>2006-06-04T18:13:51.0</vtb>\n'
        if self.cardinality['vte'][0] > 0:
            xmlstr += padding.rjust(indent + 2) + '<vte>2026-05-04T18:13:51.0</vte>\n'
        if self.cardinality['tr'][0] > 0:
            xmlstr += padding.rjust(indent + 2) + '<tr>2006-05-04T18:13:51.0</tr>\n'
        if self.cardinality['modified'][0] > 0:
            xmlstr += padding.rjust(indent + 2) + '<modified>2006-05-04T18:13:51.0</modified>\n'
        if self.cardinality['location'][0] > 0:
            xmlstr += padding.rjust(indent + 2) + '<latitude>-22.456</latitude>\n'
            xmlstr += padding.rjust(indent + 2) + '<longitude>123.654</longitude>\n'
        xmlstr += padding.rjust(indent + 2) + '<xdstring-value>' + str_val + '</xdstring-value>\n'
        if self.xdstring_language:
            xmlstr += padding.rjust(indent + 2) + '<xdstring-language>' + self.xdstring_language + '</xdstring-language>\n'
            
        xmlstr += padding.rjust(indent) + '</ms-' + self.mcuid + '>\n'
        
        # check for well-formed XML
        parser = etree.XMLParser()
        tree = etree.XML(xmlstr, parser)
        
        return(xmlstr)
    
    def asJSON(self):
        """
        Return an example JSON fragment for this model.
        """
        xml = self.asXML()
        parsed = xmltodict.parse(xml, encoding='UTF-8', process_namespaces=False)
        return(json.dumps(parsed, indent=2, sort_keys=False)) 

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
        """
        The semantic label (name of the model) is required.
        """
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

    def asXSD(self):
        """
        Return a XML Schema complexType definition.
        """
        indent = 2
        padding = ('').rjust(indent)
        xdstr = ''
        if self._adapter:
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
        xdstr += padding.rjust(indent + 6) + escape(self.docs.strip()) + '\n'
        xdstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'

        # add RDF
        xdstr += padding.rjust(indent + 6) + '<rdfs:Class rdf:about="mc-' + self.mcuid + '">\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model_3_1_0.xsd#XdOrdinalType"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + quote(self.definition_url.strip()) + '"/>\n'
        if len(self.pred_obj_list) > 0:  # are there additional predicate-object definitions?
            for po in self.pred_obj_list:
                pred = po[0]
                obj = po[1]
                xdstr += padding.rjust(indent + 8) + '<' + pred.strip() + ' rdf:resource="' + quote(obj.strip()) + '"/>\n'
        xdstr += padding.rjust(indent + 6) + '</rdfs:Class>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
        xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdOrdinalType">\n'
        xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
        # XdAny
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + self.label.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['act'][0]) + '" name="act" type="xs:string" default="' + self.act.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ExceptionalValue"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['vtb'][0]) + '" name="vtb" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['vte'][0]) + '" name="vte" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['tr'][0]) + '" name="tr" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['modified'][0]) + '" name="modified" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['location'][0]) + '" name="latitude" type="xs:decimal"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['location'][0]) + '" name="longitude" type="xs:decimal"/>\n'
        # Xd
        xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
        xdstr += padding.rjust(indent) + '</xs:complexType>\n'

        return(xdstr)


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
    Misuse: Not used for amounts of physical entities which all have standardized units as opposed to physical things counted.
    """

    def __init__(self, label):
        """
        The semantic label (name of the model) is required.
        """
        super().__init__(label)

        self._xdcount_value = None
        self._xdcount_units = None
        self.cardinality = ('xdcount_value', (0, 1))
        self.cardinality = ('xdcount_units', (1, 1))

    @property
    def xdcount_value(self):
        """
        Integer value of the counted items.
        """
        return self._xdcount_value

    @xdcount_value.setter
    def xdcount_value(self, v):
        if isinstance(v, int):
            self._xdcount_value = v
        else:
            raise ValueError("The xdcount_value value must be an integer.")

    @property
    def xdcount_units(self):
        """
        The name or type of the items counted. Examples are cigarettes, drinks, pregnancies, episodes, etc. 
        May or may not come from a standard terminology.
        """
        return self._xdcount_units

    @xdcount_units.setter
    def xdcount_units(self, v):
        if isinstance(v, XdStringType):
            self._xdcount_units = v
        else:
            raise ValueError("The xdcount_units value must be a XdStringType identifying the things to be counted.")

    def asXSD(self):
        """
        Return a XML Schema complexType definition.
        """
        indent = 2
        padding = ('').rjust(indent)
        xdstr = ''
        if self._adapter:
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
        xdstr += padding.rjust(indent + 6) + escape(self.docs.strip()) + '\n'
        xdstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'

        # add RDF
        xdstr += padding.rjust(indent + 6) + '<rdfs:Class rdf:about="mc-' + self.mcuid + '">\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model_3_1_0.xsd#XdCountType"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + quote(self.definition_url.strip()) + '"/>\n'
        if len(self.pred_obj_list) > 0:  # are there additional predicate-object definitions?
            for po in self.pred_obj_list:
                pred = po[0]
                obj = po[1]
                xdstr += padding.rjust(indent + 8) + '<' + pred.strip() + ' rdf:resource="' + quote(obj.strip()) + '"/>\n'
        xdstr += padding.rjust(indent + 6) + '</rdfs:Class>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
        xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdCountType">\n'
        xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
        # XdAny
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + self.label.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['act'][0]) + '" name="act" type="xs:string" default="' + self.act.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ExceptionalValue"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['vtb'][0]) + '" name="vtb" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['vte'][0]) + '" name="vte" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['tr'][0]) + '" name="tr" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['modified'][0]) + '" name="modified" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['location'][0]) + '" name="latitude" type="xs:decimal"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['location'][0]) + '" name="longitude" type="xs:decimal"/>\n'
        # Xd
        xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
        xdstr += padding.rjust(indent) + '</xs:complexType>\n'

        return(xdstr)


class XdQuantityType(XdQuantifiedType):
    """
    Quantified type representing specific quantities, i.e. quantities expressed as a magnitude and units. Can also be used for time durations, where it is more convenient to treat these as simply a number of individual seconds, minutes, hours, days, months, years, etc. when no temporal calculation is to be performed.
    """

    def __init__(self, label):
        """
        The semantic label (name of the model) is required.
        """
        super().__init__(label)

        self._xdquantity_value = None
        self._xdquantity_units = None
        self.cardinality = ('xdquantity_value', (0, 1))
        self.cardinality = ('xdquantity_units', (1, 1))

    @property
    def xdquantity_value(self):
        """
        Numeric value of the quantity.
        """
        return self._xdquantity_value

    @xdquantity_value.setter
    def xdquantity_value(self, v):
        if isinstance(v, float):
            self._xdquantity_value = v
        else:
            raise ValueError("The xdquantity_value value must be a decimal.")

    @property
    def xdquantity_units(self):
        """
        The name or type of the quantity. Examples are "kg/m2", “mmHg", "ms-1", "km/h". 
        May or may not come from a standard terminology.
        """
        return self._xdquantity_units

    @xdquantity_units.setter
    def xdquantity_units(self, v):
        if isinstance(v, XdStringType):
            self._xdquantity_units = v
        else:
            raise ValueError("The xdquantity_units value must be a XdStringType identifying the things to be measured.")

    def asXSD(self):
        """
        Return a XML Schema complexType definition.
        """
        indent = 2
        padding = ('').rjust(indent)
        xdstr = ''
        if self._adapter:
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
        xdstr += padding.rjust(indent + 6) + escape(self.docs.strip()) + '\n'
        xdstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'

        # add RDF
        xdstr += padding.rjust(indent + 6) + '<rdfs:Class rdf:about="mc-' + self.mcuid + '">\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model_3_1_0.xsd#XdQuantityType"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + quote(self.definition_url.strip()) + '"/>\n'
        if len(self.pred_obj_list) > 0:  # are there additional predicate-object definitions?
            for po in self.pred_obj_list:
                pred = po[0]
                obj = po[1]
                xdstr += padding.rjust(indent + 8) + '<' + pred.strip() + ' rdf:resource="' + quote(obj.strip()) + '"/>\n'
        xdstr += padding.rjust(indent + 6) + '</rdfs:Class>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
        xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdQuantityType">\n'
        xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
        # XdAny
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + self.label.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['act'][0]) + '" name="act" type="xs:string" default="' + self.act.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ExceptionalValue"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['vtb'][0]) + '" name="vtb" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['vte'][0]) + '" name="vte" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['tr'][0]) + '" name="tr" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['modified'][0]) + '" name="modified" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['location'][0]) + '" name="latitude" type="xs:decimal"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['location'][0]) + '" name="longitude" type="xs:decimal"/>\n'
        # Xd
        xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
        xdstr += padding.rjust(indent) + '</xs:complexType>\n'

        return(xdstr)


class XdFloatType(XdQuantifiedType):
    """
    Quantified type representing specific a value as a floating point number and optional units.
    """

    def __init__(self, label):
        """
        The semantic label (name of the model) is required.
        """
        super().__init__(label)

        self._xdfloat_value = None
        self._xdfloat_units = None
        self.cardinality = ('xdfloat_value', (0, 1))
        self.cardinality = ('xdfloat_units', (0, 1))

    @property
    def xdfloat_value(self):
        """
        Float value.
        """
        return self._xdfloat_value

    @xdfloat_value.setter
    def xdfloat_value(self, v):
        if isinstance(v, float):
            self._xdfloat_value = v
        else:
            raise ValueError("The xdfloat_value value must be a float.")

    @property
    def xdfloat_units(self):
        """
        The name or type of the float value.
        """
        return self._xdfloat_units

    @xdfloat_units.setter
    def xdfloat_units(self, v):
        if isinstance(v, XdStringType):
            self._xdfloat_units = v
        else:
            raise ValueError("The xdfloat_units value must be a XdStringType identifying the things to be measured.")

    def asXSD(self):
        """
        Return a XML Schema complexType definition.
        """
        indent = 2
        padding = ('').rjust(indent)
        xdstr = ''
        if self._adapter:
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
        xdstr += padding.rjust(indent + 6) + escape(self.docs.strip()) + '\n'
        xdstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'

        # add RDF
        xdstr += padding.rjust(indent + 6) + '<rdfs:Class rdf:about="mc-' + self.mcuid + '">\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model_3_1_0.xsd#XdFloatType"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + quote(self.definition_url.strip()) + '"/>\n'
        if len(self.pred_obj_list) > 0:  # are there additional predicate-object definitions?
            for po in self.pred_obj_list:
                pred = po[0]
                obj = po[1]
                xdstr += padding.rjust(indent + 8) + '<' + pred.strip() + ' rdf:resource="' + quote(obj.strip()) + '"/>\n'
        xdstr += padding.rjust(indent + 6) + '</rdfs:Class>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
        xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdFloatType">\n'
        xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
        # XdAny
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + self.label.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['act'][0]) + '" name="act" type="xs:string" default="' + self.act.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ExceptionalValue"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['vtb'][0]) + '" name="vtb" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['vte'][0]) + '" name="vte" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['tr'][0]) + '" name="tr" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['modified'][0]) + '" name="modified" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['location'][0]) + '" name="latitude" type="xs:decimal"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['location'][0]) + '" name="longitude" type="xs:decimal"/>\n'
        # Xd
        xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
        xdstr += padding.rjust(indent) + '</xs:complexType>\n'

        return(xdstr)


class XdRatioType(XdQuantifiedType):
    """
    Models a ratio of values, i.e. where the numerator and denominator are both pure numbers. Should not be used to represent things like blood pressure which are often written using a ‘/’ character, giving the misleading impression that the item is a ratio,
    when in fact it is a structured value. Similarly, visual acuity, often written as (e.g.) “20/20” in clinical notes is not a ratio but an ordinal (which includes non-numeric symbols like CF = count fingers etc). Should not be used for formulations. Used for modeling; ratios, rates or proportions.
    """

    def __init__(self, label):
        """
        The semantic label (name of the model) is required.
        """
        super().__init__(label)

        # constrained to list ['ratio','rate', 'proportion']
        self._ratio_type = None
        self._numerator = None
        self._denominator = None
        self._xdratio_value = None
        self._numerator_units = None
        self._denominator_units = None
        self._xdratio_units = None

        self.cardinality = ('ratio_type', (1, 1))
        self.cardinality = ('numerator', (0, 1))
        self.cardinality = ('denominator', (0, 1))
        self.cardinality = ('xdratio_value', (0, 1))
        self.cardinality = ('numerator_units', (0, 1))
        self.cardinality = ('denominator_units', (0, 1))
        self.cardinality = ('xdratio_units', (0, 1))

    @property
    def ratio_type(self):
        """
        Indicates specific type of ratio modeled in the DM as a 'ratio','rate', or 'proportion'.
        """
        return self._ratio_type

    @ratio_type.setter
    def ratio_type(self, v):
        if isinstance(v, str) and v in ['ratio', 'rate', 'proportion']:
            self._ratio_type = v
        else:
            raise ValueError("The ratio_type value must be a str and be one of; 'ratio','rate', or 'proportion'.")

    @property
    def numerator(self):
        """
        Numerator of ratio.
        """
        return self._numerator

    @numerator.setter
    def numerator(self, v):
        if isinstance(v, float):
            self._numerator = v
        else:
            raise ValueError("The numerator value must be a float.")

    @property
    def denominator(self):
        """
        Denominator of ratio.
        """
        return self._denominator

    @denominator.setter
    def denominator(self, v):
        if isinstance(v, float):
            self._denominator = v
        else:
            raise ValueError("The denominator value must be a float.")

    @property
    def xdratio_value(self):
        """
        Numeric value of the ratio.
        """
        return self._xdratio_value

    @xdratio_value.setter
    def xdratio_value(self, v):
        if isinstance(v, float):
            self._xdratio_value = v
        else:
            raise ValueError("The xdratio_value value must be a float.")

    @property
    def numerator_units(self):
        """
        Used to convey the meaning of the numerator. Typically countable units such as; cigarettes, drinks, 
        exercise periods, etc. May or may not come from a terminology.
        """
        return self._numerator_units

    @numerator_units.setter
    def numerator_units(self, v):
        if isinstance(v, XdStringType):
            self._numerator_units = v
        else:
            raise ValueError("The numerator_units value must be a XdStringType.")

    @property
    def denominator_units(self):
        """
        Used to convey the meaning of the denominator. Typically units such as; minutes, hours, days, years, months, etc. 
        May or may not come from a standard terminology.
        """
        return self._denominator_units

    @denominator_units.setter
    def denominator_units(self, v):
        if isinstance(v, XdStringType):
            self._denominator_units = v
        else:
            raise ValueError("The denominator_units value must be a XdStringType.")

    @property
    def xdratio_units(self):
        """
        Used to convey the meaning of the xdratio-value. May or may not come from a standard terminology.
        """
        return self._xdratio_units

    @xdratio_units.setter
    def xdratio_units(self, v):
        if isinstance(v, XdStringType):
            self._xdratio_units = v
        else:
            raise ValueError("The xdratio_units value must be a XdStringType.")

    def asXSD(self):
        """
        Return a XML Schema complexType definition.
        """
        indent = 2
        padding = ('').rjust(indent)
        xdstr = ''
        if self._adapter:
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
        xdstr += padding.rjust(indent + 6) + escape(self.docs.strip()) + '\n'
        xdstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'

        # add RDF
        xdstr += padding.rjust(indent + 6) + '<rdfs:Class rdf:about="mc-' + self.mcuid + '">\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model_3_1_0.xsd#XdRatioType"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + quote(self.definition_url.strip()) + '"/>\n'
        if len(self.pred_obj_list) > 0:  # are there additional predicate-object definitions?
            for po in self.pred_obj_list:
                pred = po[0]
                obj = po[1]
                xdstr += padding.rjust(indent + 8) + '<' + pred.strip() + ' rdf:resource="' + quote(obj.strip()) + '"/>\n'
        xdstr += padding.rjust(indent + 6) + '</rdfs:Class>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
        xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdRatioType">\n'
        xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
        # XdAny
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + self.label.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['act'][0]) + '" name="act" type="xs:string" default="' + self.act.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ExceptionalValue"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['vtb'][0]) + '" name="vtb" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['vte'][0]) + '" name="vte" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['tr'][0]) + '" name="tr" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['modified'][0]) + '" name="modified" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['location'][0]) + '" name="latitude" type="xs:decimal"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['location'][0]) + '" name="longitude" type="xs:decimal"/>\n'
        # Xd
        xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
        xdstr += padding.rjust(indent) + '</xs:complexType>\n'

        return(xdstr)


class XdTemporalType(XdOrderedType):
    """
    Type defining the concept of date and time types. 
    Must be constrained in DMs to be one or more of the below elements. 
    This gives the modeler the ability to optionally allow one or more types of temporal content such as 
    full or partial dates at run time. 
    Setting cardinality of both max and min to zero causes the element to be prohibited.
    """

    def __init__(self, label):
        """
        The semantic label (name of the model) is required.
        """
        super().__init__(label)
        self._xdtemporal_date = None
        self._xdtemporal_time = None
        self._xdtemporal_datetime = None
        self._xdtemporal_day = None
        self._xdtemporal_month = None
        self._xdtemporal_year = None
        self._xdtemporal_year_month = None
        self._xdtemporal_month_day = None
        self._xdtemporal_duration = None
        self.cardinality = ('xdtemporal_date', (0, 1))
        self.cardinality = ('xdtemporal_time', (0, 1))
        self.cardinality = ('xdtemporal_datetime', (0, 1))
        self.cardinality = ('xdtemporal_day', (0, 1))
        self.cardinality = ('xdtemporal_month', (0, 1))
        self.cardinality = ('xdtemporal_year', (0, 1))
        self.cardinality = ('xdtemporal_year_month', (0, 1))
        self.cardinality = ('xdtemporal_month_day', (0, 1))
        self.cardinality = ('xdtemporal_duration', (0, 1))

    @property
    def date(self):
        """
        Represents top-open intervals of exactly one day in length on the timelines of dateTime, 
        beginning on the beginning moment of each day, up to but not including the beginning moment of the next day). 
        For non-timezoned values, the top-open intervals disjointly cover the non-timezoned timeline, one per day. 
        For timezoned values, the intervals begin at every minute and therefore overlap.
        When serialized to XML or JSON the ISO format YYYY-MM-DD is used.
        """
        return self._date

    @date.setter
    def date(self, v):
        if isinstance(v, date):
            self._date = v
        else:
            raise ValueError("The date value must be a date type.")

    @property
    def time(self):
        """
        Represents instants of time (with or without a timezone) that recur at the same point in each calendar day, or that occur in some 
        arbitrary calendar day.
        """
        return self._time

    @time.setter
    def time(self, v):
        if isinstance(v, time):
            self._time = v
        else:
            raise ValueError("The time value must be a time type.")

    @property
    def datetime(self):
        """
        Represents instants of time, optionally marked with a particular time zone offset. 
        Values representing the same instant but having different time zone offsets are equal but not identical.
        """
        return self._datetime

    @datetime.setter
    def datetime(self, v):
        if isinstance(v, datetime):
            self._datetime = v
        else:
            raise ValueError("The datetime value must be a datetime type.")

    @property
    def day(self):
        """
        Represents whole days within an arbitrary month—days that recur at the same point in each (Gregorian) month. 
        This datatype is used to represent a specific day of the month as an integer. 
        To indicate, for example, that an employee gets a paycheck on the 15th of each month. 
        (Obviously, days beyond 28 cannot occur in all months; they are nonetheless permitted, up to 31.)        
        """
        return self._day

    @day.setter
    def day(self, v):
        if isinstance(v, int) and 1 <= v <= 31:
            self._day = v
        else:
            raise ValueError("The day value must be an integer type 1 - 31.")

    @property
    def month(self):
        """
        Represents whole (Gregorian) months within an arbitrary year—months that recur at the same point in each year. 
        It might be used, for example, to say what month annual Thanksgiving celebrations fall in different 
        countries (11 in the United States, 10 in Canada, and possibly other months in other countries).
        """
        return self._month

    @month.setter
    def month(self, v):
        if isinstance(v, int) and 1 <= v <= 12:
            self._month = v
        else:
            raise ValueError("The month value must be an integer type 1 - 12.")

    @property
    def year(self):
        """
        Represents Gregorian calendar years.
        """
        return self._year

    @year.setter
    def year(self, v):
        if isinstance(v, int) and 1 <= v <= 9999:
            self._year = v
        else:
            raise ValueError("The year value must be an integer type 1 - 9999.")

    @property
    def year_month(self):
        """
        Represents specific whole Gregorian months in specific Gregorian years.
        Represented as a tuple of integers (YYYY, MM).
        """
        return self._year_month

    @year_month.setter
    def year_month(self, v):
        if isinstance(v, tuple):
            if not 1 <= v[0] <= 9999 or not 1 <= v[1] <= 12:
                raise ValueError("The year_month value must be a tuple of integers representing 1 <= yyyy <= 9999 and 1 <= dd <= 12.")
            self._year_month = v
        else:
            raise ValueError("The year_month value must be a tuple of integers representing (yyyy,mm).")

    @property
    def month_day(self):
        """
        Represents whole calendar days that recur at the same point in each calendar year, or that occur in some 
        arbitrary calendar year. 
        (Obviously, days beyond 28 cannot occur in all Februaries; 29 is nonetheless permitted in February.)
        """
        return self._month_day

    @month_day.setter
    def month_day(self, v):
        max_days = {1:31,2:29,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
        if isinstance(v, tuple) and len(v) == 2 and isinstance(v[0], int) and isinstance(v[1], int):
            if not max_days[v[0]] <= v[1]:
                raise ValueError("The day value must be must be less than or equal to the number of days allowed in the month.")
            self._month_day = v
        else:
            raise ValueError("The month_day value must be a tuple of integers representing (mm,dd).")

    @property
    def duration(self):
        """
        A datatype that represents durations of time. The concept of duration being captured is drawn from those of 
        ISO-8601, specifically durations without fixed endpoints. 
        For example, "15 days" (whose most common lexical representation in duration is "'P15D'") is a duration value. 
        However, "15 days beginning 12 July 1995" and "15 days ending 12 July 1995" are not duration values. 
        This datatype can provide addition and subtraction operations between duration values and between 
        duration/datetime value pairs, and can be the result of subtracting datetime values.
        The tuple must include all values with a zero as a placeholder for unused positions.
        Example: 2 years, 10 days and 2 hours = (2,0,10,2,0,0). 
        Use these values in conjunction with the relativedelta type from the python-dateutil pkg.
        """
        return self._duration

    @duration.setter
    def duration(self, v):
        if isinstance(v, tuple) and len(v) == 6:
            if all(isinstance(n, int) for n in v[0:4]) and checkers.is_decimal(v[5]):
                self._duration = v
            else:
                raise ValueError("Some members of the duration tuple are not the correct type.")
        else:
            raise ValueError("The duration value must be a 6 member tuple (yyyy,mm,dd,hh,MM,ss.ss) of integers except the seconds (last member) being a decimal.")


    def asXSD(self):
        """
        Return a XML Schema complexType definition.
        """
        indent = 2
        padding = ('').rjust(indent)
        xdstr = ''
        if self._adapter:
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
        xdstr += padding.rjust(indent + 6) + escape(self.docs.strip()) + '\n'
        xdstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'

        # add RDF
        xdstr += padding.rjust(indent + 6) + '<rdfs:Class rdf:about="mc-' + self.mcuid + '">\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model_3_1_0.xsd#XdTemporalType"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + quote(self.definition_url.strip()) + '"/>\n'
        if len(self.pred_obj_list) > 0:  # are there additional predicate-object definitions?
            for po in self.pred_obj_list:
                pred = po[0]
                obj = po[1]
                xdstr += padding.rjust(indent + 8) + '<' + pred.strip() + ' rdf:resource="' + quote(obj.strip()) + '"/>\n'
        xdstr += padding.rjust(indent + 6) + '</rdfs:Class>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
        xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdTemporalType">\n'
        xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
        # XdAny
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + self.label.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['act'][0]) + '" name="act" type="xs:string" default="' + self.act.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ExceptionalValue"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['vtb'][0]) + '" name="vtb" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['vte'][0]) + '" name="vte" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['tr'][0]) + '" name="tr" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['modified'][0]) + '" name="modified" type="xs:dateTime"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['location'][0]) + '" name="latitude" type="xs:decimal"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="' + str(self.cardinality['location'][0]) + '" name="longitude" type="xs:decimal"/>\n'
        # Xd
        xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
        xdstr += padding.rjust(indent) + '</xs:complexType>\n'

        return(xdstr)

