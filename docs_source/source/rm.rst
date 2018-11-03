==============================================
The Reference Implementation - Reference Model
==============================================

S3Model may be implemented in most (any?) programming or data definition language. This reference implementation provided here is in XML Schema due to the ubiquitous nature of XML Schema and the compatibility with RDF/XML. Virtually all programming and data analysis languages can manipulate and validate XML content.


**Note:**  Any discrepancies between this document and the XML Schema implementation, as documented by the link below, is to be resolved by the XML Schema RM. The automatically generated XML Schema documentation is available at the link below.

.. raw:: html

  <p><a href='rm/index.html' target='_blank'>Reference Model Technical Docs</a></p>


Assumed Types
=============

There are several types that are assumed to be supported by the underlying implementation technology. These assumed types are based on XML Schema Part 2 Datatypes. They should be available in your implementation language or add-on libraries. The names may or may not be exactly the same.

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

3.1.0 Reference Model Documentation
===================================

The reference implementation complexType descriptions. Click the word *Schema* to display a grahic representation of the type. 

-----------------------------------
ComplexTypes in the Reference Model
-----------------------------------

DMType 
------

`DMType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_DMType.html#DMType>`_

**Derived from:** n/a

**Abstract:** False

**Description:**  

This is the root, encapsulating node of a Data Model. The data model wraps the definitions for metadata about the model and it contains the metadata about the data. 

.. note::

    The *data content* is modeled as a document composed of the subtypes of `XdAnyType`_ with the structure based on the `ItemType`_ subtypes. 


The data content is generally quite flat and consistent when compared to other approaches. This aids the ability to perform queries and explore the data by separating the structure of the document from the semantics of any given concept.


**Model metadata** is information about the creation and usage of the data model. It is based on `Dublin Core <http://dublincore.org/>`_ definitons and includes:

- *title* `A name given to the resource <http://purl.org/dc/terms/title>`_.
- *creator* `An entity primarily responsible for making the resource <http://purl.org/dc/terms/creator>`_. 
- *subject* `The topic of the resource <http://purl.org/dc/terms/subject>`_.
- *rights* `Information about rights held in and over the resource <http://purl.org/dc/terms/rights>`_.
- *relation* `A related resource <http://purl.org/dc/terms/relation>`_.
- *coverage* `The spatial or temporal topic of the resource, the spatial applicability of the resource, or the jurisdiction under which the resource is relevant <http://purl.org/dc/terms/coverage>`_.
- *type* `The nature or genre of the resource <http://purl.org/dc/terms/type>`_.
- *identifier* `An unambiguous reference to the resource within a given context <http://purl.org/dc/terms/identifier>`_.
- *description* `An account of the resource <http://purl.org/dc/terms/description>`_.
- *publisher* `An entity responsible for making the resource available <http://purl.org/dc/terms/publisher>`_.
- *date* `A point or period of time associated with an event in the lifecycle of the resource <http://purl.org/dc/terms/date>`_. Here the date indicates date of publication.
- *format* `The file format, physical medium, or dimensions of the resource <http://purl.org/dc/terms/format>`_.
- *language* `A language of the resource <http://purl.org/dc/terms/language>`_.

The precise structure and content of **Data Metadata** is designed by the data modeler within a generic framework of components. This data metadata informs data consumers about what the data means. The many contextual aspects of the existence and life-cycle of the data may be recorded. 

The components are:

- An audit system based on the `AuditType`_ 
- An attestation system based on the `AttestationType`_ 
- The *subject* (person, role, organization, etc.) of the data activity based on the `PartyType`_
- The *provider* (person, role, organization, etc.) of the activity based on the `PartyType`_
- Other *participants* (persons, roles, organizations, etc.) of the activity based on the `ParticipationType`_ 
- A link to a protocol, policy or guideline used to outline or define the structure of the data based on `XdStringType`_
- A link to a workflow engine or vocabulary based on `XdLinkType`_
- A *current-state* element to contain the current state of the data based on the workflow engine or vocabulary as a string value
- A *label* string value element as a descriptive title for the model
- A *dm-encoding* element used to record the character set encoding of the data. The default is *utf-8*
- A *dm-language* element to indicate the primary langauge of the data.
- An *acs* element to point to an external Access Control System such as a controlled vocabulary. This vocabulary informs the values available for the *act* element in all `XdAnyType`_ subtypes.
- Optional external links based on `XdLinkType`_ may also be defined to expand information regarding the purpose, usage and relationships of this data. 


