from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages


from cmgen.models import *
from cmgen.forms import *

def republish(modeladmin, request, queryset):
    if request.user.is_superuser:
        for obj in queryset:
            if  obj.published == True: # publish and save code
                obj.schema_code = ''
                obj.r_code = ''
                obj.xqr_code = ''
                obj.xqw_code = ''
                obj.save()
                msg = obj.publish(request)
                modeladmin.message_user(request, msg[0], msg[1])
republish.short_description = _("Re-Publish (Development Only!)")


def copy_cluster(modeladmin, request, queryset):
    for obj in queryset:
        new_obj = obj
        new_obj.pk = None
        new_obj.cluster_subject = (obj.cluster_subject +" (***COPY***)").encode("utf-8")
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = str(uuid4())
        new_obj.save()
copy_cluster.short_description = _("Copy Cluster(s)")

def copy_dt(modeladmin, request, queryset):
    for obj in queryset:
        new_obj = obj
        new_obj.pk = None
        new_obj.data_name = (obj.data_name +" (***COPY***)").encode("utf-8")
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = str(uuid4())
        new_obj.adapter_id = str(uuid4())
        new_obj.save()
copy_dt.short_description = _("Copy Datatype(s)")

def copy_labeled(modeladmin, request, queryset):
    for obj in queryset:
        new_obj = obj
        new_obj.pk = None
        new_obj.label = (obj.label +" (***COPY***)").encode("utf-8")
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = str(uuid4())
        new_obj.save()
copy_labeled.short_description = _("Copy Item(s)")

def make_published(modeladmin, request, queryset):
    for obj in queryset:
        msg = obj.publish(request)
        modeladmin.message_user(request, msg[0], msg[1])
make_published.short_description = "Publish"

def unpublish(modeladmin, request, queryset):
    if request.user.is_superuser:
        for obj in queryset:
            obj.schema_code = ''
            obj.r_code = ''
            obj.xqr_code = ''
            obj.xqw_code = ''
            obj.published = False
            obj.save()
    else:
        modeladmin.message_user(request,"User: "+request.user.username+" is not authorized to unpublish items.", messages.WARNING)
unpublish.short_description = _("UnPublish (Development Only!)")

def generate_cm(modeladmin, request, queryset):
    for obj in queryset:
        obj.generate()
generate_cm.short_description = _("Generate CM")

class ProjectAdmin(admin.ModelAdmin):
    ordering = ['prj_name',]
    list_display = ('prj_name','description')
admin.site.register(Project,ProjectAdmin)

class PredicateAdmin(admin.ModelAdmin):
    ordering = ['pred_def',]
admin.site.register(Predicate,PredicateAdmin)

class PredObjAdmin(admin.ModelAdmin):
    ordering = ['prj_name', 'name',]

admin.site.register(PredObj,PredObjAdmin)

