"""
Defines the S3Model RM XSD reference model in Python 3.7
"""
from datetime import datetime, date, time
from dataclasses import dataclass, field
from cuid import cuid
from decimal import Decimal
import ontology

@dataclass
class ExceptionalValue(object):
    """
    Subtypes are used to indicate why a value is missing (Null) or is outside a measurable range. The element ev-name is fixed in restricted types to a descriptive string. The subtypes defined in the reference model are considered sufficiently generic to be
    useful in many instances. Data Models may contain additional ExceptionalValueType restrictions to allow for domain related reasons for errant or missing data.
    """
    ev_name: str
   

@dataclass
class XdAnyType(object):
    """
    Serves as an abstract common ancestor of all eXtended data-types (Xd*) in S3Model.
    """
    mcuid: str = field(default_factory=cuid)
    label: str = field(default='', metadata={'min':1, 'max': 1, 'lang': 'en-US'})
    act: str = field(default='', metadata={'min':0, 'max': 1})
    ev: ExceptionalValue = field(default=None, metadata={'min':0, 'max': 1})
    vtb: datetime = field(default=None, metadata={'min':0, 'max': 1})
    vte: datetime = field(default=None, metadata={'min':0, 'max': 1})
    tr: datetime = field(default=None, metadata={'min':0, 'max': 1})
    modified: datetime = field(default=None, metadata={'min':0, 'max': 1})
    latitude: Decimal = field(default=None, metadata={'min':0, 'max': 1})
    longitude: Decimal = field(default=None, metadata={'min':0, 'max': 1})
    
@dataclass
class InvlUnits(XdAnyType):
    """
    The units designation for an Interval is slightly different than other complexTypes. This complexType is composed of a units name and a URI because in a ReferenceRange parent there can be different units for different ranges. Example: A XdQuantity of
    temperature can have a range in degrees Fahrenheit and one in degrees Celsius. The derived complexType in the CMC has these values fixed by the modeler.
    """
    units_name: str = field(default='', metadata={'min':1, 'max': 1, 'lang': 'en-US'})
    units_uri: str = field(default='', metadata={'min':1, 'max': 1})

    
@dataclass
class XdIntervalType(XdAnyType):
    """
    Generic type defining an interval (i.e. range) of a comparable type. An interval is a contiguous subrange of a 
    comparable base type. Used to define intervals of dates, times, quantities, etc. Whose datatypes are the same and 
    are ordered. In S3Model, they are primarily used in defining reference ranges. The type of upper and lower must be set in the DM.
    """
    lower: Any = field(default=None, metadata={'min':0, 'max': 1})
    upper: Any = field(default=None, metadata={'min':0, 'max': 1})
    lower_included: bool = field(default=None, metadata={'min':1, 'max': 1})
    upper_included: boo1 = field(default=None, metadata={'min':1, 'max': 1})
    lower_bounded: bool = field(default=None, metadata={'min':1, 'max': 1})
    upper_bounded: boo1 = field(default=None, metadata={'min':1, 'max': 1})
    interval_units: InvlUnits = field(default=None, metadata={'min':1, 'max': 1})

    
@dataclass
class ReferenceRangeType(XdAnyType):
    """
    Defines a named range to be associated with any ORDERED datum. Each such range is sensitive to the context, 
    e.g. sex, age, location, and any other factor which affects ranges. 
    May be used to represent high, low, normal, therapeutic, dangerous, critical, etc. ranges that are constrained by an interval.
    """
    definition: str = field(default='', metadata={'min':1, 'max': 1})
    interval: XdIntervalType = field(default=None, metadata={'min':1, 'max': 1})
    is_normal: bool = field(default=None, metadata={'min':1, 'max': 1})

