import os
from time import time
import uuid

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from django.conf.global_settings import LANGUAGES as DJANGO_LANG

from dmgen.models import Project, Modeler, dm_folder

LANGUAGES = [('en-US', 'US English'), ('pt-BR', 'Brazilian Portuguese')]
for n in DJANGO_LANG:
    LANGUAGES.append(n)

def data_upload(instance, filename):
    """
    Name and location of uploaded search results.
    """
    tfolder = 'translator_csv'
    ts = str(int(time()))                     # the timestamp rounded to an integer, of when it was uploaded
    ext = filename.split('.')[-1]          # reuse the original file extension
    path_file = os.path.join(tfolder, ts + '.' + ext)
    return path_file


class DMD(models.Model):
    """
     Data Model Description
    """
    DELIM_CHOICES = ((',', _('Comma')), (';', _('Semicolon')), ('|', _('Pipe')), (':', _('Colon')))

    title = models.CharField(_('title'), unique=True, max_length=255, help_text=_(
        "Enter the name of this Data Model."))
    description = models.TextField(_('description'), help_text=_(
        "Enter a general description for this DM."))
    definitions = models.TextField(_('definitions'), blank=False, help_text=_(
        "Enter one or more URIs (prefereable a URLs) that can be used as a definition / description for the data model. One per line."))
    project = models.ForeignKey(Project, verbose_name=_(
        "project name"), to_field="prj_name", help_text=_('Choose a Project for this Data Model (DM)'))
    author = models.ForeignKey(Modeler, verbose_name=_("Author"), help_text=_(
        "Select the author of the DM"), related_name='%(class)s_related_author')
    contrib = models.ManyToManyField(Modeler, verbose_name=_("Contributors"), help_text=_(
        "Select the contributors (if any) to this DM"), related_name='%(class)s_related_contrib', blank=True)
    delim = models.CharField( _('Delimiter'), max_length=1, choices=DELIM_CHOICES)
    lang = models.CharField(_("language"), max_length=40, choices=LANGUAGES,
                            default='en-US', help_text=_('Choose the language of this Data Model.'))

    csv_file = models.FileField(
        "CSV Upload", upload_to=data_upload, max_length=2048, blank=True, null=True)

    class Meta:
        verbose_name = "Data Model Definition"
        verbose_name_plural = "Data Model Definitions"

    def __str__(self):
        return self.title.strip()

class Record(models.Model):
    """
    A description of each data record (row) in the CSV file.
    The title returned is eXtended Datatype.
    """
    DT_CHOICES = (('xdstring', _('Text')), ('xdcount', _('Integer')), ('xdquantity', _('Decimal  (Float)')), ('xdtemporal', _('Date/Time')))

    dmd = models.ForeignKey(DMD, verbose_name=_(
        "Data Model Definition"), help_text=_('This is the associated Data Model Definition.'))
    header = models.CharField(_("Header"), max_length=110, help_text=_(
        'The column header retrieved from the CSV file.'))
    label = models.CharField(_('label'), max_length=110, help_text=_(
        "Initially this is the CSV column header. It should be changed to a human readable label used to describe this data."))
    description = models.TextField(_('description'), default='Description goes here.', help_text=_(
        "Enter a general description for this datatype."))
    dt_type = models.CharField(_('datatype type'), max_length=20, choices=DT_CHOICES, help_text=_('Select the datatype for this column and then complete the constraints in the matching section below. For Integers and Decimals you must select the Numers section and complete the Units (name and uri) fields.'))
    min_length = models.IntegerField(_('minimum length'), help_text=_(
        "Enter the minimum number of characters that are required for this string. If the character is optional, leave it blank."), null=True, blank=True)
    max_length = models.IntegerField(_('maximum length'), help_text=_(
        "Enter the maximum number of characters that are required for this string. If the character is optional, leave it blank."), null=True, blank=True)
    exact_length = models.IntegerField(_('exact length'), help_text=_(
        "Enter the exact length of the string. It should be defined only when the number of characters is always fixed (e.g. codes and identifiers)."), null=True, blank=True)
    enums = models.TextField(_('enumerations'), blank=True, help_text=_(
        "For text types that are restricted to one of a set of strings, enter the set of values of the string (e.g.Male,Female). One per line."))
    def_val = models.CharField(_('default value'), max_length=255, blank=True, help_text=_(
        "Enter a default value (up to 255 characters) for the string if desired. Cannot contain 'http://' nor 'https://'"))
    definitions = models.TextField(_('definitions'), blank=True, help_text=_(
        "Enter one or more URIs (prefereable a URLs) that can be used as a definition / description for the data in this column. One per line."))
    min_magnitude = models.DecimalField(_('minimum magnitude'), blank=True, null=True, max_digits=10, decimal_places=5, help_text=_(
        "The minimum allowed value for a magnitude. If there isn't a min. then leave blank."))
    max_magnitude = models.DecimalField(_('maximum magnitude'), blank=True, null=True, max_digits=10, decimal_places=5, help_text=_(
        "Any maximum allowed value. If there isn't a max. then leave blank."))
    min_inclusive = models.IntegerField(_('minimum inclusive'), help_text=_(
        "Enter the minimum (inclusive) value for this concept."), null=True, blank=True)
    max_inclusive = models.IntegerField(_('maximum inclusive'), help_text=_(
        "Enter the maximum (inclusive) value for this concept."), null=True, blank=True)
    min_exclusive = models.IntegerField(_('minimum exclusive'), help_text=_(
        "Enter the minimum (exclusive) value for this concept."), null=True, blank=True)
    max_exclusive = models.IntegerField(_('maximum exclusive'), help_text=_(
        "Enter the maximum (exclusive) value for this concept."), null=True, blank=True)
    total_digits = models.IntegerField(_('total digits'), help_text=_(
        "Enter the maximum number of digits for this concept, excluding the decimal separator and the decimal places."), null=True, blank=True)
    allow_duration = models.BooleanField(_('duration'), default=False, help_text=_(
        ""))
    allow_ymduration = models.BooleanField(_('yearMonthDuration'), default=False, help_text=_(
        ""))
    allow_dtduration = models.BooleanField(_('dayTimeDuration'), default=False, help_text=_(
        ""))
    allow_date = models.BooleanField(_('date'), default=False, help_text=_(
        ''))
    allow_time = models.BooleanField(_('time'), default=False, help_text=_(
        ''))
    allow_datetime = models.BooleanField(_('datetime'), default=False, help_text=_(
        ''))
    allow_datetimestamp = models.BooleanField(_('datetimestamp'), default=False, help_text=_(
        ''))
    allow_day = models.BooleanField(_('day'), default=False, help_text=_(
        ''))
    allow_month = models.BooleanField(_('month'), default=False, help_text=_(
        ''))
    allow_year = models.BooleanField(_('year'), default=False, help_text=_(
        ''))
    allow_year_month = models.BooleanField(_('year month'), default=False, help_text=_(
        ''))
    allow_month_day = models.BooleanField(_('month day'), default=False, help_text=_(
        ''))
    units_name = models.CharField(_('Units Name'), max_length=255, blank=True, help_text=_("Enter the name of what is being counted or measured."))
    units_uri = models.CharField(_('Units URI'), max_length=255, blank=True, help_text=_("Enter a URI that defines this units designation."))

    def __str__(self):
        return self.dmd.title + ":" + self.label.strip()

    class Meta:
        ordering = ['dmd', 'header']
        verbose_name = "eXtended Datatype Definition"
        verbose_name_plural = "eXtended Datatype Definitions"

