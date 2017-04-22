==============================================
The Reference Implementation - Reference Model
==============================================

**Note:**  Any discrepancies between this document and the XML Schema implementation is to be resolved by the XML Schema RM. The automatically generated XML Schema documentation is available in PDF and downloadable HTML forms: http://S3Model.org/documents.html The sources are maintained on GitHub at https://github.com/S3Model/specs To get the most recent development version using git create a clone of https://github.com/S3Model/specs.git Then checkout the most recent branch.

Assumed Types
=============

There are several types that are assumed to be supported by the underlying implementation technology. These assumed types are based on XML Schema 1.1 Part 2 Datatypes. They should be available in your implementation language or add-on libraries. The names may or may not be exactly the same.

-----------------
Non-Ordered Types
-----------------

boolean
-------
Two state only.  Either true or false.


string
-------
The string data type can contain characters, line feeds, carriage returns, and tab characters.

anyURI
------
Specifies a Unique Resource Identifier (URI).

-----------------
Ordered types
-----------------

dateTime
--------
The dateTime data type is used to specify a date and a time.
The dateTime is specified in the following form "YYYY-MM-DDThh:mm:ss" where:

* YYYY indicates the year
* MM indicates the month
* DD indicates the day
* T indicates the start of the required time section
* hh indicates the hour
* mm indicates the minute
* ss indicates the second

The following is an example of a dateTime declaration in a schema::

    <xs:element name="startdate" type="xs:dateTime"/>

An element in your document might look like this::

    <startdate>2002-05-30T09:00:00</startdate>

Or it might look like this::

    <startdate>2002-05-30T09:30:10:05</startdate>

*Time Zones*

To specify a time zone, you can either enter a dateTime in UTC time by adding a "Z" behind the time - like this::

    <startdate>2002-05-30T09:30:10Z</startdate>

or you can specify an offset from the UTC time by adding a positive or negative time behind the time - like this::

    <startdate>2002-05-30T09:30:10-06:00</startdate> or
    <startdate>2002-05-30T09:30:10+06:00</startdate>

date
----
The date data type is used to specify a date.

The date is specified in the following form "YYYY-MM-DD" where:

* YYYY indicates the year
* MM indicates the month
* DD indicates the day

An element in an XML Document  might look like this::

    <start>2002-09-24</start>

time
----
The time data type is used to specify a time.
The time is specified in the following form "hh:mm:ss" where:

* hh indicates the hour
* mm indicates the minute
* ss indicates the second

The following is an example of a time declaration in a schema::

    <xs:element name="start" type="xs:time"/>

An element in your document might look like this::

    <start>09:00:00</start>

Or it might look like this::

    <start>09:30:10:05</start>


*Time Zones*

To specify a time zone, you can either enter a time in UTC time by adding a "Z" behind the time - like this::

    <start>09:30:10Z</start>

or you can specify an offset from the UTC time by adding a positive or negative time behind the time - like this::

    <start>09:30:10-06:00</start>  or  <start>09:30:10+06:00</start>

duration
--------

The duration data type is used to specify a time interval.
The time interval is specified in the following form "PnYnMnDTnHnMnS" where:

* P indicates the period (required)
* nY indicates the number of years
* nM indicates the number of months
* nD indicates the number of days
* T indicates the start of a time section (required if you are going to specify hours, minutes, or seconds)
* nH indicates the number of hours
* nM indicates the number of minutes
* nS indicates the number of seconds

The following is an example of a duration declaration in a schema::

    <xs:element name="period" type="xs:duration"/>

An element in your document might look like this::

    <period>P5Y</period>

The example above indicates a period of five years.
Or it might look like this::

    <period>P5Y2M10D</period>

The example above indicates a period of five years, two months, and 10 days.
Or it might look like this::

    <period>P5Y2M10DT15H</period>

The example above indicates a period of five years, two months, 10 days, and 15 hours.
Or it might look like this::

    <period>PT15H</period>

The example above indicates a period of 15 hours.

Negative Duration
-----------------

To specify a negative duration, enter a minus sign before the P::

    <period>-P10D</period>

The example above indicates a period of minus 10 days.

Partial Date Types
------------------
Support for partial dates is essential to avoid poor data quality. In order to provide for partial dates and times the following types are assumed to be available in the language or in a library.

* Day – provide on the day of the month, 1 – 31
* Month – provide only the month of the year, 1 – 12
* Year – provide on the year,  CCYY
* MonthDay – provide only the Month and the Day (no year)
* YearMonth – provide only the Year and the Month (no day)

real
----
The decimal data type is used to specify a numeric value.
Note: The maximum number of decimal digits you can specify is 18.