....

XdAnyType
---------

`XdAnyType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_XdAnyType.html#XdAnyType>`_

**Derived from:**  n/a

**Abstract:** True

**Description:**  

This datatype serves as the common ancestor of all eXtended data-types (Xd*) in S3Model. This eXtended Datatype provides the components for;
    - a *label* element with a language tag to provide a natural language meaningful name
    - an *act* (access control tag) element to provide a means of testing for access control levels at the granularity of the data item
    - one or more Exceptional Value Types (aka. NullFlavors) to add information regarding why a value may not validate with the data model schema but may still be useful data
    - a *vtb* (valid time begin) element to indicate a datetime when this data starts to be valid
    - a *vte* (valid time end) element to indicate a datetime when this data ceases to be valid
    - a *tr* (time recorded) element to indicate a datetime when this data is initially recorded
    - a *modified* element to indicate a datetime when this data was modified
    - a *latitude* element to record a decimal latitude value in the range of 90.000000 to -90.000000 of where the data originated 
    - a *longitude* element to record a decimal longitude value in the range of 180.000000 to -180.000000 of where the data originated


....

XdBooleanType
--------------

`XdBooleanType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_XdBooleanType.html#XdBooleanType>`_

**Derived from:** `XdAnyType`_ by extension

**Abstract:** False

**Description:**  

An enumerated type which represents boolean decisions. Such as true/false or yes/no answers. Useful where it is essential to devise the meanings (often questions in subjective data) carefully so that the only allowed result values result in one the options; true or false but are presented to the user as a list of options. The possible choices for True or False are enumerations in the DM. The reference model defines 'true-value' and 'false-value' in an xs:choice so only one or the other may be present in the instance data. 

The XdBooleanType should not be used as a replacement for enumerated choice types such as male/female, or similar choice sets. Such values should be modeled as XdStrings with enumerations and may reference a controlled vocabulary. In any case, the choice set often has more than two values. 

The elements, 'true-value' and 'false-value' are contained in an xs:choice and only one or the other is instantiated in the instance data with its value coming from the enumerations defined in a Data Model.

....

XdLinkType
----------

`XdLinkType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_XdLinkType.html#XdLinkType>`_

**Derived from:** `XdAnyType`_ by extension

**Abstract:** False

**Description:** 

Used to specify a Universal Resource Identifier.

Set the pattern facet to accommodate your needs in the `Reusable Model Component <abstract_model.html#rmc>`_.

The primary use is to provide a mechanism that can be used to link together Data Models or to link to external resources such as workflow and access control vocabularies.

The *relation* element allows for the use of a descriptive term for the link with an optional URI pointing to the source vocabulary. In most use cases the modeler will define all three of these using the *fixed* attribute. 

Other use cases will have the *relation* and *relation-uri* elements *fixed* and the application will provide the *link* data at runtime.

....

XdStringType
------------

`XdStringType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_XdStringType.html#XdStringType>`_

**Derived from:** `XdAnyType`_ by extension

**Abstract:** False

**Description:**  

The string data type can contain a string of characters or digits, line feeds, carriage returns, and tab characters. 

The use cases are for any free-form text entry, and for any enumerated lists. Additionally, the minimum, maximum and exact lengths may be set, and regular expression patterns may be specified to control the format of items such as ID numbers and telephone numbers.

In addition to the *xdstring-value* it includes a *xdstring-language* element for indicating that a language code is specific to this content.

....

XdFileType
----------

`XdFileType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_XdFileType.html#XdFileType>`_

**Derived from:** `XdAnyType`_ by extension

**Abstract:** False

**Description:** 

A type to use for encapsulated content such as files for images, audio and other media types with a defined MIME type. This type provides a choice of embedding the file content encoded in base64 or using a URL to point to the content. 

The following elements provide metadata information about the content:

