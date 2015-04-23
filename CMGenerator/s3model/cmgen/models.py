import os
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import Group
from django.conf.global_settings import LANGUAGES as DJANGO_LANG
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib import messages

from .exceptions import *
from django_extensions.db.fields import UUIDField, ModificationDateTimeField

#import all of the publishers.
from .publisher import *


LANGUAGES = [('en-US','US English'),('pt-BR','Brazilian Portuguese')]
for n in DJANGO_LANG:
    LANGUAGES.append(n)

class Predicate(models.Model):
    """
    The list of predicates used when defining triples for PcT semantics.

    S3Model standard abbreviations are used for namespaces.
    rdfs="http://www.w3.org/2000/01/rdf-schema#"
    rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    dcterms="http://purl.org/dc/terms/"
    owl="http://www.w3.org/2002/07/owl#"
    s3m="http://www.s3model.com/"
    xs="http://www.w3.org/2001/XMLSchema"
    """

    pred_def = models.CharField(_("predicate definition"), max_length=2048, unique=True, db_index=True, help_text=_('Enter the predicate including the namespace abbreviation followed by a colon.'))

    def __str__(self):
        return self.pred_def
    class Meta:
        verbose_name = _("Predicate")
        verbose_name_plural = _("Predicates")
        ordering = ['pred_def']


class Project(models.Model):
    """
    Every item created in CMGenerator must be assigned to a Project when created.
    All complexTypes may be copied to other projects.
    """
    prj_name = models.CharField(_("project name"), max_length=110, unique=True, db_index=True, help_text=_('Enter the name of your project.'))
    description = models.TextField(_("project description"), blank=True, help_text=_('Enter a description or explaination of an acronym of the project.'))

    def __str__(self):
            return self.prj_name
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ['prj_name']

class PredObj(models.Model):
    """
     The Predicate and Object for the triple(s).
    """
    prj_name = models.ForeignKey(Project, verbose_name=_("Project Name"), default=1, help_text=_('Choose the name of your Project.'))
    name = models.CharField(_("name"), max_length=255, unique=True, db_index=True, help_text=_('Enter a unique, descriptive name for this entry.'))
    pred = models.ForeignKey(Predicate, verbose_name=_("Predicate"), help_text=_('Choose a predicate.'))
    obj = models.CharField(_("Object"), max_length=5000, help_text=_('Enter a resource link. Should be a resolvable URI.'))

    def __str__(self):
        return self.prj_name.prj_name + ' : ' + self.name

    class Meta:
        verbose_name = _("Predicate+Object")
        verbose_name_plural = _("Predicates+Objects")
        ordering = ['name','pred']


class Common(models.Model):
    """
    Columns common to all entries except Concept.
    """
    prj_name = models.ForeignKey(Project, verbose_name=_("Project Name"), help_text=_('Choose the name of your Project.'))
    ct_id = UUIDField(_("UUID"), version=4, help_text=_('A unique identifier for this PCT.'))
    created = models.DateTimeField(_('created'),auto_now_add=True, help_text=_('The dateTime that the PCT was created.'))
    last_updated = models.DateTimeField(_('last updated'),auto_now=True, help_text=_("Last update."))
    published = models.BooleanField(_("published"),default=False, help_text=_("Published must be a green check icon in order to use this in a CM. This is not user editable. It is managed by the publication process."))
    description = models.TextField(_('description'),help_text=_("Enter a free text description for this complexType. Include a usage statement and any possible misuses. This is used as the annotation for the PcT."), null=True)
    semantics = models.ManyToManyField(PredObj, verbose_name=_("semantics"), help_text="Select one or more Predicate/Object combinations for the semantics. You must select at least one.")
    schema_code = models.TextField(_("Schema Code"), help_text="This is only writable from the CMGEN, not via user input. It contains the code required for each component to create an entry in a CM.", blank=True, null=True, default='')
    asserts = models.TextField(_("asserts"), help_text="Valid XPath 2.0 assert statements. See the documentation for details. One per line.", blank=True, null=True, default='')
    lang = models.CharField(_("language"), max_length=40, choices=LANGUAGES, default='en-US', help_text=_('Choose the language of this PcT.'))
    r_code = models.TextField(_("R Code"), help_text="This is only writable from the CMGEN, not via user input. It contains the code required for each component to create a function for the R data analysis.", blank=True, null=True, default='')
    xqr_code = models.TextField(_("XQuery Read"), default='', help_text="This is only writable from the CMGEN, not via user input. It contains the code required to create a XQuery to read the PcT.", blank=True, null=True)
    xqw_code = models.TextField(_("XQuery Write"), default='', help_text="This is only writable from the CMGEN, not via user input. It contains the code required to create a XQuery to write the PcT.", blank=True, null=True)

    class Meta:
        abstract = True

class DvAny(Common):
    """
    Abstract root of all datatypes.
    """
    data_name = models.CharField(_('data name'),max_length=110, db_index=True, help_text=_("Type a name for this ComplexType."))
    adapter_id = UUIDField(_("Element UUID"), version=4, help_text=_('This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific DvAdapter complexType.'))
    vtb_required = models.BooleanField(_("VTB Required?"),default=False, help_text=_("Require a Valid begin time?"))
    vte_required = models.BooleanField(_("VTE Required?"),default=False, help_text=_("Require a Valid end time?"))

    def __str__(self):
        return self.prj_name.prj_name + ' : '+ self.data_name

    class Meta:
        abstract = True
        ordering=['prj_name','data_name']