class DvBooleanAdmin(admin.ModelAdmin):
    actions = [make_published, unpublish,copy_dt,republish]
    ordering = ['prj_name','data_name']
    search_fields = ['data_name','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
    list_display = ('data_name','prj_name','published',)
    filter_horizontal = ['semantics',]

    form = DvBooleanAdminForm

    fieldsets = (
        (None, {
        'fields':(('data_name','prj_name','lang'),'true_values','false_values',)}),
        ("Require dates in instances?", {'classes':('collapse',),'fields':(('vtb_required', 'vte_required'),)}),
        ("Additional Information", {'classes':('wide',),
                       'fields':('description','semantics',)}),
        ("Advanced", {'classes':('collapse',),'fields':('asserts',)}),
        ("Published Code (read-only)", {'classes':('collapse',),
                           'fields':('schema_code','r_code','xqr_code','xqw_code',)}),
    )

admin.site.register(DvBoolean,DvBooleanAdmin)

class DvLinkAdmin(admin.ModelAdmin):
    actions = [make_published, unpublish,copy_dt,republish]
    ordering = ['prj_name','data_name']
    search_fields = ['data_name','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
    list_display = ('data_name','prj_name','published',)
    filter_horizontal = ['semantics',]

    form = DvLinkAdminForm

    fieldsets = (
        (None, {
        'fields':(('data_name','prj_name','lang',),'relation','relation_uri','link_value',)}),
        ("Require dates in instances?", {'classes':('collapse',),'fields':(('vtb_required', 'vte_required'),)}),
        ("Additional Information", {'classes':('wide',),
                       'fields':('description','semantics',)}),
        ("Advanced", {'classes':('collapse',),'fields':('asserts',)}),
        ("Published Code (read-only)", {'classes':('collapse',),
                           'fields':('schema_code','r_code','xqr_code','xqw_code',)}),
    )

admin.site.register(DvLink,DvLinkAdmin)

class DvStringAdmin(admin.ModelAdmin):
    actions = [make_published, unpublish,copy_dt,republish]
    ordering = ['prj_name','data_name']
    search_fields = ['data_name','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
    list_display = ('data_name','prj_name','published',)
    filter_horizontal = ['semantics',]

    form = DvStringAdminForm

    fieldsets = (
        (None, {
        'fields':(('data_name','prj_name','lang'),)}),
        ("Require dates in instances?", {'classes':('collapse',),'fields':(('vtb_required', 'vte_required'),)}),
        ("Additional Information", {'classes':('wide',),
                       'fields':('lang_required','description','semantics',)}),
        ("Other Constraints", {'classes':('collapse',),
                         'fields':(('exact_length','min_length','max_length'),
                                    ('default_value','whitespace','pattern'),'enums','enums_def',)}),
        ("Advanced", {'classes':('collapse',),'fields':('asserts',)}),
        ("Published Code (read-only)", {'classes':('collapse',),
                           'fields':('schema_code','r_code','xqr_code','xqw_code',)}),
    )

admin.site.register(DvString,DvStringAdmin)

class DvParsableAdmin(admin.ModelAdmin):
    actions = [make_published, unpublish,copy_dt,republish]
    ordering = ['prj_name','data_name']
    search_fields = ['data_name','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
    list_display = ('data_name','prj_name','published',)
    filter_horizontal = ['semantics',]

    form = DvParsableAdminForm
    fieldsets = (
        (None, {
        'fields':(('data_name','prj_name','lang'),)}),
        ("Require dates in instances?", {'classes':('collapse',),'fields':(('vtb_required', 'vte_required'),)}),
        ("Additional Information", {'classes':('wide',),
                       'fields':('lang_required','description','semantics',)}),
        ("Other Constraints", {'classes':('collapse',),
                         'fields':('encoding','dvparsable_value','fenums','fenums_def',)}),
        ("Advanced", {'classes':('collapse',),'fields':('asserts',)}),
        ("Published Code (read-only)", {'classes':('collapse',),
                           'fields':('schema_code','r_code','xqr_code','xqw_code',)}),
    )

admin.site.register(DvParsable,DvParsableAdmin)

class DvMediaAdmin(admin.ModelAdmin):
    actions = [make_published, unpublish,copy_dt,republish]
    ordering = ['prj_name','data_name']
    search_fields = ['data_name','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
    list_display = ('data_name','prj_name','published',)
    filter_horizontal = ['semantics',]

    form = DvMediaAdminForm
    fieldsets = (
        (None, {
        'fields':(('data_name','prj_name','lang'),)}),
        ("Require dates in instances?", {'classes':('collapse',),'fields':(('vtb_required', 'vte_required'),)}),
        ("Additional Information", {'classes':('wide',),
                       'fields':('content','lang_required','description','semantics',)}),
        ("Other Constraints", {'classes':('collapse',),
                         'fields':(('alt_required','media_required','comp_required','hash_required'),
                                   'encoding','media_type','compression_type','hash_function','fenums','fenums_def',)}),
        ("Advanced", {'classes':('collapse',),'fields':('asserts',)}),
        ("Published Code (read-only)", {'classes':('collapse',),
                           'fields':('schema_code','r_code','xqr_code','xqw_code',)}),
    )

admin.site.register(DvMedia,DvMediaAdmin)

class DvIntervalAdmin(admin.ModelAdmin):
    actions = [make_published, unpublish,copy_dt,republish]
    ordering = ['prj_name','data_name']
    search_fields = ['data_name','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
    list_display = ('data_name','prj_name','published',)
    filter_horizontal = ['semantics',]

    form = DvIntervalAdminForm
    fieldsets = (
        (None, {
        'fields':(('data_name','prj_name','lang'),)}),
        ("Require dates in instances?", {'classes':('collapse',),'fields':(('vtb_required', 'vte_required'),)}),
        ("Additional Information", {'classes':('wide',),
                       'fields':(('lower','upper'),('lower_included','upper_included'),
                                 ('lower_bounded','upper_bounded'),'description','semantics',)}),
        ("Advanced", {'classes':('collapse',),'fields':('asserts',)}),
        ("Published Code (read-only)", {'classes':('collapse',),
                           'fields':('schema_code','r_code','xqr_code','xqw_code',)}),
    )

admin.site.register(DvInterval,DvIntervalAdmin)

class ReferenceRangeAdmin(admin.ModelAdmin):
    actions = [make_published, unpublish,copy_dt,republish]
    ordering = ['prj_name','data_name']
    search_fields = ['data_name','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
    list_display = ('data_name','prj_name','published',)
    filter_horizontal = ['semantics',]

    form = ReferenceRangeAdminForm
    fieldsets = (
        (None, {
        'fields':(('data_name','prj_name','lang'),)}),
        ("Require dates in instances?", {'classes':('collapse',),'fields':(('vtb_required', 'vte_required'),)}),
        ("Additional Information", {'classes':('wide',),
                       'fields':('definition',('is_normal','data_range'),'description','semantics',)}),
        ("Advanced", {'classes':('collapse',),'fields':('asserts',)}),
        ("Published Code (read-only)", {'classes':('collapse',),
                           'fields':('schema_code','r_code','xqr_code','xqw_code',)}),
    )

admin.site.register(ReferenceRange,ReferenceRangeAdmin)

class DvOrdinalAdmin(admin.ModelAdmin):
    actions = [make_published, unpublish,copy_dt,republish]
    ordering = ['prj_name','data_name']
    search_fields = ['data_name','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
    list_display = ('data_name','prj_name','published',)
    filter_horizontal = ['semantics','reference_ranges']

    form = DvOrdinalAdminForm

    fieldsets = (
        (None, {
        'fields':(('data_name','prj_name','lang'),)}),
        ("Require dates in instances?", {'classes':('collapse',),'fields':(('vtb_required', 'vte_required'),)}),
        ("Additional Information", {'classes':('wide',),
                       'fields':('reference_ranges','normal_status','ordinals','symbols','symbols_def',
                                 'description','semantics',)}),
        ("Advanced", {'classes':('collapse',),'fields':('asserts',)}),
        ("Published Code (read-only)", {'classes':('collapse',),
                           'fields':('schema_code','r_code','xqr_code','xqw_code',)}),
    )

admin.site.register(DvOrdinal,DvOrdinalAdmin)

class DvCountAdmin(admin.ModelAdmin):
    actions = [make_published, unpublish,copy_dt,republish]
    ordering = ['prj_name','data_name']
    search_fields = ['data_name','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
    list_display = ('data_name','prj_name','published',)
    filter_horizontal = ['semantics','reference_ranges']

    form = DvCountAdminForm
    fieldsets = (
        (None, {
        'fields':(('data_name','prj_name','lang'),)}),
        ("Require dates in instances?", {'classes':('collapse',),'fields':(('vtb_required', 'vte_required'),)}),
        ("Additional Information", {'classes':('wide',),
                       'fields':('reference_ranges','normal_status','units',
                                 'description','semantics',)}),
        ("Other Constraints", {'classes':('collapse',),
                               'fields':(('min_inclusive','max_inclusive'),
                                         ('min_exclusive','max_exclusive'),('fraction_digits','total_digits'),)}),
        ("Advanced", {'classes':('collapse',),'fields':('asserts',)}),
        ("Published Code (read-only)", {'classes':('collapse',),
                           'fields':('schema_code','r_code','xqr_code','xqw_code',)}),
    )

admin.site.register(DvCount,DvCountAdmin)

class DvQuantityAdmin(admin.ModelAdmin):
    actions = [make_published, unpublish,copy_dt,republish]
    ordering = ['prj_name','data_name']
    search_fields = ['data_name','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
    list_display = ('data_name','prj_name','published',)
    filter_horizontal = ['semantics','reference_ranges']

    form = DvQuantityAdminForm
    fieldsets = (
        (None, {
        'fields':(('data_name','prj_name','lang'),)}),
        ("Require dates in instances?", {'classes':('collapse',),'fields':(('vtb_required', 'vte_required'),)}),
        ("Additional Information", {'classes':('wide',),
                       'fields':('reference_ranges','normal_status','units',
                                 'description','semantics',)}),
        ("Other Constraints", {'classes':('collapse',),
                               'fields':(('min_inclusive','max_inclusive'),
                                         ('min_exclusive','max_exclusive'),('fraction_digits','total_digits'),)}),
        ("Advanced", {'classes':('collapse',),'fields':('asserts',)}),
        ("Published Code (read-only)", {'classes':('collapse',),
                           'fields':('schema_code','r_code','xqr_code','xqw_code',)}),
    )

admin.site.register(DvQuantity,DvQuantityAdmin)

class DvRatioAdmin(admin.ModelAdmin):
    actions = [make_published, unpublish,copy_dt,republish]
    ordering = ['prj_name','data_name']
    search_fields = ['data_name','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
    list_display = ('data_name','prj_name','published',)
    filter_horizontal = ['semantics','reference_ranges']

    form = DvRatioAdminForm

    fieldsets = (
        (None, {
        'fields':(('data_name','prj_name','lang'),)}),
        ("Require dates in instances?", {'classes':('collapse',),'fields':(('vtb_required', 'vte_required'),)}),
        ("Additional Information", {'classes':('wide',),
                       'fields':('reference_ranges','normal_status','ratio_type',
                                 'description','semantics',)}),
        ("Ratio Constraints", {'classes':('collapse',),
                               'fields':('ratio_units',('min_inclusive','max_inclusive'),
                                         ('min_exclusive','max_exclusive'),('fraction_digits','total_digits'),)}),
        ("Numerator Constraints", {'classes':('collapse',),
                               'fields':('num_units',('num_min_inclusive','num_max_inclusive'),
                                         ('num_min_exclusive','num_max_exclusive'),('num_fraction_digits','num_total_digits'),)}),
        ("Denominator Constraints", {'classes':('collapse',),
                               'fields':('den_units',('den_min_inclusive','den_max_inclusive'),
                                         ('den_min_exclusive','den_max_exclusive'),('den_fraction_digits','den_total_digits'),)}),
        ("Advanced", {'classes':('collapse',),'fields':('asserts',)}),
        ("Published Code (read-only)", {'classes':('collapse',),
                           'fields':('schema_code','r_code','xqr_code','xqw_code',)}),
    )

admin.site.register(DvRatio,DvRatioAdmin)

class DvTemporalAdmin(admin.ModelAdmin):
    actions = [make_published, unpublish,copy_dt,republish]
    ordering = ['prj_name','data_name']
    search_fields = ['data_name','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
    list_display = ('data_name','prj_name','published',)
    filter_horizontal = ['semantics','reference_ranges']

    form = DvTemporalAdminForm
    require_text = """Selecting one required element means only that element is allowed.
    You cannot select any in the Allow section below."""
    allow_text = """Select as many as desired to allow partial user input. However, only one duration type is allowed.
    If you select a duration type, no other types are allowed."""
    fieldsets = (
        (None, {
        'fields':(('data_name','prj_name','lang'),)}),
        ("Require dates in instances?", {'classes':('collapse',),'fields':(('vtb_required', 'vte_required'),)}),
        ("Additional Information", {'classes':('wide',),
                       'fields':('reference_ranges','normal_status',
                                 'description','semantics',)}),
        ("Require One", {'description':require_text,
            'classes':('collapse',),
                               'fields':('require_date','require_time','require_datetime','require_day','require_month','require_year','require_year_month','require_month_day',
                                         'require_duration','require_ymduration','require_dtduration',)}),
        ("Allow", {'description':allow_text,
            'classes':('wide',),
                         'fields':('allow_date','allow_time','allow_datetime','allow_day','allow_month','allow_year','allow_year_month','allow_month_day',
                                   ('allow_duration','allow_ymduration','allow_dtduration'),)}),
        ("Advanced", {'classes':('collapse',),'fields':('asserts',)}),
        ("Published Code (read-only)", {'classes':('collapse',),
                           'fields':('schema_code','r_code','xqr_code','xqw_code',)}),
    )

admin.site.register(DvTemporal,DvTemporalAdmin)

class PartyAdmin(admin.ModelAdmin):
    actions = [make_published, unpublish,copy_labeled,republish]
    ordering = ['prj_name','label']
    search_fields = ['label','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
    list_display = ('label','prj_name','published',)
    filter_horizontal = ['semantics','party_ref']

    form = PartyAdminForm
    fieldsets = (
        (None, {
        'fields':(('label','prj_name','lang'),)}),
        (None, {'classes':('wide',),
                       'fields':('require_name','party_details','party_ref','description','semantics',)}),
        ("Advanced", {'classes':('collapse',),'fields':('asserts',)}),
        ("Published Code (read-only)", {'classes':('collapse',),
                           'fields':('schema_code','r_code','xqr_code','xqw_code',)}),
    )

admin.site.register(Party,PartyAdmin)

class AuditAdmin(admin.ModelAdmin):
    actions = [make_published, unpublish,copy_labeled,republish]
    ordering = ['prj_name','label']
    search_fields = ['label','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
    list_display = ('label','prj_name','published',)
    filter_horizontal = ['semantics',]

    form = AuditAdminForm
    fieldsets = (
        (None, {
        'fields':(('label','prj_name','lang'),)}),
        (None, {'classes':('wide',),
                       'fields':('system_id','system_user','location','description','semantics',)}),
        ("Advanced", {'classes':('collapse',),'fields':('asserts',)}),
        ("Published Code (read-only)", {'classes':('collapse',),
                           'fields':('schema_code','r_code','xqr_code','xqw_code',)}),
    )

admin.site.register(Audit,AuditAdmin)

class AttestationAdmin(admin.ModelAdmin):
    actions = [make_published, unpublish,copy_labeled,republish]
    ordering = ['prj_name','label']
    search_fields = ['label','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
    list_display = ('label','prj_name','published',)
    filter_horizontal = ['semantics',]

    form = AttestationAdminForm
    fieldsets = (
        (None, {
        'fields':(('label','prj_name','lang'),)}),
        (None, {'classes':('wide',),
                       'fields':('attested_view','proof','reason','committer','description','semantics',)}),
        ("Advanced", {'classes':('collapse',),'fields':('asserts',)}),
        ("Published Code (read-only)", {'classes':('collapse',),
                           'fields':('schema_code','r_code','xqr_code','xqw_code',)}),
    )


admin.site.register(Attestation,AttestationAdmin)

class ParticipationAdmin(admin.ModelAdmin):
    actions = [make_published, unpublish,copy_labeled,republish]
    ordering = ['prj_name','label']
    search_fields = ['label','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
    list_display = ('label','prj_name','published',)
    filter_horizontal = ['semantics',]

    form = ParticipationAdminForm
    fieldsets = (
        (None, {
        'fields':(('label','prj_name','lang'),)}),
        (None, {'classes':('wide',),
                       'fields':('performer','function','mode','description','semantics',)}),
        ("Advanced", {'classes':('collapse',),'fields':('asserts',)}),
        ("Published Code (read-only)", {'classes':('collapse',),
                           'fields':('schema_code','r_code','xqr_code','xqw_code',)}),
    )

admin.site.register(Participation,ParticipationAdmin)

class ClusterAdmin(admin.ModelAdmin):
    actions = [make_published, unpublish,copy_cluster,republish]
    ordering = ['prj_name','cluster_subject']
    search_fields = ['cluster_subject','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
    list_display = ('cluster_subject','prj_name','published',)
    filter_horizontal = ['semantics','clusters','dvboolean','dvlink','dvstring','dvparsable','dvmedia',
                                 'dvordinal','dvcount','dvquantity','dvratio','dvtemporal',]

    form = ClusterAdminForm
    fieldsets = (
        (None, {
        'fields':(('cluster_subject','prj_name','lang'),)}),
        (None, {'classes':('wide',),
                       'fields':('description','semantics','clusters','dvboolean','dvlink','dvstring','dvparsable','dvmedia',
                                 'dvordinal','dvcount','dvquantity','dvratio','dvtemporal', )}),
        ("Advanced", {'classes':('collapse',),'fields':('asserts',)}),
        ("Published Code (read-only)", {'classes':('collapse',),
                           'fields':('schema_code','r_code','xqr_code','xqw_code',)}),
    )

admin.site.register(Cluster,ClusterAdmin)

class ConceptAdmin(admin.ModelAdmin):
    actions = [make_published, generate_cm, unpublish,republish]
    ordering = ['prj_name','title']
    search_fields = ['title','ct_id']
    readonly_fields = ['published','schema_code','r_code','xqr_code','xqw_code']
    list_display = ('title','prj_name','published',)
    filter_horizontal = ['semantics','contributors','participations','audits','links',]

    form = ConceptAdminForm

    fieldsets = (
        (None, {
        'fields':(('title','prj_name','lang'),)}),
        ("Metadata", {'classes':('wide',),
                       'fields':('author','contributors','license',('rights_holder_name','rights_holder_email'),
                                 'relation',)}),
        (None, {'classes':('wide',),
                      'fields':('description','semantics',)}),
        ("Structure", {'classes':('collapse',),
                               'fields':('encoding','data','subject','protocol','workflow','attested',
                                         'participations','audits','links',)}),
        ("Advanced", {'classes':('collapse',),'fields':('asserts',)}),
        ("Published Code (read-only)", {'classes':('collapse',),
                           'fields':('schema_code','r_code','xqr_code','xqw_code',)}),
    )

admin.site.register(Concept,ConceptAdmin)

