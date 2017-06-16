"""
tastypie based DMGen API v1
Resource definitions
"""
from tastypie.resources import ModelResource
from tastypie.authentication import Authentication

from dmgen.models import (Project, XdBoolean, XdLink, XdString, Units, XdFile, XdInterval, ReferenceRange,
                          SimpleReferenceRange, XdOrdinal, XdCount, XdQuantity, XdRatio,
                          XdTemporal, Party, Audit, Attestation, Participation, Cluster, Entry, DM, Modeler, NS, Predicate, PredObj)


# define the resources based on the models.
class ProjectResource(ModelResource):
    class Meta:
        queryset = Project.objects.all()
        resource_name = 'project'
        always_return_data = True
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()


class ModelerResource(ModelResource):
    class Meta:
        queryset = Modeler.objects.all()
        resource_name = 'modeler'
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()


class NSResource(ModelResource):
    class Meta:
        queryset = NS.objects.all()
        resource_name = 'ns'
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()


class PredicateResource(ModelResource):
    class Meta:
        queryset = Predicate.objects.all()
        resource_name = 'predicate'
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()


class PredObjResource(ModelResource):
    class Meta:
        queryset = PredObj.objects.all()
        resource_name = 'predobj'
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()


# XdAny subclasses
class XdBooleanResource(ModelResource):

    class Meta:
        queryset = XdBoolean.objects.all()
        resource_name = 'xdboolean'
        excludes = ['r_code', 'schema_code']
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()


class XdLinkResource(ModelResource):

    class Meta:
        queryset = XdLink.objects.all()
        resource_name = 'xdlink'
        excludes = ['r_code', 'schema_code']
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()


class XdStringResource(ModelResource):

    class Meta:
        queryset = XdString.objects.all()
        resource_name = 'xdstring'
        excludes = ['r_code', 'schema_code']
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()


class UnitsResource(ModelResource):

    class Meta:
        queryset = Units.objects.all()
        resource_name = 'units'
        excludes = ['r_code', 'schema_code']
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()


class XdFileResource(ModelResource):

    class Meta:
        queryset = XdFile.objects.all()
        resource_name = 'xdfile'
        excludes = ['r_code', 'schema_code']
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()


class XdIntervalResource(ModelResource):

    class Meta:
        queryset = XdInterval.objects.all()
        resource_name = 'xdinterval'
        excludes = ['r_code', 'schema_code']
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()


class ReferenceRangeResource(ModelResource):

    class Meta:
        queryset = ReferenceRange.objects.all()
        resource_name = 'referencerange'
        excludes = ['r_code', 'schema_code']
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()


class SimpleReferenceRangeResource(ModelResource):

    class Meta:
        queryset = SimpleReferenceRange.objects.all()
        resource_name = 'simplereferencerange'
        excludes = ['r_code', 'schema_code']
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()


class XdOrdinalResource(ModelResource):

    class Meta:
        queryset = XdOrdinal.objects.all()
        resource_name = 'xdordinal'
        excludes = ['r_code', 'schema_code']
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()


class XdCountResource(ModelResource):

    class Meta:
        queryset = XdCount.objects.all()
        resource_name = 'xdcount'
        excludes = ['r_code', 'schema_code']
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()


class XdQuantityResource(ModelResource):

    class Meta:
        queryset = XdQuantity.objects.all()
        resource_name = 'xdquantity'
        excludes = ['r_code', 'schema_code']
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()


class XdRatioResource(ModelResource):

    class Meta:
        queryset = XdRatio.objects.all()
        resource_name = 'xdratio'
        excludes = ['r_code', 'schema_code']
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()


class XdTemporalResource(ModelResource):

    class Meta:
        queryset = XdTemporal.objects.all()
        resource_name = 'xdtemporal'
        excludes = ['r_code', 'schema_code']
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()


class PartyResource(ModelResource):

    class Meta:
        queryset = Party.objects.all()
        resource_name = 'party'
        excludes = ['r_code', 'schema_code']
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()


class AuditResource(ModelResource):

    class Meta:
        queryset = Audit.objects.all()
        resource_name = 'audit'
        excludes = ['r_code', 'schema_code']
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()


class AttestationResource(ModelResource):

    class Meta:
        queryset = Attestation.objects.all()
        resource_name = 'attestation'
        excludes = ['r_code', 'schema_code']
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()


class ParticipationResource(ModelResource):

    class Meta:
        queryset = Participation.objects.all()
        resource_name = 'participation'
        excludes = ['r_code', 'schema_code']
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()


class ClusterResource(ModelResource):

    class Meta:
        queryset = Cluster.objects.all()
        resource_name = 'cluster'
        excludes = ['r_code', 'schema_code']
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()


class EntryResource(ModelResource):

    class Meta:
        queryset = Entry.objects.all()
        resource_name = 'entry'
        excludes = ['r_code', 'schema_code']
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()


class DMResource(ModelResource):

    class Meta:
        queryset = DM.objects.all()
        resource_name = 'dm'
        excludes = ['r_code', 'schema_code']
        # TODO: Fix with correct authentication before deployment.
        authentication = Authentication()
