"""
Import all API v1 components and register them.
v1_api is then imported into urls.py
"""
from tastypie.api import Api

from dmgen.api.resources import ProjectResource, XdBooleanResource, XdLinkResource, XdStringResource, UnitsResource, XdFileResource, XdIntervalResource, ReferenceRangeResource, \
     SimpleReferenceRangeResource, XdOrdinalResource, XdCountResource, XdQuantityResource, XdRatioResource, XdTemporalResource, PartyResource, AuditResource, AttestationResource, \
     ParticipationResource, ClusterResource, EntryResource, DMResource, ModelerResource, NSResource, PredicateResource, PredObjResource

v1_api = Api(api_name='v1')

#  dmgen
v1_api.register(ProjectResource())
v1_api.register(XdBooleanResource())
v1_api.register(XdLinkResource())
v1_api.register(XdStringResource())
v1_api.register(UnitsResource())
v1_api.register(XdFileResource())
v1_api.register(XdIntervalResource())
v1_api.register(ReferenceRangeResource())
v1_api.register(SimpleReferenceRangeResource())
v1_api.register(XdOrdinalResource())
v1_api.register(XdCountResource())
v1_api.register(XdQuantityResource())
v1_api.register(XdRatioResource())
v1_api.register(XdTemporalResource())
v1_api.register(PartyResource())
v1_api.register(AuditResource())
v1_api.register(AttestationResource())
v1_api.register(ParticipationResource())
v1_api.register(ClusterResource())
v1_api.register(EntryResource())
v1_api.register(DMResource())
v1_api.register(ModelerResource())
v1_api.register(NSResource())
v1_api.register(PredicateResource())
v1_api.register(PredObjResource())


