"""

tastypie based DMGen API v1

Resource definitions and Api registrations.
"""
from tastypie.resources import ModelResource
from tastypie.api import Api

from dmgen.models import XdBoolean, XdString, Project

# define the resources based on the models.

#DMGen system wide
class ProjectResource(ModelResource):
    class Meta:
        queryset = Project.objects.all()
        resource_name = 'project'

#XdAny subclasses
class XdBooleanResource(ModelResource):
    class Meta:
        queryset = XdBoolean.objects.all()
        resource_name = 'Xdboolean'
        excludes = ['r_code', 'schema_code']

class XdStringResource(ModelResource):
    class Meta:
        queryset = XdString.objects.all()
        resource_name = 'Xdstring'



# do the registrations here and import into the site urls module
v1_api = Api(api_name='v1')

v1_api.register(ProjectResource())

v1_api.register(XdBooleanResource())
v1_api.register(XdStringResource())