@dataclass
class XdBooleanType(XdAnyType):
    """
    An enumerated type which represents boolean decisions. Such as true/false or yes/no answers. Useful where it is essential to devise the meanings (often questions in subjective data) carefully so that the only allowed result values result in one the options; true or false but are presented to the user as a list of options. The possible choices for True or False are enumerations in the DM. The reference model defines 'true-value' and 'false-value' in an xs:choice so only one or the other may be present in the instance data. 
    The XdBooleanType should not be used as a replacement for enumerated choice types such as male/female, or similar choice sets. Such values should be modeled as XdStrings with enumerations and may reference a controlled vocabulary. In any case, the choice set often has more than two values. 
    The elements, 'true-value' and 'false-value' are contained in an xs:choice and only one or the other is instantiated in the instance data with its value coming from the enumerations defined in a Data Model.
    """
    # choice of true_value or false_value
    true_value: str = field(default='', metadata={'min':0, 'max': 1})
    false_value: str = field(default='', metadata={'min':0, 'max': 1})


@dataclass
class XdLinkType(XdAnyType):
    """
    Used to specify a Universal Resource Identifier. Set the pattern facet to accommodate your needs in the DM. Intended use is to provide a mechanism that can be used to link together Concept Models. The relation element allows for the use of a descriptive
    term for the link with an optional URI pointing to the source vocabulary. In most usecases the modeler will define all three of these using the 'fixed' attribute. Other usecases will have the 'relation' and 'relation-uri' elements fixed and the application will provide the 'link-value'.
    """
    link: str = field(default='', metadata={'min':1, 'max': 1})
    relation: str = field(default='', metadata={'min':1, 'max': 1})
    relation_uri: str = field(default='', metadata={'min':0, 'max': 1})
    
    
@dataclass
class XdStringType(XdAnyType):
    """
    The string data type can contain characters, line feeds, carriage returns, and tab characters. The use cases are for any free form text entry or for any enumerated lists. Additionally the minimum and maximum lengths may be set and regular expression patterns  may be specified.
    """
    xdstring_value: str = field(default='', metadata={'min':0, 'max': 1})
    xdstring_language: str = field(default='', metadata={'min':0, 'max': 1})



@dataclass
class XdFileType(XdAnyType):
    """
    A type to use for encapsulated content (aka. files) for image, audio and other media types with a defined MIME type. This type provides a choice of embedding the content into the data or using a URL to point to the content.
    """
    size: int = field(default=None, metadata={'min':1, 'max': 1})
    encoding: str = field(default='', metadata={'min':0, 'max': 1})
    xdfile_language: str = field(default='', metadata={'min':0, 'max': 1})
    formalism: str = field(default='', metadata={'min':0, 'max': 1})
    media_type: str = field(default='', metadata={'min':0, 'max': 1})
    compression_type: str = field(default='', metadata={'min':0, 'max': 1})
    hash_result: str = field(default='', metadata={'min':0, 'max': 1})
    hash_function: str = field(default='', metadata={'min':0, 'max': 1})
    alt_txt: str = field(default='', metadata={'min':0, 'max': 1})
    # choice of uri or media_content
    uri: str = field(default='', metadata={'min':1, 'max': 1})
    media_content: bytes = field(default=None, metadata={'min':1, 'max': 1})


@dataclass
class XdOrderedType(XdAnyType):
    """
    Serves as an abstract common ancestor of all ordered types
    """
    referencerange: ReferenceRangeType = field(default=None, metadata={'min':0, 'max': 1})
    normal_status: str = field(default='', metadata={'min':0, 'max': 1})


@dataclass
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
    ordinal: Decimal = field(default=None, metadata={'min':1, 'max': 1})
    symbol: str = field(default=None, metadata={'min':1, 'max': 1})


@dataclass
class XdQuantifiedType(XdOrderedType):
    """
    Serves as an abstract common ancestor of all quantifiable types
    """
    # constrained to list [None,'equal','less_than', 'greater_than', 'less_than_or_equal', 'greater_than_or_equal', 'approximate']
    magnitude_status: str = field(default=None, metadata={'min':0, 'max': 1})
    error: int = field(default=None, metadata={'min':0, 'max': 1})
    accuracy: Decimal = field(default=None, metadata={'min':0, 'max': 1})


@dataclass
class XdCountType(XdQuantifiedType):
    """
    Countable quantities. Used for countable types such as pregnancies and steps (taken by a physiotherapy patient), number of cigarettes smoked in a day, etc. The thing(s) being counted must be represented in the units element. Misuse:Not used for amounts of physical entities (which all have standardized units).
    """
    xdcount_value: int = field(default=None, metadata={'min':0, 'max': 1})
    xdcount_units: XdStringType = field(default=None, metadata={'min':1, 'max': 1})