class DvBoolean(DvAny):
    """
    Items which represent boolean decisions, such as true/false or yes/no answers. Use for such data, it
    is important to devise the meanings (usually questions in subjective data) carefully, so that the only allowed results
    are in fact true or false. Potential MisUse: The DvBoolean class should not be used as a replacement for naively
    modelled enumerated types such as male/female etc. Such values should be coded, and in any case the enumeration often
    has more than two values.
    """

    true_values = models.TextField(_('true options'),help_text=_("Enter the set of values that are Boolean TRUEs. For instance, if this is a 'Yes/No' type of concept, usually the 'Yes' is a Boolean TRUE. Enter one per line without blank lines."))
    false_values = models.TextField(_('false options'),help_text=_("Enter the set of values that are Boolean FALSEs. For instance, if this is a 'Yes/No' type of concept, usually the 'No' is a Boolean FALSE. Enter one per line without blank lines."))

    def publish(self, request):
        if self.schema_code == '':
            result = publish_DvBoolean(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.save()
        else:
            result = (self.data_name.strip()+' was not published because code already exists.', messages.ERROR)

        return result

    class Meta:
        verbose_name = "DvBoolean"
        verbose_name_plural = "DvBooleans"
        ordering=['prj_name','data_name']

class DvLink(DvAny):
    """
    Used to specify a Universal Resource Identifier as a link along with the semantics of what type of relationship exists
    between this context and the linked item.
    """
    relation = models.CharField(_('relation'),max_length=110, help_text=_("The relationship term describing the URI. Usually constrained by an ontology such as <a href='http://www.obofoundry.org/cgi-bin/detail.cgi?id=ro'>OBO RO</a>."))
    relation_uri = models.URLField(_('relation URL'),max_length=1024, blank=True, default='', help_text=_("A URL where the definition of the relation element term can be found. Normally points to an ontology such as the <a href='http://www.obofoundry.org/cgi-bin/detail.cgi?id=ro'>OBO RO</a>."))
    link_value = models.URLField(_('link'),max_length=1024, blank=True, default='', help_text=_("A URI specifying the linked item. Optional in the generator but required in instance data. If specified here, this value will be enforced in instance data."))

    def publish(self, request):
        if self.schema_code == '':
            result = publish_DvLink(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.save()
        else:
            result = (self.data_name.strip()+' was not published because code already exists.', messages.ERROR)

        return result

    class Meta:
        verbose_name = "DvLink"
        verbose_name_plural = "DvLinks"
        ordering=['prj_name','data_name']

class DvString(DvAny):
    """
    The string data type can contain characters, line feeds, carriage returns,
        and tab characters. The usecases are for any free form text entry or for any enumerated lists.
        Additionally the minimum and maximum lengths may be set and regular expression patterns may be specified.
    """
    WHITESPACE = [(None, 'Default is to preserve whitespace.'),('preserve','Preserve'),('replace','Replace'),('collapse','Collapse'),]
    min_length = models.IntegerField(_('minimum length'),help_text=_("Enter the minimum number of characters that are required for this concept. If the character is optional, leave it blank."), null=True, blank=True)
    max_length = models.IntegerField(_('maximum length'),help_text=_("Enter the maximum number of characters that are required for this concept. If the character is optional, leave it blank."), null=True, blank=True)
    exact_length = models.IntegerField(_('exact length'),help_text=_("Enter the exact length of the concept. It should be defined only when the number of characters is always fixed (e.g. codes and identifiers)."), null=True, blank=True)
    default_value = models.CharField(_('default value'),max_length=255, blank=True, help_text=_("Enter a default value for the string if desired."))
    enums = models.TextField(_('enumerations'),blank=True, help_text=_("Enter the categories values of the concept (e.g.Male,Female). One per line."))
    enums_def = models.TextField(_('enumerations definition'),blank=True, help_text=_("Enter a URI for each enumeration. One per line. These are used as rdf:isDefinedBy in the semantics. If the same URI is to be used for all enumeration then enter it on the first line only."))
    pattern = models.CharField(_('Pattern'),max_length=255, blank=True, help_text=_("Enter a pattern to constrain string if desired. See <a href='http://www.regular-expressions.info/xml.html'>options</a>"))
    whitespace = models.CharField("Whitespace", max_length=8, default='preserve', blank=False, help_text=_("Whitespace handling. See <a href=''>here</a>."), choices=WHITESPACE)
    lang_required =  models.BooleanField(_("Language Required?"), default=False, help_text=_("Require a language element?"))


    def publish(self, request):
        if self.schema_code == '':
            result = publish_DvString(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.save()
        else:
            result = (self.data_name.strip()+' was not published because code already exists.', messages.ERROR)

        return result

    class Meta:
        verbose_name = "DvString"
        verbose_name_plural = "DvStrings"
        ordering=['prj_name','data_name']

class DvEncapsulated(DvAny):
    """
    Abstract class defining the common meta-data of all types of encapsulated data.
    """
    encoding = models.CharField(_("encoding"), max_length=20, default='utf-8', help_text=_("<a href='http://www.iana.org/assignments/character-sets/character-sets.txt'>List of encoding types at IANA.</a>"))
    language = models.CharField(_("default language"), max_length=40, choices=LANGUAGES, default='en-US', help_text=_('Optional: Choose the DEFAULT language of the content.'))
    lang_required =  models.BooleanField(_("Language Required?"), default=False, help_text=_("Require a language element?"))
    fenums = models.TextField(_('formalism options'),blank=True, help_text=_("Leave blank to allow any formalisms or constrain the formalism to these options.  One per line."))
    fenums_def = models.TextField(_('formalism definitions'),blank=True, help_text=_("Enter a URI for each option. One per line. These are used as rdf:isDefinedBy in the semantics. If the same URI is to be used for all options then enter it on the first line only. Name of the formalism or syntax used to inform an application regarding a candidate parser to use on the content. Examples might include: 'ATL', 'MOLA', 'QVT', 'GDL', 'GLIF', etc. for DvParsables. Text-based formats that have a MIME type assigned, such as XML, XHTML, etc. should use DvMediaType."))

    def publish(self):
        pass

    class Meta:
        abstract = True
        ordering=['prj_name','data_name']

class DvParsable(DvEncapsulated):
    """
    Encapsulated data expressed as a parsable String. The internal model of the data item is not described
    in S3Model, but in this case, the form of the data is assumed to be plaintext, rather than compressed or other types of large binary data.
    If the content is to be binary data then use a DvMedia.
    """
    dvparsable_value = models.TextField(_('Default value'), help_text=_("You may enter a default value for the parsable content."), blank=True)

    def publish(self, request):
        if self.schema_code == '':
            result = publish_DvParsable(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.save()
        else:
            result = (self.data_name.strip()+' was not published because code already exists.', messages.ERROR)

        return result

    class Meta:
        verbose_name = "DvParsable"
        ordering=['prj_name','data_name']

class DvMedia(DvEncapsulated):
    """
    A specialisation of DvEncapsulated for audiovisual and bio-signal types. Includes further metadata
    relating to media types which with a defined MIME type.
    """
    CONTENT = [(None, 'Default is allow user choice'),('user','User Choice'),('url','Via URL'),('embed','Embedded in data')]

    media_type = models.TextField(_("Media Type"), help_text=_("The allowed Media Types of the included data, one per line; i.e. application/rdf+xml, image/jpeg, video/mp4. See < a href='http://www.iana.org/assignments/media-types/media-types.xhtml'>IANA</a>."), blank=True)
    compression_type = models.TextField(_("compression Type"), help_text=_("The allowed Compression Types of the included data, one per line. See <a href='http://en.wikipedia.org/wiki/List_of_archive_formats'>Listing</a>."), blank=True)
    hash_function = models.TextField(_("HASH Function"), blank=True, help_text=_("List of allowed HASH functions. See <a href='http://en.wikipedia.org/wiki/Hash_function'>HASH Functions</a>"))
    alt_required =  models.BooleanField(_("Alt Text Required?"), default=False, help_text=_("Require an alt-txt element?"))
    media_required =  models.BooleanField(_("Media Type Required?"), default=False, help_text=_("Require a media-type element?"))
    comp_required =  models.BooleanField(_("Compression Type Required?"), default=False, help_text=_("Require a compression-type element?"))
    hash_required =  models.BooleanField(_("HASH Required?"), default=False, help_text=_("Require hash-function and hash-result elements?"))
    content = models.CharField(_("Media Content"), max_length=20, blank=False, choices=CONTENT, default='user', help_text=_("Select the location of the data. Via a URL or embedded in the data instance."))

    def publish(self, request):
        if self.schema_code == '':
            result = publish_DvMedia(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.save()
        else:
            result = (self.data_name.strip()+' was not published because code already exists.', messages.ERROR)

        return result

    class Meta:
        verbose_name = "DvMedia"
        verbose_name_plural = "DvMedia"
        ordering=['prj_name','data_name']

class DvInterval(DvAny):
    """
    Generic class defining an interval (i.e. range) of a comparable type. An interval is a contiguous
    subrange of a comparable base type. Used to define intervals of dates, times, quantities Whose units of measure match
    and datatypes are the same and are ordered. See http://docstore.mik.ua/orelly/xml/schema/ch04_04.htm for value limits on numerics.
    """
    INTERVAL_TYPES = (('None','Select Type:'),('int','Count data (xs:int)'),('decimal','Real set numbers (xs:decimal)'),('float','Floating Point (xs:float)'),
                      ('dateTime','Date/Time (YYYY-MM-DDTHH:mm:ss)'),('date','Date (YYYY-MM-DD)'),
                      ('time','Time (HH:mm:ss)'),('duration','Duration (xs:duration)'))
    lower = models.CharField(_("Lower Value"), max_length=110, blank=True, null=True, help_text=_('Enter the lower value of the interval. This will be used to set the minInclusive facet.'))
    upper = models.CharField(_("Upper Value"), max_length=110, blank=True, null=True, help_text=_('Enter the upper value of the interval. This will be used to set the maxInclusive facet.'))
    interval_type = models.CharField(_("Interval Type"), default='Select Type:', help_text=_("The XML Schema datatype of the upper and lower values."), choices=INTERVAL_TYPES, max_length=20)
    lower_included = models.BooleanField(_('Lower Included?'),default=True, help_text=_('Uncheck this box if the lower value is excluded in the interval'))
    upper_included = models.BooleanField(_('Upper Included?'),default=True, help_text=_('Uncheck this box if the upper value is excluded in the interval'))
    lower_bounded = models.BooleanField(_('Lower Bounded?'),default=True, help_text=_("Uncheck this box if the lower value is unbounded. If unchecked, instances must be set to xsi:nil='true'"))
    upper_bounded = models.BooleanField(_('Upper Bounded?'),default=True, help_text=_("Uncheck this box if the lower value is unbounded. If unchecked, instances must be set to xsi:nil='true'"))

    def publish(self, request):
        if self.schema_code == '':
            result = publish_DvInterval(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.save()
        else:
            result = (self.data_name.strip()+' was not published because code already exists.', messages.ERROR)

        return result

    class Meta:
        verbose_name = "DvInterval"
        ordering=['prj_name','data_name']

class ReferenceRange(DvAny):
    """
    Defines a named range to be associated with any ORDERED datum. Each such range is particular to the
    patient and context, e.g. sex, age, and any other factor which affects ranges. May be used to represent normal,
    therapeutic, dangerous, critical etc ranges.
    """
    definition = models.CharField(_("Definition"), max_length=110, help_text=_("Enter the term that indicates the status of this range, e.g. 'normal', 'critical', 'therapeutic' etc."))
    data_range = models.ForeignKey(DvInterval, verbose_name=_('data range'),help_text=_("The data range for this meaning. Select the appropriate DvInterval."))
    is_normal = models.BooleanField(_('Is Normal?'),default=False, help_text=_("Is this considered the normal range?"))

    def publish(self, request):
        if self.schema_code == '':
            result = publish_ReferenceRange(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.save()
        else:
            result = (self.data_name.strip()+' was not published because code already exists.', messages.ERROR)

        return result

    class Meta:
        verbose_name = "ReferenceRange"
        ordering=['prj_name','data_name']

class DvOrdered(DvAny):
    """
    Abstract class defining the concept of ordered values, which includes ordinals as well as true
    quantities. The implementations require the functions ‘&lt;’, '&gt;' and is_strictly_comparable_to ('==').
    """
    reference_ranges = models.ManyToManyField(ReferenceRange, verbose_name=_('reference ranges'), blank=True, help_text=_('Select the appropriate ReferenceRange(s) that defines each ordered value. The listing is by Project: Reference Range Name.'))
    normal_status = models.CharField(_('normal status'),max_length=110, help_text=_("Enter text that indicates a normal status."), blank=True, null=True)

    def publish(self):
        pass

    class Meta:
        abstract = True


class DvOrdinal(DvOrdered):
    """Models rankings and scores, e.g. pain, Apgar values, etc, where there is a)
        implied ordering, b) no implication that the distance between each value is constant, and c)
        the total number of values is finite. Note that although the term ‘ordinal’ in mathematics
        means natural numbers only, here any decimal is allowed, since negative and zero values are
        often used by medical and other professionals for values around a neutral point.
        Also, decimal values are sometimes used such as 0.5 or .25

        Examples of sets of ordinal values:
        -3, -2, -1, 0, 1, 2, 3 -- reflex response values
        0, 1, 2 -- Apgar values

        Also used for recording any clinical or other datum which is customarily recorded using symbolic values.
        Examples:
        the results on a urinalysis strip, e.g. {neg, trace, +, ++, +++} are used for leukocytes, protein, nitrites etc;
        for non-haemolysed blood {neg, trace, moderate};
        for haemolysed blood {neg, trace, small, moderate, large}.

      Elements dvordinal-value and symbol MUST have exactly the same number of enumerations.
    """
    ordinals = models.TextField(_('ordinals'),help_text=_("Enter the ordered sequence of integer values. The base integer is zero with any number of integer values used to order the symbols. Example A: 0 = Trace, 1 = +, 2 = ++, 3 = +++, etc. Example B: 0 = Mild, 1 = Moderate, 2 = Severe. One per line."))
    symbols = models.TextField(_('symbols'),help_text=_("Enter the symbols or the text that represent the ordinal values, which may be strings made from '+' symbols, or other enumerations of terms such as 'mild', 'moderate', 'severe', or even the same number series used for the ordinal values, e.g. '1', '2', '3'.. One per line."))
    symbols_def = models.TextField(_('symbols definition'), blank=True, help_text=_("Enter a URI for each symbol. One per line. These are used as rdf:isDefinedBy in the semantics. If the same URI is to be used for all symbols then enter it on the first line only."))

    def publish(self, request):
        if self.schema_code == '':
            result = publish_DvOrdinal(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.save()
        else:
            result = (self.data_name.strip()+' was not published because code already exists.', messages.ERROR)

        return result

    class Meta:
        verbose_name = "DvOrdinal"
        ordering=['prj_name','data_name']

class DvQuantified(DvOrdered):
    """
    Abstract class defining the concept of true quantified values, i.e. values which are not only ordered,
    but which have a precise magnitude.
    """
    min_inclusive = models.DecimalField(_('minimum inclusive'), max_digits=19, decimal_places=10, help_text=_("Enter the minimum (inclusive) value for the magnitude."), null=True, blank=True)
    max_inclusive = models.DecimalField(_('maximum inclusive'), max_digits=19, decimal_places=10, help_text=_("Enter the maximum (inclusive) value for the magnitude."), null=True, blank=True)
    min_exclusive = models.DecimalField(_('minimum exclusive'), max_digits=19, decimal_places=10, help_text=_("Enter the minimum (exclusive) value for the magnitude."), null=True, blank=True)
    max_exclusive = models.DecimalField(_('maximum exclusive'), max_digits=19, decimal_places=10, help_text=_("Enter the maximum (exclusive) value for the magnitude."), null=True, blank=True)
    fraction_digits = models.IntegerField(_('fraction digits'), blank=True,null=True, help_text=_('Specifies the maximum number of decimal places allowed. Must be equal to or greater than zero for DvQuantity. For DvCount it is zero.'))
    total_digits = models.IntegerField(_('total digits'),help_text=_("Enter the maximum number of digits for the magnitude."), null=True, blank=True)

    def publish(self):
        pass

    class Meta:
        abstract = True

class DvCount(DvQuantified):
    """
    Countable quantities. Used for countable types such as pregnancies and steps (taken by a physiotherapy
    patient), number of cigarettes smoked in a day, etc. Misuse:Not used for amounts of physical entities (which all have
    standardized units)
    """
    units = models.ForeignKey(DvString, verbose_name=_('units'), null=True, blank=True,help_text=_("Choose a DvString for the allowed units of measurement of this concept."))

    def publish(self, request):
        if self.schema_code == '':
            result = publish_DvCount(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.save()
        else:
            result = (self.data_name.strip()+' was not published because code already exists.', messages.ERROR)

        return result

    class Meta:
        verbose_name = "DvCount"
        ordering=['prj_name','data_name']

class DvQuantity(DvQuantified):
    """
    Quantitified type representing “scientific” quantities, i.e. quantities expressed as a magnitude and
    units. Units were inspired by the Unified Code for Units of Measure (UCUM), developed by Gunther Schadow and Clement J.
    McDonald of The Regenstrief Institute. http://unitsofmeasure.org/ Can also be used for time durations, where it is more
    convenient to treat these as simply a number of individual seconds, minutes, hours, days, months, years, etc. when no temporal calculation is to be performed.
    """
    units = models.ForeignKey(DvString, verbose_name=_('units'), null=True, blank=True,help_text=_("Choose a DvString for the allowed units of measurement of this concept."))

    def publish(self, request):
        if self.schema_code == '':
            result = publish_DvQuantity(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.save()
        else:
            result = (self.data_name.strip()+' was not published because code already exists.', messages.ERROR)

        return result

    class Meta:
        verbose_name = "DvQuantity"
        verbose_name_plural = "DvQuantities"
        ordering=['prj_name','data_name']

class DvRatio(DvQuantified):
    """
    Models a ratio of values, i.e. where the numerator and denominator are both pure numbers. Should not
    be used to represent things like blood pressure which are often written using a ‘/’ character, giving the misleading
    impression that the item is a ratio, when in fact it is a structured value. Similarly, visual acuity, often written as
    (e.g.) “6/24” in clinical notes is not a ratio but an ordinal (which includes non-numeric symbols like CF = count
    fingers etc). Should not be used for formulations.
    """
    RATIO_CHOICES = (('ratio',_('Ratio')),('proportion',_('Proportion')),('rate',_('Rate')))
    ratio_type = models.CharField(_('ratio type'),max_length=10,choices=RATIO_CHOICES)

    num_min_inclusive = models.IntegerField(_('numerator minimum inclusive'),help_text=_("Enter the minimum (inclusive) value for the numerator."), null=True, blank=True)
    num_max_inclusive = models.IntegerField(_('numerator maximum inclusive'),help_text=_("Enter the maximum (inclusive) value for the numerator."), null=True, blank=True)
    num_min_exclusive = models.IntegerField(_('numerator minimum exclusive'),help_text=_("Enter the minimum (exclusive) value for the numerator."), null=True, blank=True)
    num_max_exclusive = models.IntegerField(_('numerator maximum exclusive'),help_text=_("Enter the maximum (exclusive) value for the numerator."), null=True, blank=True)
    num_fraction_digits = models.IntegerField(_('fraction digits'), blank=True,null=True, help_text=_('Specifies the maximum number of decimal places allowed in the numerator. Must be equal to or greater than zero.'))
    num_total_digits = models.IntegerField(_('total digits'),help_text=_("Enter the maximum number of digits for the numerator."), null=True, blank=True)

    den_min_inclusive = models.IntegerField(_('denominator minimum inclusive'),help_text=_("Enter the minimum (inclusive) value for the denominator."), null=True, blank=True)
    den_max_inclusive = models.IntegerField(_('denominator maximum inclusive'),help_text=_("Enter the maximum (inclusive) value for the denominator."), null=True, blank=True)
    den_min_exclusive = models.IntegerField(_('denominator minimum exclusive'),help_text=_("Enter the minimum (exclusive) value for the denominator."), null=True, blank=True)
    den_max_exclusive = models.IntegerField(_('denominator maximum exclusive'),help_text=_("Enter the maximum (exclusive) value for the denominator."), null=True, blank=True)
    den_fraction_digits = models.IntegerField(_('fraction digits'), blank=True,null=True, help_text=_('Specifies the maximum number of decimal places allowed in the denominator. Must be equal to or greater than zero.'))
    den_total_digits = models.IntegerField(_('total digits'),help_text=_("Enter the maximum number of digits for the denominator."), null=True, blank=True)

    num_units = models.ForeignKey(DvString, verbose_name=_('numerator units'), related_name='num_units', null=True, blank=True,help_text=_("Choose a DvString for the units of measurement of the numerator."))
    den_units = models.ForeignKey(DvString, verbose_name=_('denominator units'), related_name='den_units', null=True, blank=True,help_text=_("Choose a DvString for the units of measurement of the denominator."))
    ratio_units = models.ForeignKey(DvString, verbose_name=_('ratio units'), related_name='ratio_units', null=True, blank=True,help_text=_("Choose a DvString for the units of measurement of the ratio (magnitude)."))

    def publish(self, request):
        if self.schema_code == '':
            result = publish_DvRatio(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.save()
        else:
            result = (self.data_name.strip()+' was not published because code already exists.', messages.ERROR)

        return result

    class Meta:
        verbose_name = "DvRatio"
        ordering=['prj_name','data_name']

class DvTemporal(DvOrdered):
    """
    Class defining the concept of date and time types.
    Must be constrained in CCDs to be one or more of the allowed types.
    This gives the modeller the ability to optionally allow partial dates at run time.
    If one of the duration types is selected then no other type is allowed.
    All types are considered optional (minOccurs='0') by default. If you need to make on mandatory then an assert statement is required.
    """
    allow_duration = models.BooleanField(_('allow duration'),default=False, help_text=_("If Duration is allowed, no other types will be permitted."))
    allow_ymduration = models.BooleanField(_('allow yearMonthDuration'),default=False, help_text=_("If yearMonthDuration is allowed, no other types will be permitted."))
    allow_dtduration = models.BooleanField(_('allow dayTimeDuration'),default=False, help_text=_("If dayTimeDuration is allowed, no other types will be permitted."))
    allow_date = models.BooleanField(_('allow date'),default=False, help_text=_('Check this box if complete date entry is allowed.'))
    allow_time = models.BooleanField(_('allow time'),default=False, help_text=_('Check this box if time only entry is allowed.'))
    allow_datetime = models.BooleanField(_('allow datetime'),default=False, help_text=_('Check this box if complete dates and times are allowed.'))
    allow_day = models.BooleanField(_('allow day'),default=False, help_text=_('Check this box if day only is allowed.'))
    allow_month = models.BooleanField(_('allow month'),default=False, help_text=_('Check this box if month only is allowed.'))
    allow_year = models.BooleanField(_('allow year'),default=False, help_text=_('Check this box if year only entry is allowed.'))
    allow_year_month = models.BooleanField(_('allow year month'),default=False, help_text=_('Check this box if combination of years and months are allowed.'))
    allow_month_day = models.BooleanField(_('allow month day'),default=False, help_text=_('Check this box if combination of months and days are allowed.'))

    require_duration = models.BooleanField(_('require duration'),default=False, help_text=_("If Duration is required, no other types will be permitted."))
    require_ymduration = models.BooleanField(_('require yearMonthDuration'),default=False, help_text=_("If yearMonthDuration is required, no other types will be permitted."))
    require_dtduration = models.BooleanField(_('require dayTimeDuration'),default=False, help_text=_("If dayTimeDuration is required, no other types will be permitted."))
    require_date = models.BooleanField(_('require date'),default=False, help_text=_('Check this box if complete date entry is required.'))
    require_time = models.BooleanField(_('require time'),default=False, help_text=_('Check this box if time only entry is required.'))
    require_datetime = models.BooleanField(_('require datetime'),default=False, help_text=_('Check this box if complete dates and times are required.'))
    require_day = models.BooleanField(_('require day'),default=False, help_text=_('Check this box if day only is required.'))
    require_month = models.BooleanField(_('require month'),default=False, help_text=_('Check this box if month only is required.'))
    require_year = models.BooleanField(_('require year'),default=False, help_text=_('Check this box if year only entry is required.'))
    require_year_month = models.BooleanField(_('require year month'),default=False, help_text=_('Check this box if combination of years and months are required.'))
    require_month_day = models.BooleanField(_('require month day'),default=False, help_text=_('Check this box if combination of months and days are required.'))

    def publish(self, request):
        if self.schema_code == '':
            result = publish_DvTemporal(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.save()
        else:
            result = (self.data_name.strip()+' was not published because code already exists.', messages.ERROR)

        return result

    class Meta:
        verbose_name = "DvTemporal"
        ordering=['prj_name','data_name']

class Party(Common):
    """
    A proxy description of a party, including an optional link to data for this party in a demographic or other
    identity management system.
    """
    label = models.CharField(_('label'),max_length=110, help_text=_("A label used to identify this model in CM Generator."))
    require_name = models.BooleanField(_('require name'),default=False, help_text=_('Check this box if a party-name element is required.'))
    party_details = models.ForeignKey('Cluster', verbose_name=_('details'), related_name='%(class)s_related', null=True, blank=True, help_text=_('A Cluster structure that defines the details of this Party.'))
    party_ref = models.ManyToManyField(DvLink, verbose_name=_('external reference'), help_text=_("An optional DvLink that points to a description of this Party in another service."), blank=True)


    def publish(self, request):
        if self.schema_code == '':
            result = publish_Party(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.save()
        else:
            result = (self.data_name.strip()+' was not published because code already exists.', messages.ERROR)

        return result

    def __str__(self):
            return self.prj_name.prj_name + ' : '+ self.label
    class Meta:
        verbose_name = "Party"
        ordering=['prj_name','label']

class Audit(Common):
    """
    Audit provides a mechanism to identifiy the who/where/when tracking of instances as they move from system to system.
    """
    label = models.CharField(_('label'),max_length=110, help_text=_("A label used to identify this model in CM Generator."))
    system_id = models.ForeignKey(DvString, verbose_name=_('system id'), null=True, blank=True, help_text=_('A model for an Identifier of the system which handled the information item.'))
    system_user = models.ForeignKey(Party, verbose_name=_('system user'), null=True, blank=True, help_text=_('A model for user(s) who created, committed, forwarded or otherwise handled the item.'))
    location = models.ForeignKey('Cluster', verbose_name=_('location'), related_name='%(class)s_related', null=True, blank=True, help_text=_('A Cluster for location information.'))

    def __str__(self):
            return self.prj_name.prj_name + ' : '+self.label

    def publish(self, request):
        if self.schema_code == '':
            result = publish_Audit(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.save()
        else:
            result = (self.label.strip()+' was not published because code already exists.', messages.ERROR)

        return result

    class Meta:
        verbose_name = "Audit"
        verbose_name_plural = "Audits"
        ordering=['prj_name','label']


class Attestation(Common):
    """
    Record an attestation by a party of item(s) of record content. The type of attestation is recorded by
    the reason attribute.
    """
    label = models.CharField(_('label'),max_length=110, help_text=_("A label used to identify this model in CM Generator."))
    attested_view = models.ForeignKey(DvMedia, verbose_name=_('attested view'), null=True, help_text=_('A recorded view that is being attested.'))
    proof = models.ForeignKey(DvParsable, verbose_name=_('proof'), null=True, help_text=_('Proof of attestation such as an GPG signature.'))
    reason = models.ForeignKey(DvString, verbose_name=_('reason'), null=True, help_text=_('Select a DvString type as a model for the reason.'))
    committer = models.ForeignKey(Party, verbose_name=_('committer'), null=True, help_text=_('A Party model for someone that commited the Attestation.'))

    def publish(self, request):
        if self.schema_code == '':
            result = publish_Attestation(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.save()
        else:
            result = (self.label.strip()+' was not published because code already exists.', messages.ERROR)

        return result

    def __str__(self):
            return self.prj_name.prj_name + ' : '+self.label

    class Meta:
        verbose_name = "Attestation"
        ordering=['prj_name','label']

class Participation(Common):
    """
    Model of a participation of a Party (any Actor or Role) in an activity. Used to represent any
    participation of a Party in some activity, which is not explicitly in the model, e.g. assisting nurse, ambulance service, etc.
    Can be used to record past or future participations. Should not be used in place of more permanent relationships between demographic
    entities.
    """
    label = models.CharField(_('label'),max_length=110, help_text=_("A label used to identify this model in CM Generator."))
    performer = models.ForeignKey(Party, null=True, help_text=_('The Party instance and possibly demographic system link of the party participating in the activity.'))
    function = models.ForeignKey(DvString, null=True, related_name='function', help_text=_('The function of the Party in this participation (note that a given party might participate in more than one way in a particular activity). In some applications this might be called a Role.'))
    mode = models.ForeignKey(DvString, null=True, related_name='mode', help_text=_('The mode of the performer / activity interaction, e.g. present, by telephone, by email etc. If the participation is by device or software it may contain a protocol standard or interface definition.'))

    def publish(self, request):
        if self.schema_code == '':
            result = publish_Participation(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.save()
        else:
            result = (self.label.strip()+' was not published because code already exists.', messages.ERROR)

        return result

    def __str__(self):
            return self.prj_name.prj_name + ' : '+self.label

    class Meta:
        verbose_name = "Participation"
        ordering=['prj_name','label']

class Cluster(Common):
    """
    The grouping variant of Item, which may contain further instances of Item, in an ordered list. This
    provides the root Item for potentially very complex structures.
    """
    cluster_subject = models.CharField(_('cluster subject'),max_length=110, help_text="Enter a text name for this subject of this cluster.")
    clusters = models.ManyToManyField('Cluster',help_text="Select zero or more Clusters to include in this Cluster. You cannot put a Cluster inside itself, it will be ignored if you select itself.", blank=True)
    dvboolean = models.ManyToManyField(DvBoolean,  help_text="Select zero or more booleans to include in this Cluster.", blank=True)
    dvlink = models.ManyToManyField(DvLink,  help_text="Select zero or more links to include in this Cluster.", blank=True)
    dvstring = models.ManyToManyField(DvString,  help_text="Select zero or more strings to include in this Cluster.", blank=True)
    dvparsable = models.ManyToManyField(DvParsable,  help_text="Select zero or more parsables to include in this Cluster.", blank=True)
    dvmedia = models.ManyToManyField(DvMedia,  help_text="Select zero or more media items to include in this Cluster.", blank=True)
    dvordinal = models.ManyToManyField(DvOrdinal,  help_text="Select zero or more ordinals to include in this Cluster.", blank=True)
    dvcount = models.ManyToManyField(DvCount,  help_text="Select zero or more counts to include in this Cluster.", blank=True)
    dvquantity = models.ManyToManyField(DvQuantity,  help_text="Select zero or more quantity items to include in this Cluster.", blank=True)
    dvratio = models.ManyToManyField(DvRatio,  help_text="Select zero or more ratios to include in this Cluster.", blank=True)
    dvtemporal = models.ManyToManyField(DvTemporal,  help_text="Select zero or more temporal items to include in this Cluster.", blank=True)

    def __str__(self):
        return self.prj_name.prj_name + ' : '+self.cluster_subject

    def publish(self, request):
        if self.schema_code == '':
            result = publish_Cluster(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.save()
        else:
            result = (self.cluster_subject.strip()+' was not published because code already exists.', messages.ERROR)

        return result

    class Meta:
        verbose_name = "Cluster"
        ordering=['prj_name','cluster_subject']

class Concept(Common):
    """
    An Concept is the root of a logical set of data items.
        The Concept Model must contain metadata about the model.
        Mandatory DCTERMS; identifier, title, creator, rightsHolder, license, issued, format ('text/xml'), language and abstract.
        Suggested but optional DCTERMS; contributors, relation

    """

    #metadata
    title = models.CharField(_('title'),unique=True, max_length=255, help_text=_("Enter the name of this  Model (CM)"))
    author = models.ForeignKey(User, verbose_name=_("author"), related_name='creator', help_text=_('Choose Author of this Concept Model (CM)'))
    contributors = models.ManyToManyField(User, verbose_name=_("contributors"), help_text=_('Select contributors to this Concept Model (CM)'))
    license = models.CharField(_('rights'),max_length=255, help_text=_("Enter the rights or license statement."), default="All Rights Reserved.")
    rights_holder_name = models.CharField(_('Rights Holder Name'),max_length=255, help_text=_("Enter the name of the publisher/copyright holder."))
    rights_holder_email = models.CharField(_('Rights Holder Email'),max_length=255, blank=True, default=' ', help_text=_("Enter the email of the publisher/copyright holder."))
    relation = models.CharField(_('relation'), max_length=255, blank=True, help_text=_("Enter the relationship to another Concpet Model, if applicable."), default="None")
    pub_date = ModificationDateTimeField(verbose_name=_("date of publication"),help_text=_("Date of publication."))

    # concept model data
    encoding = models.CharField(_("encoding"), max_length=20, default='utf-8', help_text=_("Normally leave as utf-8 default. Otherwise see: <a href='http://www.iana.org/assignments/character-sets/character-sets.txt'>List of encoding types at IANA.</a>"))
    data = models.ForeignKey(Cluster, verbose_name=_("Data Cluster"), help_text=_('Choose the data element cluster of this Concept Model (CM)'))
    subject = models.ForeignKey(Party, verbose_name=_("Subject"), help_text=_('Choose the subject element Party model of this Concept Model (CM)'))
    protocol = models.ForeignKey(DvLink, verbose_name=_("Protocol"), related_name='protocol', help_text=_('Choose the protocol element model of this Concept Model (CM)'))
    workflow = models.ForeignKey(DvLink, verbose_name=_("Workflow"), related_name='workflow', help_text=_('Choose the workflow element model of this Concept Model (CM)'))
    attested = models.ForeignKey(Attestation, verbose_name=_("Attestation"), help_text=_('Choose the attested element model of this Concept Model (CM)'))
    participations = models.ManyToManyField(Participation, verbose_name=_("Participations"), help_text=_('Choose the participation models element model of this Concept Model (CM)'))
    audits = models.ManyToManyField(Audit, verbose_name=_("Audits"), help_text=_('Choose the audit element models of this Concept Model (CM)'))
    links = models.ManyToManyField(DvLink, verbose_name=_("Links"), related_name='links', help_text=_('Select links models to/from this Concept Model (CM)'))

    def generate(self):
        """
        Create an XML Schema for the CM.
        """
        generateCM(self)

    def publish(self, request):
        if self.schema_code == '':
            result = publish_Concept(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.save()
        else:
            result = (self.title.strip()+' was not published because code already exists.', messages.ERROR)

        return result

    def __str__(self):
            return self.prj_name.prj_name + ' : '+self.title

    class Meta:
        verbose_name = "Concept"
        ordering=['prj_name','title']