- *size* is an integer that represents the unencoded content in bytes
- *encoding* is a string value from the `IANA character set table <http://www.iana.org/assignments/character-sets>`_. Unicode is the default assumption in S3Model, with UTF-8 being the assumed encoding. This element allows for variations from these assumptions.
- *xdfile-language* is an optional language code from `RFC 3066 <https://www.ietf.org/rfc/rfc3066.txt>`_. It is used to indicate the language of the content.
- *formalism* contains the name of the formalism or syntax used to inform an application regarding a candidate parser to use on the content. Examples might include: 'ATL', 'MOLA', 'QVT', 'GDL', 'GLIF', or other domain-specific language parser.
- *media-type* optionally contains the MIME type from the `IANA registered types <http://www.iana.org/assignments/media-types/media-types.xhtml>`_ 
- *compression-type* optionally contains the compression/archiving mime-type. If this element does not exist, then it means there is no compression/archiving. `Common mime-types for compression/archiving <http://en.wikipedia.org/wiki/List_of_archive_formats>`_.
- *hash-result* optionally contains a hash function result of the *media-content*. There must be a corresponding *hash-function* type listed for this to have any meaning. `Candidate list <http://en.wikipedia.org/wiki/List_of_hash_functions#Cryptographic_hash_functions>`_
- *hash-function* contains the hash function used to compute the content for *hash-result*. `Candidate list <http://en.wikipedia.org/wiki/List_of_hash_functions#Cryptographic_hash_functions>`_.
- *alt-txt* optionally contains the text to display in place of multimedia display or execution.

These two elements have a binary choice relationship. One and only one of them will appear in the model.

- *uri* contains a URI reference to electronic information stored outside the record as a file, database entry or other persistence methods when the content is supplied as a reference.
- *media-content* contains the file contents encoded using the base64Bianry algorithm.


....

XdOrderedType
-------------

`XdOrderedType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_XdOrderedType.html#XdOrderedType>`_

**Derived from:** `XdAnyType`_ by extension

**Abstract:** True

**Description:**  

An abstract class that defines the concept of ordered values, these items include ordinals as well as exact quantities. 
This type includes facilities for an optional list of ReferenceRanges for this value in its particular measurement context.

A *normal-status* element provides for a string indicating the string for a normal status in this context from range or interval of options.

....

XdOrdinalType
-------------

`XdOrdinalType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_XdOrdinalType.html#XdOrdinalType>`_

**Derived from:** `XdOrderedType`_ by extension

**Abstract:** False

**Description:**  

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

Elements *ordinal* and *symbol* MUST have the same number of enumerations in the `RMC <abstract_model.html#rmc>`_.

....

XdQuantifiedType
----------------

`XdQuantifiedType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_XdQuantifiedType.html#XdQuantifiedType>`_

**Derived from:** `XdOrderedType`_ by extension

**Abstract:** True

**Description:**  

An abstract type used for defining the concept of actual quantified values, i.e., values which are not only ordered but which have a precise magnitude. This type provides for facilities to indicate a magnitude-status to give a general idea of the accuracy of the quantity expressed in the XdQuantified subtypes. Should be used to inform users and not for decision support uses.

The optional element named error represents the error margin of measurement as an integer. This value indicates an error in the recording method or instrument (+/- %). A logical value of 0 indicates 100% accuracy, i.e., no error.

The optional accuracy element represents the accuracy of the value in the magnitude attribute in the range 0% to (+/-)100%. A value of 0 means that the accuracy is unknown.

....

XdCountType
-----------

`XdCountType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_XdCountType.html#XdCountType>`_

**Derived from:** `XdQuantifiedType`_ by extension

**Abstract:** False

**Description:** 

Used for countable quantities as an integer and a units value such as pregnancies and steps (taken by a physiotherapy patient), the number of cigarettes smoked in a day, etc. The name of the thing being counted must be represented in the units element.

**Misuse:** Not used for amounts of physical entities (which all have standardized units).

....

XdQuantityType
--------------

`XdQuantityType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_XdQuantityType.html#XdQuantityType>`_

**Derived from:** `XdQuantifiedType`_ by extension

**Abstract:** False

**Description:** 

A quantified type representing specific quantities, i.e., amounts expressed as magnitude as a decimal and units. This type can also be used for time durations where it is more convenient to treat these as some number of seconds, minutes, hours, days, months, years, etc. This use is only appropriate when the performance of temporal calculations is not required.

....

XdFloatType
--------------

`XdFloatType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_XdFloatType.html#XdFloatType>`_

**Derived from:** `XdQuantifiedType`_ by extension

**Abstract:** False

**Description:** 

Quantified type representing specific quantities as a magnitude as a float value and optional units. 


....


XdTemporalType
--------------

`XdTemporalType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_XdTemporalType.html#XdTemporalType>`_