integer
-------
The integer data type is used to specify a numeric value without a fractional component.


3.0.0 Reference Model Documentation
===================================

The complete technical documentation is available `here <http://datainsights.tech/S3Model/docs/rm/index.html>`_.

---------------
RM complexTypes
---------------

The reference implementation complexType descriptions.

XdAnyType
-----------

**Derived from:**  n/a

**Abstract:** True

**Description:**  Serves as a common ancestor of all extended datatypes in S3Model models.

XdBooleanType
--------------

**Derived from:** XdAnyType by extension

**Abstract:** False

**Description:**  An enumerated type which represents boolean decisions. Such as true/false or yes/no answers. Useful where it is important to devise the meanings (usually questions in subjective data) carefully, so that the only allowed results are in fact true or false but are presented to the user as a list of options. The possible choices for True or False are enumerations in the DM. The reference model defines 'true' and 'false' in a choice so only one or the other may be present in the instance data. The XdBooleanType should not be used as a replacement for enumerated choice types such as male/female, etc. Such values should be modeled as XdStrings with enumerations and may reference a controlled vocabulary. In any case the enumeration often has more than two values. The elements, 'true' and 'false' are contained in an xs:choice and only one or the other is instantiated in the instance data with its value coming from the enumerations defined in a DM.

XdLinkType
----------

**Derived from:** XdAnyType by extension

**Abstract:** False

**Description:** Used to specify a Universal Resource Identifier.
Set the pattern facet to accommodate your needs in the PCM.
The primary use is to provide a mechanism that can be used to link together DMs.
The relation element allows for the use of a descriptive term for the link with an optional URI pointing to the source vocabulary. In most use cases the modeler will define all three of these using the 'fixed' attribute. Other use cases will have the 'relation' and 'relation-uri' elements fixed and the application will provide the 'link'.

XdStringType
------------

**Derived from:** XdAnyType by extension

**Abstract:** False

**Description:**  The string data type can contain characters, line feeds, carriage returns,
and tab characters. The use cases are for any free form text entry or for any enumerated lists. Additionally the minimum and maximum lengths may be set and regular expression patterns may be specified.

XdFileType
----------

**Derived from:** XdAnyType by extension

**Abstract:** False

**Description:** A type to use for encapsulated content (aka. files) for image, audio and other media types with a defined MIME type. This type provides a choice of embedding the content into the data or using a URL to point to the content.

XdOrderedType
-------------

**Derived from:** XdAnyType by extension

**Abstract:** True

**Description:**  Abstract class defining the concept of ordered values, which includes ordinals as well as true quantities. The implementations require the functions ‘<’, '>' and is_strictly_comparable_to ('==').

XdOrdinalType
-------------

**Derived from:** XdOrderedType by extension

**Abstract:** False

**Description:**  Models rankings and scores, e.g. pain, Apgar values, etc, where there is;

* implied ordering,
* no implication that the distance between each value is constant, and
* the total number of values is finite.

Note that although the term ‘ordinal’ in mathematics means natural numbers only, here any decimal is allowed, since negative and zero values are often used by medical and other professionals for values around a neutral point. Also, decimal values are sometimes used such as 0.5 or .25

Examples of sets of ordinal values;

* -3, -2, -1, 0, 1, 2, 3 -- reflex response values
* 0, 1, 2 -- Apgar values

Also used for recording any clinical or other datum which is customarily recorded using symbolic values. Examples;

* the results on a urinalysis strip, e.g. {neg, trace, +, ++, +++} are used for leukocytes, protein, nitrites etc;
* for non-haemolysed blood {neg, trace, moderate};
* for haemolysed blood {neg, trace, small, moderate, large}.

Elements ordinal and symbol MUST have exactly the same number of enumerations in the PCM.

XdQuantifiedType
----------------

**Derived from:** XdOrderedType by extension

**Abstract:** True

**Description:**  Abstract type defining the concept of true quantified values, i.e. values which are not only ordered, but which have a precise magnitude.

XdCountType
-----------

**Derived from:** XdQuantifiedType by extension

**Abstract:** False

**Description:** Countable quantities. Used for countable types such as pregnancies and steps (taken by a physiotherapy patient), number of cigarettes smoked in a day, etc.
The *thing(s)* being counted must be represented in the units element.

**Misuse:** Not used for amounts of physical entities (which all have standardized units).

XdQuantityType
--------------

**Derived from:** XdQuantifiedType by extension

**Abstract:** False

**Description:** Quantified type representing specific quantities, i.e. quantities expressed as a magnitude and units. Can also be used for time durations, where it is more convenient to treat these as simply a number of individual seconds, minutes, hours, days, months, years, etc. when no temporal calculation is to be performed.


