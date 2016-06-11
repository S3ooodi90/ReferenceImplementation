"""
Django Admin definitions.
"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

from dmgen.models import *
from dmgen.forms import *
from dmgen.generator import generateDM

from .exceptions import CodesImportError

# disable Django's sitewide delete
admin.site.disable_action('delete_selected')
# now add our own that checks for creator


def delete_mcs(modeladmin, request, queryset):
    # get the current users modeler id
    cur_modeler = Modeler.objects.filter(user=request.user)
    if cur_modeler:
        for obj in queryset:
            if hasattr(obj, 'label'):
                name = obj.label
            elif hasattr(obj, 'title'):
                name = obj.title
            else:
                name = " this object."
            if obj.creator.id != cur_modeler[0].id and request.user.is_superuser is False:
                modeladmin.message_user(request, "Cannot delete the model component " + name + " because " + cur_modeler[
                    0].user.username + " is not the creator.", messages.ERROR)
            else:
                    obj.delete()
    else:
        modeladmin.message_user(request, request.user.username +
                                " is not a registered DMGen modeler. ", messages.ERROR)

delete_mcs.short_description = _("Delete MC(s)")


def make_published(modeladmin, request, queryset):
    for obj in queryset:
        if "(***COPY***)" in obj.__str__():  # skip publishing a copy.
            msg = (
                obj.__str__() + " --Cannot publish a copy until it is edited.", messages.ERROR)
            continue
        if not obj.published and obj.schema_code == '':  # publish and save code
            msg = obj.publish(request)
        else:
            msg = (obj.__str__() + " is already Published.", messages.WARNING)

        modeladmin.message_user(request, msg[0], msg[1])
make_published.short_description = _("Publish")


def republish(modeladmin, request, queryset):
    if request.user.is_superuser:
        for obj in queryset:
            if obj.published is True:  # re-publish and save code
                obj.published = False
                obj.schema_code = ''
                obj.r_code = ''
                obj.save()
                msg = obj.publish(request)
                modeladmin.message_user(request, msg[0], msg[1])
    else:
        msg = ("User: " + request.user.username +
               " is not authorized to unpublish items.", messages.ERROR)

republish.short_description = _("Re-Publish (Development Only!)")


def republishAll(modeladmin, request, queryset):
    if request.user.is_superuser:
        q = XdBoolean.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " XdBooleans.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.r_code = ''
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " wasn't republished.")
            else:
                print(obj.__str__() + " was republished.")


        q = Units.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " Units.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.r_code = ''
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " wasn't republished.")
            else:
                print(obj.__str__() + " was republished.")

        q = XdString.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " XdStrings.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.r_code = ''
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " wasn't republished.")
            else:
                print(obj.__str__() + " was republished.")

        q = XdLink.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " XdLinks.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.r_code = ''
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " wasn't republished.")
            else:
                print(obj.__str__() + " was republished.")

        q = XdInterval.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " XdIntervals.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.r_code = ''
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " wasn't republished.")
            else:
                print(obj.__str__() + " was republished.")

        q = ReferenceRange.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " ReferenceRanges.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.r_code = ''
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " wasn't republished.")
            else:
                print(obj.__str__() + " was republished.")

        q = XdOrdinal.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " XdOrdinals.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.r_code = ''
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " wasn't republished.")
            else:
                print(obj.__str__() + " was republished.")

        q = XdCount.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " XdCounts.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.r_code = ''
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " wasn't republished.")
            else:
                print(obj.__str__() + " was republished.")

        q = XdQuantity.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " XdQuantities.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.r_code = ''
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " wasn't republished.")
            else:
                print(obj.__str__() + " was republished.")

        q = XdRatio.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " XdRatios.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.r_code = ''
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " wasn't republished.")
            else:
                print(obj.__str__() + " was republished.")

        q = XdFile.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " XdFiles.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.r_code = ''
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " wasn't republished.")
            else:
                print(obj.__str__() + " was republished.")

        q = XdTemporal.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " XdTemporals.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.r_code = ''
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " wasn't republished.")
            else:
                print(obj.__str__() + " was republished.")

        q = Cluster.objects.filter(published=True)
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.r_code = ''
            obj.save()

        q2 = []
        q3 = []
        print("Re-publishing " + str(len(q)) + " Clusters.")
        print("Clusters pass #1")
        for obj in q:
            obj.publish(request)
            print(obj.label, obj.published)
            if obj.published is False:
                q2.append(obj)

        print("Clusters pass #2")
        print("Re-publishing " + str(len(q2)) + " Clusters.")
        for obj in q2:
            if obj.published is False:
                obj.publish(request)
                if obj.published is False:
                    q3.append(obj)

        print("Clusters pass #3")
        print("Re-publishing " + str(len(q3)) + " Clusters.")
        for obj in q3:
            if obj.published is False:
                obj.publish(request)
                if obj.published is False:
                    print("Could not publish: ", obj.__str__())

        q = Party.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " Partys.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.r_code = ''
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " wasn't republished.")

        q = Participation.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " Participations.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.r_code = ''
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " wasn't republished.")

        q = Attestation.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " Attestations.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.r_code = ''
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " wasn't republished.")

        q = Audit.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " Audits.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.r_code = ''
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " wasn't republished.")

        q = Entry.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " Entrys.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.r_code = ''
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " wasn't republished.")

        print("Finished!!!!!")
    else:
        msg = ("User: " + request.user.username +
               " is not authorized to Republish items.", messages.ERROR)

republishAll.short_description = _("Re-Publish ALL (Development Only!)")


def unpublish(modeladmin, request, queryset):
    if request.user.is_superuser:
        for obj in queryset:
            obj.schema_code = ''
            obj.r_code = ''
            obj.published = False
            msg = (obj.__str__() + " was Unpublished!", messages.SUCCESS)
            obj.save()
    else:
        msg = ("User: " + request.user.username +
               " is not authorized to unpublish items.", messages.ERROR)

    modeladmin.message_user(request, msg[0], msg[1])

unpublish.short_description = _("UnPublish (Development Only!)")


def copy_dt(modeladmin, request, queryset):
    cur_modeler = Modeler.objects.filter(user=request.user)
    for obj in queryset:
        new_obj = obj
        new_obj.creator = cur_modeler[0]
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = None
        new_obj.element_ctid = None
        new_obj.save()
        msg = (obj.__str__() + " was Created!", messages.SUCCESS)

        modeladmin.message_user(request, msg[0], msg[1])

copy_dt.short_description = _("Copy Datatype(s)")


def copy_labeled(modeladmin, request, queryset):
    cur_modeler = Modeler.objects.filter(user=request.user)
    for obj in queryset:
        new_obj = obj
        new_obj.creator = cur_modeler[0]
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = None
        new_obj.element_ctid = None
        new_obj.save()
        msg = (obj.__str__() + " was Created!", messages.SUCCESS)

        modeladmin.message_user(request, msg[0], msg[1])

copy_labeled.short_description = _("Copy Item(s)")


def copy_cluster(modeladmin, request, queryset):
    cur_modeler = Modeler.objects.filter(user=request.user)
    for obj in queryset:
        new_obj = obj
        new_obj.creator = cur_modeler[0]
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = None
        new_obj.element_ctid = None
        new_obj.save()
        msg = (obj.__str__() + " was Created!", messages.SUCCESS)

        modeladmin.message_user(request, msg[0], msg[1])

copy_cluster.short_description = _("Copy Cluster(s)")


def copy_entry(modeladmin, request, queryset):
    cur_modeler = Modeler.objects.filter(user=request.user)
    for obj in queryset:
        new_obj = obj
        new_obj.creator = cur_modeler[0]
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = None
        new_obj.save()
        msg = (obj.__str__() + " was Created!", messages.SUCCESS)

        modeladmin.message_user(request, msg[0], msg[1])

copy_entry.short_description = _("Copy Entries")


def copy_dm(modeladmin, request, queryset):
    cur_modeler = Modeler.objects.filter(user=request.user)
    for obj in queryset:
        new_obj = obj
        new_obj.creator = cur_modeler[0]
        new_obj.pk = None
        new_obj.title = obj.title + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = str(uuid4())
        new_obj.identifier = 'dm-' + new_obj.ct_id
        new_obj.save()
        msg = (obj.__str__() + " was Created!", messages.SUCCESS)

        modeladmin.message_user(request, msg[0], msg[1])

copy_dm.short_description = _("Copy DM")


def generate_dm(modeladmin, request, queryset):

    if len(queryset) > 1:
        msg = (_("You may only generate one DM at a time. " +
                 str(len(queryset)) + " were selected."), messages.ERROR)
    elif queryset[0].published and request.user.is_superuser is False:
        msg = (_("This DM has been previously generated. Please make a copy and generate a new one."), messages.ERROR)
    else:
        new_id = str(uuid4())
        obj = queryset[0]
        obj.ct_id = new_id
        obj.identifier = 'dm-' + new_id
        obj.save()
        modeladmin.message_user(
            request, "Generating dm-" + new_id + " " + obj.title, messages.INFO)
        msg = generateDM(obj, request)
        # final msg from generator says success. create a standard success msg.
        if msg[1] == messages.SUCCESS:
            msg = (obj.__str__() + " with ID: " + obj.identifier +
                   " was Generated!", messages.SUCCESS)

    modeladmin.message_user(request, msg[0], msg[1])

generate_dm.short_description = _("Generate DM")


def copy_prj(modeladmin, request, queryset):
    for obj in queryset:
        new_obj = obj
        new_obj.pk = None
        new_obj.prj_name = (obj.prj_name + " (***COPY***)")
        new_obj.description = obj.description
        new_obj.rm_version = obj.rm_version
        new_obj.allowed_groups = obj.allowed_groups
        new_obj.save()
copy_prj.short_description = _("Copy Project(s)")


class DMAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    ordering = ['project', 'title']
    search_fields = ['title', 'ct_id']
    actions = [copy_dm, generate_dm, republishAll, delete_mcs, ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    filter_horizontal = ['contrib', 'pred_obj', ]

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('title', 'project', 'published')}),
        ("DM Entry", {'classes': ('wide',),
                      'fields': ('entry',),
                      'description': _('Select one Entry for this DM.')}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('pred_obj', 'asserts',),
                                     'description': _("")}),
        ("Metadata ", {'classes': ('wide',),
                       'fields': ('dc_language', 'about', 'description', 'author', 'contrib',
                                  'subject', 'source', 'rights', 'relation', 'coverage', 'publisher',),
                       'description': _("Enter the <a href='http://dublincore.org/'>Dublin Core</a> Metadata")}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'html_file', 'xml_file', 'xsd_file', 'json_file', 'sha1_file', 'zip_file',)}),
    )

    def get_form(self, request, obj=None, **kwargs):

        if request.user.is_superuser:
            kwargs['form'] = DMAdminSUForm
        else:
            kwargs['form'] = DMAdminForm

        form = super(DMAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project

        return form

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('title', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(DM, DMAdmin)


class EntryAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_entry, republish, delete_mcs, ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    filter_horizontal = ['links', 'participations', 'pred_obj', ]
    form = EntryAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(EntryAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'language'), 'encoding', 'data')}),
        ("Subject of the Entry ", {'classes': ('wide',),
                                   'fields': ('subject',),
                                   'description': _('Select Subject of the Entry.')}),
        ("Provider of the Entry ", {'classes': ('wide',),
                                    'fields': ('provider',),
                                    'description': _('Select Provider.')}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("HIGHLY Recommended: (but not required)", {'classes': ('collapse',),
                                                    'fields': ('links', 'audit', 'participations',
                                                               'protocol', 'workflow', 'state', 'attestation'),
                                                    'description': _('At least a generic item should be selected for each of these. This allows data to be entered at runtime.')}),
        ("Advanced", {'classes': ('collapse',), 'fields': ('asserts',)}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)

admin.site.register(Entry, EntryAdmin)


class XdBooleanAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator', ]
    search_fields = ['label', 'ct_id', ]
    ordering = ['project', 'label', ]
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs, ]
    readonly_fields = ['published', 'schema_code',
                       'r_code', 'creator', 'edited_by', ]
    form = XdBooleanAdminForm
    filter_horizontal = ['pred_obj', ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(XdBooleanAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang'), 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'trues', 'falses')}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("Advanced", {'classes': ('collapse',), 'fields': ('asserts',)}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code', 'r_code',)}),

    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(XdBoolean, XdBooleanAdmin)


class XdLinkAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs, ]
    readonly_fields = ['published', 'schema_code',
                       'r_code', 'creator', 'edited_by', ]
    form = XdLinkAdminForm
    filter_horizontal = ['pred_obj', ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(XdLinkAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang'), 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'relation',)}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("Advanced", {'classes': ('collapse',), 'fields': ('asserts',)}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code', 'r_code',)}),

    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(XdLink, XdLinkAdmin)


class XdStringAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs, ]
    readonly_fields = ['published', 'schema_code',
                       'r_code', 'creator', 'edited_by', ]
    filter_horizontal = ['pred_obj', ]
    form = XdStringAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(XdStringAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang'),)}),
        ("Optional", {'classes': ('collapse',),
                      'fields': ('min_length', 'max_length', 'exact_length', 'enums', 'definitions', 'def_val',)}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("Advanced", {'classes': ('collapse',), 'fields': ('asserts',)}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code', 'r_code',)}),

    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(XdString, XdStringAdmin)


class UnitsAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs, ]
    readonly_fields = ['published', 'schema_code',
                       'r_code', 'creator', 'edited_by', ]
    form = UnitsAdminForm
    filter_horizontal = ['pred_obj', ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(UnitsAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang'), 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'enums', 'definitions', 'def_val',)}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("Advanced", {'classes': ('collapse',), 'fields': ('asserts',)}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code', 'r_code',)}),

    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(Units, UnitsAdmin)


class XdCountAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs, ]
    readonly_fields = ['published', 'schema_code',
                       'r_code', 'creator', 'edited_by', ]
    filter_horizontal = ['reference_ranges', 'pred_obj', ]
    form = XdCountAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(XdCountAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang'),)}),
        ("Units", {'classes': ('wide',),
                   'fields': ('units',),
                   'description': _('<b>Mandatory:</b> Select a units.')}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("Optional", {'classes': ('collapse',),
                      'fields': ('normal_status', 'reference_ranges',
                                 'min_inclusive', 'max_inclusive', 'min_exclusive', 'max_exclusive', 'total_digits',)}),
        ("Advanced", {'classes': ('collapse',), 'fields': ('asserts',)}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code', 'r_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(XdCount, XdCountAdmin)


class XdIntervalAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs, ]
    readonly_fields = ['published', 'schema_code',
                       'r_code', 'creator', 'edited_by', ]
    form = XdIntervalAdminForm
    filter_horizontal = ['pred_obj', ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(XdIntervalAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang'), 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'interval_type', 'lower', 'upper',
                           'lower_included', 'upper_included',
                           'lower_bounded', 'upper_bounded',)}),
        ("Optional Units", {'classes': ('collapse',),
                            'fields': ('units_name', 'units_uri',)}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("Advanced", {'classes': ('collapse',), 'fields': ('asserts',)}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code', 'r_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(XdInterval, XdIntervalAdmin)


class XdFileAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs, ]
    readonly_fields = ['published', 'schema_code',
                       'r_code', 'creator', 'edited_by', ]
    form = XdFileAdminForm
    filter_horizontal = ['pred_obj', ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(XdFileAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang'), 'require_vtb', 'require_vte', 'require_tr', 'require_mod', )}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj', 'content_mode',)}),
        ("Optional", {'classes': ('collapse',),
                      'fields': ('language', 'media_type', 'encoding', 'alt_txt',)}),
        ("Advanced", {'classes': ('collapse',), 'fields': ('asserts',)}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code', 'r_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(XdFile, XdFileAdmin)


class XdOrdinalAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs, ]
    readonly_fields = ['published', 'schema_code',
                       'r_code', 'creator', 'edited_by', ]
    filter_horizontal = ['reference_ranges', 'pred_obj', ]
    form = XdOrdinalAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(XdOrdinalAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang'), 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'ordinals', 'symbols', 'annotations',)}),
        ("Optional", {'classes': ('collapse',),
                      'fields': ('normal_status', 'reference_ranges',)}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("Advanced", {'classes': ('collapse',), 'fields': ('asserts',)}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code', 'r_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(XdOrdinal, XdOrdinalAdmin)


class XdQuantityAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs, ]
    readonly_fields = ['published', 'schema_code',
                       'r_code', 'creator', 'edited_by', ]
    filter_horizontal = ['reference_ranges', 'pred_obj', ]
    form = XdQuantityAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(XdQuantityAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang'), 'require_vtb', 'require_vte', 'require_tr', 'require_mod', )}),
        ("Units", {'classes': ('wide',),
                   'fields': ('units',),
                   'description': _('<b>Mandatory:</b> Select a units.')}),
        ("Optional", {'classes': ('collapse',),
                      'fields': ('normal_status', 'reference_ranges',
                                 'min_inclusive', 'max_inclusive', 'min_exclusive', 'max_exclusive', 'total_digits', 'fraction_digits',)}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("Advanced", {'classes': ('collapse',), 'fields': ('asserts',)}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code', 'r_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(XdQuantity, XdQuantityAdmin)


class XdRatioAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs, ]
    readonly_fields = ['published', 'schema_code',
                       'r_code', 'creator', 'edited_by', ]
    filter_horizontal = ['reference_ranges', 'pred_obj', ]
    form = XdRatioAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(XdRatioAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang'), 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'ratio_type',)}),
        ("Numerator Units (Optional and CANNOT be the same PcT as the denominator or ratio.)", {'classes': ('collapse',),
                                                                                                'fields': ('num_units',),
                                                                                                'description': _('Select a units.')}),
        ("Denominator Units (Optional and CANNOT be the same PcT as the numerator or ratio.)", {'classes': ('collapse',),
                                                                                                'fields': ('den_units',),
                                                                                                'description': _('Select a units.')}),
        ("Ratio Units (Optional and CANNOT be the same PcT as the numerator or denominator.)", {'classes': ('collapse',),
                                                                                                'fields': ('ratio_units',),
                                                                                                'description': _('Select a units.')}),
        ("Optional Constraints", {'classes': ('collapse',),
                                  'fields': ('num_min_inclusive', 'num_max_inclusive', 'num_min_exclusive',
                                             'num_max_exclusive', 'den_min_inclusive', 'den_max_inclusive',
                                             'den_min_exclusive', 'den_max_exclusive', 'normal_status',
                                             'reference_ranges', 'min_magnitude', 'max_magnitude',)}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("Advanced", {'classes': ('collapse',), 'fields': ('asserts',)}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code', 'r_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(XdRatio, XdRatioAdmin)


class XdTemporalAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs, ]
    readonly_fields = ['published', 'schema_code',
                       'r_code', 'creator', 'edited_by', ]
    filter_horizontal = ['reference_ranges', 'pred_obj', ]
    form = XdTemporalAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(XdTemporalAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang'), 'require_vtb', 'require_vte', 'require_tr', 'require_mod', )}),
        ("Allow Only One Duration Type", {'classes': ('wide',),
                                          'fields': ('allow_duration', 'allow_ymduration', 'allow_dtduration',)}),
        ("Allow Any Combination of these:", {'classes': ('wide',),
                                             'fields': ('allow_date', 'allow_time', 'allow_datetime', 'allow_datetimestamp', 'allow_day', 'allow_month',
                                                        'allow_year', 'allow_year_month', 'allow_month_day',)}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("Optional", {'classes': ('collapse',),
                      'fields': ('normal_status', 'reference_ranges',)}),
        ("Advanced", {'classes': ('collapse',), 'fields': ('asserts',)}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code', 'r_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(XdTemporal, XdTemporalAdmin)


class ClusterAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_cluster, delete_mcs, ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    filter_horizontal = ['xdboolean', 'xdlink', 'xdstring', 'clusters', 'xdfile',
                         'xdordinal', 'xdtemporal', 'xdcount', 'xdquantity', 'xdratio', 'pred_obj', ]
    form = ClusterAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(ClusterAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project'), 'description', 'pred_obj',)}),
        ("Contents", {'classes': ('wide',),
                      'fields': ('clusters',),
                      'description': _('Select all Clusters that you wish to include in this Cluster.'), }),
        ("Non-Quantitative", {'classes': ('wide',),
                              'fields': ('xdboolean', 'xdlink', 'xdstring', 'xdfile', 'xdordinal', 'xdtemporal',),
                              'description': _('Select one or more non-quantitative datatype(s) for this Cluster.')}),
        ("Quantitative", {'classes': ('wide',),
                          'fields': ('xdcount', 'xdquantity', 'xdratio',),
                          'description': _('Select one or more quantitative datatype(s) for this Cluster.')}),

        ("Advanced", {'classes': ('collapse',), 'fields': ('asserts',)}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(Cluster, ClusterAdmin)


class PartyAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish,
               copy_labeled, republish, delete_mcs, ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    filter_horizontal = ['external_ref', 'pred_obj', ]
    form = PartyAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(PartyAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang'), 'details', 'external_ref',)}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("Advanced", {'classes': ('collapse',), 'fields': ('asserts',)}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(Party, PartyAdmin)


class ReferenceRangeAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs, ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    form = ReferenceRangeAdminForm
    filter_horizontal = ['pred_obj', ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(ReferenceRangeAdmin, self).get_form(
            request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang'), 'definition',
                           'interval', 'is_normal',)}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("Advanced", {'classes': ('collapse',), 'fields': ('asserts',)}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(ReferenceRange, ReferenceRangeAdmin)


class SimpleRRAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs, ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    form = SimpleRRAdminForm
    filter_horizontal = ['pred_obj', ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(SimpleRRAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        form.prj_filter = modeller.prj_filter

        return form

    fieldsets = (
        (None, {'classes': ('wide', ),
                'fields': ('published', ('label', 'project', 'lang'), 'definition', 'is_normal', 'interval_type',
                           'lower', 'upper', 'lower_included', 'upper_included', 'lower_bounded',
                           'upper_bounded', )}),

        ("Optional Units", {'classes': ('collapse', ),
                            'fields': ('units_name', 'units_uri', )}),

        ("Additional Information ", {'classes': ('wide', ),
                                     'fields': ('description', 'pred_obj', )}),
        ("Advanced", {'classes': ('collapse', ), 'fields': ('asserts', )}),
        ("Read Only", {'classes': ('collapse', ),
                       'fields': ('creator', 'edited_by', 'schema_code', )}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator', )
admin.site.register(SimpleReferenceRange, SimpleRRAdmin)


class AuditAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish,
               copy_labeled, republish, delete_mcs, ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    form = AuditAdminForm
    filter_horizontal = ['pred_obj', ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(AuditAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', 'project', 'label', 'lang',)}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        (None, {'classes': ('wide',),
                'fields': ('system_id', 'system_user', 'location',)}),
        ("Advanced", {'classes': ('collapse',), 'fields': ('asserts',)}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(Audit, AuditAdmin)


class AttestationAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish,
               copy_labeled, republish, delete_mcs, ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    form = AttestationAdminForm
    filter_horizontal = ['pred_obj', ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(AttestationAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang'), 'view', 'reason', 'proof', 'committer',)}),
        ("Additional Information", {'classes': ('wide',),
                                    'fields': ('description', 'pred_obj',)}),
        ("Advanced", {'classes': ('collapse',), 'fields': ('asserts',)}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(Attestation, AttestationAdmin)


class ParticipationAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish,
               copy_labeled, republish, delete_mcs, ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    form = ParticipationAdminForm
    filter_horizontal = ['pred_obj', ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(ParticipationAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang'), 'performer', 'function', 'mode',)}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("Advanced", {'classes': ('collapse',), 'fields': ('asserts',)}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(Participation, ParticipationAdmin)


class ProjectAdmin(admin.ModelAdmin):
    actions = ['delete_selected', ]
    list_display = ('prj_name', 'description',)
admin.site.register(Project, ProjectAdmin)


class NSAdmin(admin.ModelAdmin):
    actions = ['delete_selected', ]
    list_display = ('abbrev', 'uri',)
admin.site.register(NS, NSAdmin)


class PredicateAdmin(admin.ModelAdmin):
    actions = ['delete_selected', ]
    list_display = ('ns_abbrev', 'class_name',)
admin.site.register(Predicate, PredicateAdmin)


class PredObjAdmin(admin.ModelAdmin):
    actions = ['delete_selected', ]
    ordering = ['project', 'object_uri']
    list_filter = ['project', ]
    list_display = ('project', 'predicate', 'object_uri',)
admin.site.register(PredObj, PredObjAdmin)


class ModelerAdmin(admin.ModelAdmin):
    actions = ['delete_selected', ]
    list_display = ('name', 'email', 'user', 'project',)
admin.site.register(Modeler, ModelerAdmin)