**Derived from:** `XdOrderedType`_ by extension

**Abstract:** False

**Description:** 

This type defines the concept of dates and times. It must be constrained in an `RMC <abstract_model.html#rmc>`_ to be one or more of the below elements.  

This type gives the modeler the ability to allow full or partial dates at runtime. Each of the elements may be required, prohibited or allowed.

- *xdtemporal-date* represents top-open intervals of exactly one day in length on the timelines of dateTime, beginning on the beginning moment of each day, up to but not including the beginning moment of the next day). For values that do not have a timezone, the top-open intervals disjointly cover the timeline, one per day. For values with a time zone, the intervals begin at every minute and therefore overlap
- *xdtemporal-time* represents instants of time that recur at the same point in each calendar day, or that occur in some arbitrary calendar day.
- *xdtemporal-datetime* represents instants of time, optionally marked with a particular time zone offset. Values representing the same instant but having different time zone offsets are equal but not identical
- *xdtemporal-day* represents whole days within an arbitrary month—days that recur at the same point in each (Gregorian) month. This datatype is used to represent a specific day of the month. To indicate, for example, that an employee gets a paycheck on the 15th of each month. (Obviously, days beyond 28 cannot occur in all months; they are nonetheless permitted, up to 31.)</xs:documentation>
- *xdtemporal-month* represents whole (Gregorian) months within an arbitrary year—months that recur at the same point in each year. This type is used, for example, to say what month annual Thanksgiving celebrations fall in different countries (--11 in the United States, --10 in Canada, and possibly other months in other countries).
- *xdtemporal-year* represents Gregorian calendar years.
- *xdtemporal-year-month* represents Gregorian calendar years.
- *xdtemporal-month-day* represents whole calendar days that recur at the same point in each calendar year, or that occur in some arbitrary calendar year. (Obviously, days beyond 28 cannot occur in all Februaries; 29 is nonetheless permitted.)
- *xdtemporal-duration* represents durations of time. The concept of duration being captured is drawn from those of [ISO 8601], specifically durations without fixed endpoints. For example, "15 days" (whose most common lexical representation in duration is "'P15D'") is a duration value; "15 days beginning 12 July 1995" and "15 days ending 12 July 1995" are not duration values. This datatype can provide addition and subtraction operations between duration values and between duration/dateTime value pairs and can be the result of subtracting dateTime values.


....

XdIntervalType
--------------

`XdIntervalType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_XdIntervalType.html#XdIntervalType>`_

**Derived from:** `XdAnyType`_ by extension

**Abstract:** False

**Description:** 

This is a generic type that defines an interval (i.e., range) of a comparable nature. An interval is a contiguous subrange of an equivalent base type. Used to determine intervals of dates, times, quantities, etc. Whose datatypes are the same and are ordered. In S3Model, this type is primarily used in defining an interval for reference ranges.

....

InvlType
--------

`InvlType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_InvlType.html#InvlType>`_

**Derived from:** n/a

**Abstract:** False

**Description:** 

In the Data Model, the modeler creates two restrictions on this complexType. One for the 'lower' value and one for the 'upper' value.

Both restrictions will have the same element choice, and the value is 'fixed' on each representing the lower value and the upper value range boundaries. When the value is set to NULL by using the xsi:nil='true' attribute, the maxOccurs and minOccurs attributes must be set to 1, in the Data Model.

For more information on using this approach `see these tips <https://www.ibm.com/developerworks/webservices/library/ws-tip-null/index.html>`_

....

InvlUnits
---------

`InvlUnits Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_InvlUnits.html#InvlUnits>`_

**Derived from:** n/a

**Abstract:** False

**Description:** 

The units designation for an Interval is slightly different than other complexTypes. This complexType is composed of a units name and a URI because in a reference range parent there can be different units for different ranges. Example: A XdQuantity of temperature can have a range of degrees Fahrenheit and one in degrees Celsius.

The derived type in the Data Model has these values fixed by the modeler.

....

ReferenceRangeType
------------------

`ReferenceRangeType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_ReferenceRangeType.html#ReferenceRangeType>`_

**Derived from:** `XdAnyType`_ by extension

**Abstract:** False

**Description:** 

This type defines a named range associated with any ORDERED datum. 

Each such range is sensitive to the context, e.g., sex, age, location, and any other factor which affects ranges. May be used to representing high, low, normal, therapeutic, dangerous, critical, etc. ranges that are constrained by an interval.


