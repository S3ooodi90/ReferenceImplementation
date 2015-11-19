"""

tastypie based DMGen API v1

Resource definitions and Api registrations.
"""
from tastypie.resources import ModelResource
from tastypie.api import Api

from dmgen.models import DvBoolean, DvString, Project

# define the resources based on the models.

#DMGen system wide
class ProjectResource(ModelResource):
    class Meta:
        queryset = Project.objects.all()
        resource_name = 'project'

#DvAny subclasses
class DvBooleanResource(ModelResource):
    class Meta:
        queryset = DvBoolean.objects.all()
        resource_name = 'dvboolean'
        excludes = ['r_code', 'schema_code']

class DvStringResource(ModelResource):
    class Meta:
        queryset = DvString.objects.all()
        resource_name = 'dvstring'



# do the registrations here and import into the site urls module
v1_api = Api(api_name='v1')

v1_api.register(ProjectResource())

v1_api.register(DvBooleanResource())
v1_api.register(DvStringResource())

