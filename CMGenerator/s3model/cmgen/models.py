import os
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import Group
from django.conf.global_settings import LANGUAGES as DJANGO_LANG
from django.utils.translation import ugettext_lazy as _

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
    dct="http://purl.org/dc/terms/"
    owl="http://www.w3.org/2002/07/owl#"
    s3m="http://www.s3model.com/"
    xs="http://www.w3.org/2001/XMLSchema"
    """

    pred_def = models.CharField(_("predicate definition"), max_length=2048, unique=True, db_index=True, help_text=_('Enter the predicate including the namespace abbreviation followed by a colon.'))



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
    pred = models.ForeignKey(Predicate, verbose_name=_("Predicate"), help_text=_('Choose a predicate.'))

class Common(models.Model):
    """
    Columns common to all entries except Concept.
    """
    prj_name = models.ForeignKey(Project, verbose_name=_("Project Name"), to_field="prj_name", help_text=_('Choose the name of your Project.'))
    ct_id = UUIDField(_("UUID"), version=4, help_text=_('A unique identifier for this PCT.'))
    created = models.DateTimeField(_('created'),auto_now_add=True, help_text=_('The dateTime that the PCT was created.'))
    last_updated = models.DateTimeField(_('last updated'),auto_now=True, help_text=_("Last update."))
    published = models.BooleanField(_("published"),default=False, help_text=_("Published must be a green check icon in order to use this in a CCD. This is not a user editable. It is managed by the publication process."))
    description = models.TextField(_('description'),help_text=_("Enter a free text description for this complexType. Include a usage statement and any possible misuses. This is used as the annotation for the PCT."), null=True)
    resource_uri = models.TextField(_("resource URIs"), help_text="URIs to be used as the object for semantic context. One per line.", blank=True, null=True, default='')
    schema_code = models.TextField(_("Schema Code"), help_text="This is only writable from the CCDGEN, not via user input. It contains the code required for each component to create an entry in a CCD.", blank=True, null=True, default='')
    asserts = models.TextField(_("asserts"), help_text="Valid XPath 2.0 assert statements. See the documentation for details. One per line.", blank=True, null=True, default='')
    lang = models.CharField(_("language"), max_length=40, choices=LANGUAGES, default='en-US', help_text=_('Choose the language of this PCT.'))
    r_code = models.TextField(_("R Code"), help_text="This is only writable from the CCDGEN, not via user input. It contains the code required for each component to create a function for the R data analysis.", blank=True, null=True, default='')
    xqr_code = models.TextField(_("XQuery Read"), default='', help_text="This is only writable from the CCDGEN, not via user input. It contains the code required to create a XQuery to read the PcT.", blank=True, null=True)
    xqw_code = models.TextField(_("XQuery Write"), default='', help_text="This is only writable from the CCDGEN, not via user input. It contains the code required to create a XQuery to write the PcT.", blank=True, null=True)

    class Meta:
        abstract = True

class DvAny(Common):
    """
    Abstract root of all datatypes.
    """
    data_name = models.CharField(_('data name'),max_length=110, db_index=True, help_text=_("Type a name for this ComplexType."))
    element_ctid = UUIDField(_("Element UUID"), version=4, help_text=_('This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific DvAdapter complexType.'))

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

    true_values = models.TextField(_('true options'),help_text=_("Enter the set of values that are Boolean TRUEs. For instance, if this is a 'Yes/No' type of concept, usually the 'Yes' is a Boolean TRUE. Enter one per line."))
    false_values = models.TextField(_('false options'),help_text=_("Enter the set of values that are Boolean FALSEs. For instance, if this is a 'Yes/No' type of concept, usually the 'No' is a Boolean FALSE. Enter one per line."))

##    def get_absolute_url(self):
##        return reverse('dvboolean_update/', kwargs={'pk': self.pk})

    def publish(self):
        if self.schema_code == '':
            self.schema_code = publish_DvBoolean(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.save()

    class Meta:
        verbose_name = "DvBoolean"
        verbose_name_plural = "DvBooleans"
        ordering=['prj_name','data_name']

class DvLink(DvAny):
    """
    Used to specify a Universal Resource Identifier.
    """
    relation = models.CharField(_('relation'),max_length=110, help_text=_("The relationship describing the URI. Usually constrained by an ontology such as <a href='http://www.obofoundry.org/cgi-bin/detail.cgi?id=ro'>OBO RO</a>."))

    def publish(self):
        if self.schema_code == '':
            self.schema_code = publish_DvLink(self)
            if len(self.schema_code) > 100:
                self.published = True
                self.save()
            else:
                self.published = False
                self.save()

    class Meta:
        verbose_name = "DvURI"
        verbose_name_plural = "DvURIs"
        ordering=['prj_name','data_name']

    def get_absolute_url(self):
        return reverse('dvuri_update/', kwargs={'pk': self.pk})