....

AuditType
---------

`AuditType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_AuditType.html#AuditType>`_

**Derived from:** n/a

**Abstract:** False

**Description:** 

The AuditType provides a mechanism to identify the who/where/when tracking of instances as they move from system to system.

....

PartyType
---------

`PartyType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_PartyType.html#PartyType>`_

**Derived from:** n/a

**Abstract:** False

**Description:** 

Description of a party, including an optional external link to data for this party in a demographic or other identity management system. An additional details element provides for the inclusion of information related to this party directly. If the party information is to be anonymous, then do not include the details element.

....

AttestationType
---------------

`AttestationType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_AttestationType.html#AttestationType>`_

**Derived from:** n/a

**Abstract:** False

**Description:** 

Record an attestation by a party of item(s) of record content. The type of attestation is recorded by the reason attribute, which may be coded.

....

ParticipationType
-----------------

`ParticipationType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_ParticipationType.html#ParticipationType>`_

**Derived from:** n/a

**Abstract:** False

**Description:** 

Model of participation of a Party (any Actor or Role) in an activity. Used to represent any involvement of a Party in some event, which is not explicitly in the model, e.g., assisting nurse, law clerk, accounting firm, etc. Can be used to record past or future participations.

....

ExceptionalValueType
--------------------

`ExceptionalValueType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_ExceptionalValueType.html#ExceptionalValueType>`_

**Derived from:** n/a

**Abstract:** True

**Description:** 

Subtypes are used to indicate why a value is missing (Null) or is outside a measurable range. The element named *ev-name* has its value fixed in restricted types to a descriptive string. The subtypes defined in the reference model are considered sufficiently generic to be useful in many instances. The original set of subtypes are based on Null Flavour types from `ISO 21090 <https://www.iso.org/standard/35646.html>`_. 

Data Models may contain additional `ExceptionalValueType`_ restrictions to allow for domain related reasons for errant or missing data.


....

NIType
------

`NIType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_NIType.html#NIType>`_

**Derived from:** `ExceptionalValueType`_ by restriction

**Abstract:** False

**Description:**  

*No Information*: The value is exceptional (missing, omitted, incomplete, improper). No information as to the reason for being an exceptional value is provided. This is the most general exceptional value. It is also the default exceptional value.

....

MSKType
-------

`MSKType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_MSKType.html#MSKType>`_

**Derived from:** `ExceptionalValueType`_ by restriction

**Abstract:** False

**Description:**  

*Masked*: There is information on this item available but it has not been provided by the sender due to security, privacy or other reasons. There may be an alternate mechanism for gaining access to this information.
.. Warning:
Using this exceptional value does provide information that may be a breach of confidentiality, even though no detail data is provided. Its primary purpose is for those circumstances where it is necessary to inform the receiver that the information does exist without providing any detail.

....

INVType
-------

`INVType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_INVType.html#INVType>`_

**Derived from:** `ExceptionalValueType`_ by restriction

**Abstract:** False

**Description:**  

*Invalid*: The value as represented in the instance is not a member of the set of permitted data values in the constrained value domain of a variable.

....

DERType
-------

`DERType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_DERType.html#DERType>`_

**Derived from:** `ExceptionalValueType`_ by restriction

**Abstract:** False

**Description:**  

*Derived*: An actual value may exist, but it must be derived from the provided information; usually an expression is provided directly.

....

UNCType
-------

`UNCType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_UNCType.html#UNCType>`_

**Derived from:** `ExceptionalValueType`_ by restriction

**Abstract:** False

**Description:**  

*Unencoded*: No attempt has been made to encode the information correctly but the raw source information is represented, usually in free text.

....

OTHType
-------

`OTHType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_OTHType.html#OTHType>`_

**Derived from:** `ExceptionalValueType`_ by restriction

**Abstract:** False

**Description:**  

*Other*: The actual value is not a member of the permitted data values in the variable. (e.g., when the value of the variable is not by the coding system)


....

NINFType
--------

`NINFType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_NINFType.html#NINFType>`_

**Derived from:** `ExceptionalValueType`_ by restriction

**Abstract:** False

**Description:**  

*Negative Infinity*: Negative infinity of numbers


....

PINFType
--------

`PINFType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_PINFType.html#PINFType>`_

**Derived from:** `ExceptionalValueType`_ by restriction