XdRatioType
-----------

**Derived from:** XdQuantifiedType by extension

**Abstract:** False

**Description:** Models a ratio of values, i.e. where the numerator and denominator are both pure numbers. Should not be used to represent things like blood pressure which are often written using a forward slash ('/') character, giving the misleading impression that the item is a ratio, when in fact it is a structured value. Similarly, visual acuity, often written as (e.g.) “20/20” in clinical notes is not a ratio but an ordinal (which includes non-numeric symbols like CF = count fingers etc). Should not be used for formulations.


XdTemporalType
--------------

**Derived from:** XdOrderedType by extension

**Abstract:** False

**Description:** Type defining the concept of date and time types. Must be constrained in PCMs to be one or more of the below elements.  This gives the modeler the ability to optionally allow full or partial dates at run time.  Setting both maxOccurs and minOccurs to zero causes the element to be prohibited.


XdIntervalType
--------------

**Derived from:** XdAnyType by extension

**Abstract:** False

**Description:** Generic type defining an interval (i.e. range) of a comparable type. An interval is a contiguous subrange of a comparable base type. Used to define intervals of dates, times, quantities, etc. Whose datatypes are the same and are ordered. In S3Model, they are primarily used in defining reference ranges.


InvlType
--------

**Derived from:** n/a

**Abstract:** False

**Description:** In the DM, the modeler creates two restrictions on this complexType.
One for the 'lower' value and one for the 'upper' value.
Both restrictions will have the same element choice and the value is 'fixed' on each representing the lower and upper value range boundary. The value may be set to NULL (unbounded) by using the xsi:nil='true' attribute. The maxOccurs and minOccurs attributes must be set to 1, in the DM.

For more information on using this approach `see these tips <http://www.ibm.com/developerworks/webservices/library/ws-tip-null/index.html>`_

InvlUnits
---------

**Derived from:** n/a

**Abstract:** False

**Description:** The units designation for an Interval is slightly different than other complexTypes. This complexType is composed of a units name and a URI because in a ReferenceRange parent there can be different units for different ranges. Example: A XdQuantity of temperature can have a range in degrees Fahrenheit and one in degrees Celsius.
The derived complexType in the DM has these values fixed by the modeler.

ReferenceRangeType
------------------

**Derived from:** XdAnyType by extension

**Abstract:** False

**Description:** Defines a named range to be associated with any ORDERED datum. Each such
range is sensitive to the context, e.g. sex, age, location, and any other factor which affects ranges. May be used to represent high, low, normal, therapeutic, dangerous, critical, etc. ranges that are constrained by an interval.


AuditType
---------

**Derived from:** n/a

**Abstract:** False

**Description:** AuditType provides a mechanism to identify the who/where/when tracking of instances as they move from system to system.

PartyType
---------

**Derived from:** n/a

**Abstract:** False

**Description:** Description of a party, including an optional external link to data for this party in a demographic or other identity management system. An additional details element provides for the inclusion of information related to this party directly. If the party information is to be anonymous then do not include the details element.

AttestationType
---------------

**Derived from:** n/a

**Abstract:** False

**Description:** Record an attestation by a party of item(s) of record content. The type of attestation is recorded by the reason attribute, which may be coded.

ParticipationType
-----------------

**Derived from:** n/a

**Abstract:** False

**Description:** Model of a participation of a Party (any Actor or Role) in an activity. Used to represent any participation of a Party in some activity, which is not explicitly in the model, e.g. assisting nurse. Can be used to record past or future participations.

ExceptionalValueType
--------------------

**Derived from:** n/a

**Abstract:** True

**Description:** Subtypes are used to indicate why a value is missing (Null) or is outside a measurable range. The element ev-name is fixed in restricted types to a descriptive string. The subtypes defined in the reference model are considered sufficiently generic to be useful in many instances.

DMs may contain additional ExceptionalValueType restrictions to allow for domain related reasons for errant or missing data.


NIType
------

**Derived from:** ExceptionalValueType by restriction

**Abstract:** False

**Description:**  No Information: The value is exceptional (missing, omitted, incomplete, improper). No information as to the reason for being an exceptional value is provided. This is the most general exceptional value. It is also the default exceptional value.

MSKType
-------

**Derived from:** ExceptionalValueType by restriction

**Abstract:** False

**Description:**  Masked: There is information on this item available but it has not been provided by the sender due to security, privacy or other reasons. There may be an alternate mechanism for gaining access to this information.
.. Warning:
Using this exceptional value does provide information that may be a breach of confidentiality, even though no detail data is provided. Its primary purpose is for those circumstances where it is necessary to inform the receiver that the information does exist without providing any detail.

INVType
-------