@dataclass
class XdQuantityType(XdQuantifiedType):
    """
    Quantified type representing specific quantities, i.e. quantities expressed as a magnitude and units. Can also be used for time durations, where it is more convenient to treat these as simply a number of individual seconds, minutes, hours, days, months, years, etc. when no temporal calculation is to be performed.
    """
    xdquantity_value: int = field(default=None, metadata={'min':0, 'max': 1})
    xdquantity_units: XdStringType = field(default=None, metadata={'min':1, 'max': 1})


@dataclass
class XdFloatType(XdQuantifiedType):
    """
    Quantified type representing specific a value as a floating point number and optional units.
    """
    xdfloat_value: float = field(default=None, metadata={'min':0, 'max': 1})
    xdfloat_units: XdStringType = field(default=None, metadata={'min':1, 'max': 1})
    
    
@dataclass
class XdRatioType(XdQuantifiedType):
    """
    Models a ratio of values, i.e. where the numerator and denominator are both pure numbers. Should not be used to represent things like blood pressure which are often written using a ‘/’ character, giving the misleading impression that the item is a ratio,
    when in fact it is a structured value. Similarly, visual acuity, often written as (e.g.) “20/20” in clinical notes is not a ratio but an ordinal (which includes non-numeric symbols like CF = count fingers etc). Should not be used for formulations. Used for modeling; ratios, rates or proportions.
    """
    # constrained to list ['ratio','rate', 'proportion']    
    ratio_type: str = field(default=None, metadata={'min':1, 'max': 1})
    numerator: float = field(default=None, metadata={'min':0, 'max': 1})
    denominator: float = field(default=None, metadata={'min':0, 'max': 1})
    xdratio_value: float = field(default=None, metadata={'min':0, 'max': 1})
    numerator_units: XdStringType = field(default=None, metadata={'min':0, 'max': 1})
    denominator_units: XdStringType = field(default=None, metadata={'min':0, 'max': 1})
    xdratio_units: XdStringType = field(default=None, metadata={'min':0, 'max': 1})
    

@dataclass
class XdTemporalType(XdOrderedType):
    """
    Type defining the concept of date and time types. Must be constrained in DMs to be one or more of the below elements. This gives the modeler the ability to optionally allow full or partial dates at run time. Setting both maxOccurs and minOccurs to zero cause the element to be prohibited.
    """
    # TODO: fix the types
    xdtemporal_date: date = field(default=None, metadata={'min':0, 'max': 1})
    xdtemporal_time: time = field(default=None, metadata={'min':0, 'max': 1})
    xdtemporal_datetime: datetime = field(default=None, metadata={'min':0, 'max': 1})
    xdtemporal_day: date = field(default=None, metadata={'min':0, 'max': 1})
    xdtemporal_month: date = field(default=None, metadata={'min':0, 'max': 1})
    xdtemporal_year: date = field(default=None, metadata={'min':0, 'max': 1})
    xdtemporal_year_month: date = field(default=None, metadata={'min':0, 'max': 1})
    xdtemporal_month_day: date = field(default=None, metadata={'min':0, 'max': 1})
    xdtemporal_duration: date = field(default=None, metadata={'min':0, 'max': 1})    
    
    
@dataclass
class ItemType(object):
    """
    The abstract parent of ClusterType and XdAdapterType structural representation types. 
    """
    pass


@dataclass
class XdAdapterType(ItemType):
    """
    The leaf variant of Item, to which any XdAnyType subtype instance is attached for use in a Cluster.
    """
    XdAdapter_value: XdAnyType = field(default=None, metadata={'min':0, 'max': 100}) # max is technically unbounded however a proactical limit is well under 100

@dataclass
class ClusterType(ItemType):
    """
    The grouping component, which may contain further instances of itself or any eXtended datatype, in an ordered list. This can serve as the root component for arbitrarily complex structures.
    """
    label: str = field(default='', metadata={'min':1, 'max': 1})
    items: ItemType = field(default=None, metadata={'min':0, 'max': 100}) # max is technically unbounded however a proactical limit is well under 100
    