**Abstract:** False

**Description:**  

*Positive Infinity*: Positive infinity of numbers

....

UNKType
-------

`UNKType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_UNKType.html#UNKType>`_

**Derived from:** `ExceptionalValueType`_ by restriction

**Abstract:** False

**Description:**  

*Unknown*: A proper value is applicable, but not known.

....

ASKRType
--------

`ASKRType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_ASKRType.html#ASKRType>`_

**Derived from:** `ExceptionalValueType`_ by restriction

**Abstract:** False

**Description:**  

*Asked and Refused*: Information was sought but refused to be provided (e.g., patient was asked but refused to answer)

....

NASKType
--------

`NASKType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_NASKType.html#NASKType>`_

**Derived from:** `ExceptionalValueType`_ by restriction

**Abstract:** False

**Description:**  

*Not Asked*: This information has not been sought (e.g., patient was not asked)


....

QSType
------

`QSType Schema </rm/s3model_3_1_0_xsd_Complex_Type_s3m_QSType.html#QSType>`_

**Derived from:** `ExceptionalValueType`_ by restriction

**Abstract:** False

**Description:**  

*Sufficient Quantity*: The specific quantity is not known, but is known to non-zero and it is not specified because it makes up the bulk of the material; Add 10mg of ingredient X, 50mg of ingredient Y and sufficient quantity of water to 100mL.

....

TRCType
-------

`TRCType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_TRCType.html#TRCType>`_

**Derived from:** `ExceptionalValueType`_ by restriction

**Abstract:** False

**Description:**  

*Trace*: The content is greater or less than zero but too small to be quantified.

....

ASKUType
--------

`ASKUType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_ASKUType.html#ASKUType>`_

**Derived from:** `ExceptionalValueType`_ by restriction

**Abstract:** False

**Description:**  

*Asked but Unknown*: Information was sought but not found (e.g., patient was asked but did not know)


....

NAVType
-------

`NAVType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_NAVType.html#NAVType>`_

**Derived from:** `ExceptionalValueType`_ by restriction

**Abstract:** False

**Description:** 

*Not Available*: This information is not available and the specific reason is not known.

....

NAType
------

`NAType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_NAType.html#NAType>`_

**Derived from:** `ExceptionalValueType`_ by restriction

**Abstract:** False

**Description:**  

*Not Applicable*: No proper value is applicable in this context e.g.,the number of cigarettes smoked per day by a non-smoker subject.

....

ItemType
--------

`ItemType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_ItemType.html#ItemType>`_

**Derived from:** n/a

**Abstract:** True

**Description:**  

The abstract parent of `ClusterType`_ and `XdAdapterType`_ structural representation types.

....

ClusterType
-----------

`ClusterType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_ClusterType.html#ClusterType>`_

**Derived from:** `ItemType`_ by extension

**Abstract:** False

**Description:**  

The grouping component of `ItemType`_, which may contain further instances of `ItemType`_,
in an ordered list. This can serve as the root component for arbitrarily complex structures used to model data content as well as *data metadata* components.

....

XdAdapterType
-------------

`XdAdapterType Schema <rm/s3model_3_1_0_xsd_Complex_Type_s3m_XdAdapterType.html#XdAdapterType>`_

**Derived from:** `ItemType`_ by extension

**Abstract:** False

**Description:**  

An adapter/container, to which any `XdAnyType`_ subtype instance is attached for use in a `ClusterType`_.


....


---------------
RM simpleTypes
---------------

The reference implementation simpleType descriptions. These types do not have global element definitions. They are used to define other element types within the `RM <abstract_model.html#rm>`_ and are used as restrictions on a Data Model.

MagnitudeStatus
---------------

`MagnitudeStatus Schema <rm/s3model_3_1_0_xsd_Simple_Type_s3m_MagnitudeStatus.html#MagnitudeStatus>`_

**Derived from:** xs:string

**Abstract:** False

**Description:** 

Optional status of magnitude with values::

        *equal* : magnitude is a point value

        *less_than* : value is less than the magnitude

        *greater_than* : value is greater than the magnitude

        *less_than_or_equal* : value is less_than_or_equal to the magnitude

        *greater_than_or_equal* : value is greater_than_or_equal to the magnitude

        *approximate* : value is the approximately the magnitude

These enumerations are used in the *magnitude-status* element of the `XdQuantifiedType`_ subtypes.

