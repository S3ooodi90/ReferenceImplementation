from django.contrib import admin

from models import *

def make_published(modeladmin, request, queryset):
    for obj in queryset:
        obj.publish()
make_published.short_description = "Publish"

def generate_cm(modeladmin, request, queryset):
    for obj in queryset:
        obj.generate()
generate_cm.short_description = _("Generate CM")

class ProjectAdmin(admin.ModelAdmin):
    ordering = ['prj_name',]
    list_display = ('prj_name','description')
admin.site.register(Project,ProjectAdmin)

class PredicateAdmin(admin.ModelAdmin):
    pass
admin.site.register(Predicate,PredicateAdmin)

class PredObjAdmin(admin.ModelAdmin):
    pass
admin.site.register(PredObj,PredObjAdmin)

class DvBooleanAdmin(admin.ModelAdmin):
    actions = [make_published]
    ordering = ['prj_name','data_name']
    search_fields = ['data_name','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
admin.site.register(DvBoolean,DvBooleanAdmin)

class DvLinkAdmin(admin.ModelAdmin):
    actions = [make_published]
    ordering = ['prj_name','data_name']
    search_fields = ['data_name','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
admin.site.register(DvLink,DvLinkAdmin)

class DvStringAdmin(admin.ModelAdmin):
    actions = [make_published]
    ordering = ['prj_name','data_name']
    search_fields = ['data_name','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
admin.site.register(DvString,DvStringAdmin)

class DvParsableAdmin(admin.ModelAdmin):
    actions = [make_published]
    ordering = ['prj_name','data_name']
    search_fields = ['data_name','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
admin.site.register(DvParsable,DvParsableAdmin)

class DvMediaAdmin(admin.ModelAdmin):
    actions = [make_published]
    ordering = ['prj_name','data_name']
    search_fields = ['data_name','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
admin.site.register(DvMedia,DvMediaAdmin)

class DvIntervalAdmin(admin.ModelAdmin):
    actions = [make_published]
    ordering = ['prj_name','data_name']
    search_fields = ['data_name','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
admin.site.register(DvInterval,DvIntervalAdmin)

class ReferenceRangeAdmin(admin.ModelAdmin):
    actions = [make_published]
    ordering = ['prj_name','data_name']
    search_fields = ['data_name','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
admin.site.register(ReferenceRange,ReferenceRangeAdmin)

class DvOrdinalAdmin(admin.ModelAdmin):
    actions = [make_published]
    ordering = ['prj_name','data_name']
    search_fields = ['data_name','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
admin.site.register(DvOrdinal,DvOrdinalAdmin)

class DvCountAdmin(admin.ModelAdmin):
    actions = [make_published]
    ordering = ['prj_name','data_name']
    search_fields = ['data_name','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
admin.site.register(DvCount,DvCountAdmin)

class DvQuantityAdmin(admin.ModelAdmin):
    actions = [make_published]
    ordering = ['prj_name','data_name']
    search_fields = ['data_name','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
admin.site.register(DvQuantity,DvQuantityAdmin)

class DvRatioAdmin(admin.ModelAdmin):
    actions = [make_published]
    ordering = ['prj_name','data_name']
    search_fields = ['data_name','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
admin.site.register(DvRatio,DvRatioAdmin)

class DvTemporalAdmin(admin.ModelAdmin):
    actions = [make_published]
    ordering = ['prj_name','data_name']
    search_fields = ['data_name','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
admin.site.register(DvTemporal,DvTemporalAdmin)

class PartyAdmin(admin.ModelAdmin):
    actions = [make_published]
    ordering = ['prj_name','label']
    search_fields = ['label','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
admin.site.register(Party,PartyAdmin)

class AuditAdmin(admin.ModelAdmin):
    actions = [make_published]
    ordering = ['prj_name','label']
    search_fields = ['label','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
admin.site.register(Audit,AuditAdmin)

class AttestationAdmin(admin.ModelAdmin):
    actions = [make_published]
    ordering = ['prj_name','label']
    search_fields = ['label','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
admin.site.register(Attestation,AttestationAdmin)

class ParticipationAdmin(admin.ModelAdmin):
    actions = [make_published]
    ordering = ['prj_name','label']
    search_fields = ['label','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
admin.site.register(Participation,ParticipationAdmin)

class ClusterAdmin(admin.ModelAdmin):
    actions = [make_published]
    ordering = ['prj_name','cluster_subject']
    search_fields = ['cluster_subject','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
admin.site.register(Cluster,ClusterAdmin)

class ConceptAdmin(admin.ModelAdmin):
    actions = [make_published, generate_cm]
    ordering = ['prj_name','title']
    search_fields = ['title','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
admin.site.register(Concept,ConceptAdmin)