**Derived from:** ExceptionalValueType by restriction

**Abstract:** False

**Description:**  Invalid: The value as represented in the instance is not a member of the set of permitted data values in the constrained value domain of a variable.

DERType
-------

**Derived from:** ExceptionalValueType by restriction

**Abstract:** False

**Description:**  Derived: An actual value may exist, but it must be derived from the provided information; usually an expression is provided directly.

UNCType
-------

**Derived from:** ExceptionalValueType by restriction

**Abstract:** False

**Description:**  Unencoded: No attempt has been made to encode the information correctly but the raw source information is represented, usually in free text.

OTHType
-------

**Derived from:** ExceptionalValueType by restriction

**Abstract:** False

**Description:**  Other: The actual value is not a member of the permitted data values in the variable. (e.g., when the value of the variable is not by the coding system)


NINFType
--------

**Derived from:** ExceptionalValueType by restriction

**Abstract:** False

**Description:**  Negative Infinity: Negative infinity of numbers


PINFType
--------

**Derived from:** ExceptionalValueType by restriction

**Abstract:** False

**Description:**  Positive Infinity: Positive infinity of numbers

UNKType
-------

**Derived from:** ExceptionalValueType by restriction

**Abstract:** False

**Description:**  Unknown: A proper value is applicable, but not known.

ASKRType
--------

**Derived from:** ExceptionalValueType by restriction

**Abstract:** False

**Description:**  Asked and Refused: Information was sought but refused to be provided (e.g., patient was asked but refused to answer)

NASKType
--------

**Derived from:** ExceptionalValueType by restriction

**Abstract:** False

**Description:**  Not Asked: This information has not been sought (e.g., patient was not asked)


QSType
------

**Derived from:** ExceptionalValueType by restriction

**Abstract:** False

**Description:**  Sufficient Quantity : The specific quantity is not known, but is known to non-zero and it is not specified because it makes up the bulk of the material; Add 10mg of ingredient X, 50mg of ingredient Y and sufficient quantity of water to 100mL.

TRCType
-------

**Derived from:** ExceptionalValueType by restriction

**Abstract:** False

**Description:**  Trace: The content is greater or less than zero but too small to be quantified.

ASKUType
--------

**Derived from:** ExceptionalValueType by restriction

**Abstract:** False

**Description:**  Asked but Unknown: Information was sought but not found (e.g., patient was asked but did not know)


NAVType
-------

**Derived from:** ExceptionalValueType by restriction

**Abstract:** False

**Description:** Not Available: This information is not available and the specific reason is not known.

NAType
------

**Derived from:** ExceptionalValueType by restriction

**Abstract:** False

**Description:**  Not Applicable: No proper value is applicable in this context e.g.,the number of cigarettes smoked per day by a non-smoker subject.

ItemType
--------

**Derived from:** n/a

**Abstract:** True

**Description:**  The abstract parent of ClusterType and XdAdapterType structural representation types.

ClusterType
-----------

**Derived from:** ItemType by extension

**Abstract:** False

**Description:**  The grouping variant of Item, which may contain further instances of Item,
in an ordered list. This can serve as the root component for arbitrarily complex structures.

XdAdapterType
-------------

**Derived from:** ItemType by extension

**Abstract:** False

**Description:**  The leaf variant of Item, to which any *XdAnyType* subtype instance is attached for use in a Cluster.

EntryType
---------

**Derived from:** n/a

**Abstract:** False

**Description:** An Entry is the root of a logical set of data items.

DMType
-------

**Derived from:** n/a

**Abstract:** False

**Description:**  This is the root node of a Data Model.

---------------
RM simpleTypes
---------------

The reference implementation simpleType descriptions.
These types do not have global element definitions. They are used to define other element types within the RM and are used as restrictions on a DM.

MagnitudeStatus
---------------

**Derived from:** xs:string

**Abstract:** False

**Description:** Optional status of magnitude with values::

        equal : magnitude is a point value

        less_than : value is less than the magnitude

        greater_than : value is greater than the magnitude

        less_than_or_equal : value is less_than_or_equal to the magnitude

        greater_than_or_equal : value is greater_than_or_equal to the magnitude

        approximate : value is the approximately the magnitude

These enumerations are used in they XdQuantifiedType subtypes.

TypeOfRatio
-----------

**Derived from:** xs:string

**Abstract:** False

**Description:** Indicates semantic type of ratio.

* ratio = a relationship between two numbers.
* proportion = a relationship between two numbers where there is a bi-univocal relationship between the numerator and the denominator (the numerator is contained in the denominator)
* rate = a relationship between two numbers where there is not a bi-univocal relationship between the numerator and the denominator (the numerator is not contained in the denominator)