@dataclass
class PartyType(object):
    """
    Description of a party, including an optional external link to data for this party in a demographic or other identity management system. An additional details element provides for the inclusion of information related to this party directly. If the party
    information is to be anonymous then do not include the details element.
    """
    label: str = field(default='', metadata={'min':1, 'max': 1})
    party_name: str = field(default='', metadata={'min':0, 'max': 1})
    party_ref: XdLinkType = field(default='', metadata={'min':0, 'max': 1})
    party_details: ClusterType = field(default='', metadata={'min':0, 'max': 1})

    
@dataclass
class AuditType(object):
    """
    AuditType provides a mechanism to identify the who/where/when tracking of instances as they move from system to system.
    """
    label: str = field(default='', metadata={'min':1, 'max': 1})
    system_id: XdStringType = field(default=None, metadata={'min':0, 'max': 1})
    system_user: PartyType = field(default=None, metadata={'min':0, 'max': 1})
    location: ClusterType = field(default=None, metadata={'min':0, 'max': 1})
    timestamp: datetime = field(default=None, metadata={'min':1, 'max': 1})


@dataclass
class AttestationType(object):
    """
    Record an attestation by a party of the DM content. The type of attestation is recorded by the reason attribute, which my be coded.
    """
    label: str = field(default='', metadata={'min':1, 'max': 1})
    view: XdFileType = field(default=None, metadata={'min':0, 'max': 1})
    proof: XdFileType = field(default=None, metadata={'min':0, 'max': 1})
    reason: XdStringType = field(default=None, metadata={'min':0, 'max': 1})
    committer: PartyType = field(default=None, metadata={'min':0, 'max': 1})
    committed: datetime = field(default=None, metadata={'min':0, 'max': 1})
    pending: bool = field(default=None, metadata={'min':1, 'max': 1})
   


@dataclass
class ParticipationType(object):
    """
    Model of a participation of a Party (any Actor or Role) in an activity. Used to represent any participation of a Party in some activity, which is not explicitly in the model, e.g. assisting nurse. Can be used to record past or future participations.
    """
    label: str = field(default='', metadata={'min':1, 'max': 1})
    performer: PartyType = field(default=None, metadata={'min':0, 'max': 1})
    function: XdStringType = field(default=None, metadata={'min':0, 'max': 1})
    mode: XdStringType = field(default=None, metadata={'min':0, 'max': 1})
    start: datetime = field(default=None, metadata={'min':0, 'max': 1})
    end: datetime = field(default=None, metadata={'min':0, 'max': 1})


@dataclass
class DMType(object):
    """
    This is the root node of a Data Model (DM)
    """
    label: str = field(default='', metadata={'min':1, 'max': 1})
    dm_language: str = field(default='', metadata={'min':1, 'max': 1})
    dm_encoding: str = field(default='', metadata={'min':1, 'max': 1})
    current_state: str = field(default='', metadata={'min':1, 'max': 1})
    data: ClusterType = field(default=None, metadata={'min':1, 'max': 1})
    subject: PartyType = field(default=None, metadata={'min':0, 'max': 1})
    provider: PartyType = field(default=None, metadata={'min':0, 'max': 1})
    participations: ParticipationType = field(default=None, metadata={'min':0, 'max': 100})  # max is technically unbounded however a proactical limit is well under 100
    protocol: XdStringType = field(default=None, metadata={'min':0, 'max': 1})
    workflow: XdLinkType = field(default=None, metadata={'min':0, 'max': 1})
    acs: XdLinkType = field(default=None, metadata={'min':0, 'max': 1})
    audits: AuditType = field(default=None, metadata={'min':0, 'max': 100})  # max is technically unbounded however a proactical limit is well under 100
    attestations: AttestationType = field(default=None, metadata={'min':0, 'max': 100})  # max is technically unbounded however a proactical limit is well under 100
    links: XdLinkType = field(default=None, metadata={'min':0, 'max': 100})  # max is technically unbounded however a proactical limit is well under 100
