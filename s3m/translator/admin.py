import os
import csv

from time import time
from django.contrib import messages
from s3m.settings import MEDIA_ROOT

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.shortcuts import get_object_or_404

from dmgen.models import XdString, XdCount, XdQuantity, XdTemporal, Cluster, Entry, DM, PredObj, Predicate, Party, Units
from dmgen.generator import generateDM
from dmgen.admin import generate_dm

from .models import DMD, Record
from .datagen import dataGen

def make_records(modeladmin, request, queryset):
    """
    Add the headers to the Record table for editing.
    """
    for obj in queryset:
        msg = (obj.__str__() + " Is being processed.", messages.SUCCESS)

        with open(os.path.join(MEDIA_ROOT, obj.csv_file.url)) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=obj.delim)
            for hdr in reader.fieldnames:
                hdr = hdr.strip()

                rec = Record(dmd=obj, header=hdr, label=hdr,dt_type='xdstring', description='Created by the Data Insights, Inc. Data Translator.')
                rec.save()

        modeladmin.message_user(request, msg[0], msg[1])
make_records.short_description = _("Process CSV")


def dmgen(modeladmin, request, queryset):
    """
    Generate a complete Data Model for this DMD.
    """
    columns = []

    for obj in queryset:
        with open(os.path.join(MEDIA_ROOT, obj.csv_file.url)) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=obj.delim)
            for hdr in reader.fieldnames:
                columns.append(hdr.strip())

        msg = (obj.__str__() + " Is being processed.", messages.SUCCESS)

        pred = get_object_or_404(Predicate, id=1)

        dmd_po, x = PredObj.objects.get_or_create(po_name='Definition for ' + obj.title, predicate=pred, object_uri=obj.definitions.splitlines()[0], project=obj.project)
        newsub = False
        subject, newsub = Party.objects.get_or_create(project=obj.project, label=obj.title + ' - Entry Subject', lang=obj.lang, description=obj.description)
        if newsub:
            subject.pred_obj.add(dmd_po)
            subject.save()
            subject.publish(request)

        newprv = False
        provider, newprv = Party.objects.get_or_create(project=obj.project, label=obj.title + ' - Entry Provider', lang=obj.lang, description=obj.description)
        if newprv:
            provider.pred_obj.add(dmd_po)
            provider.save()
            provider.publish(request)

        cluster, x = Cluster.objects.get_or_create(project=obj.project, label=obj.title + ' - Cluster', lang=obj.lang, description=obj.description)
        if x:
            cluster.pred_obj.add(dmd_po)
            cluster.save()
        entry, x = Entry.objects.get_or_create(project=obj.project, label=obj.title + ' - Entry', lang=obj.lang, language=obj.lang, description=obj.description, subject=subject, provider=provider, data=cluster)
        if x:
            entry.pred_obj.add(dmd_po)
            entry.save()
        dm = DM.objects.create(project=obj.project, title=obj.title, dc_language=obj.lang, description=obj.description, author=obj.author,  creator=obj.author, edited_by=obj.author, entry=entry)
        dm.pred_obj.add(dmd_po)
        dm.save()
        lang = obj.lang
        recs = Record.objects.filter(dmd=obj)
        for col in columns:
            mc = None
            new = False
            rec = recs.get(header=col)
            if rec.dt_type == 'xdstring':
                mc = XdString.objects.create(project=dm.project, label=rec.label, lang=lang, description=rec.description, min_length=rec.min_length, max_length=rec.max_length, exact_length=rec.exact_length, enums=rec.enums, def_val=rec.def_val )

                defs = rec.definitions.splitlines()
                if len(defs) <= 0:
                    mc.pred_obj.add(dmd_po)
                else:
                    for d in defs:
                        rdf = PredObj.objects.create(po_name='Definition for ' + mc.label, predicate=pred, object_uri=d, project=obj.project)
                        mc.pred_obj.add(rdf)
                        mc.save()

                msg = mc.publish(request)
                cluster.xdstring.add(mc)
                cluster.save()

            elif rec.dt_type == 'xdcount':
                u, new = Units.objects.get_or_create(project=dm.project, label=rec.units_name, lang=lang, description='Units for ' + rec.label + '. ' + rec.description, enums=rec.units_name, definitions=rec.units_uri)
                if new:
                    rdf = PredObj.objects.create(po_name='Definition for ' + u.label, predicate=pred, object_uri=rec.units_uri, project=dm.project)
                    u.pred_obj.add(rdf)
                    u.save()
                if u.published is False:
                    u.publish(request)
                mc = XdCount.objects.create(project=dm.project, label=rec.label, lang=lang, description=rec.description, min_inclusive=rec.min_inclusive, max_inclusive=rec.max_inclusive, min_exclusive=rec.min_exclusive, max_exclusive=rec.max_exclusive, total_digits=rec.total_digits, units=u)

                defs = rec.definitions.splitlines()
                if len(defs) <= 0:
                    mc.pred_obj.add(dmd_po)
                else:
                    for d in defs:
                        rdf = PredObj.objects.create(po_name='Definition for ' + mc.label, predicate=pred, object_uri=d, project=obj.project)
                        mc.pred_obj.add(rdf)
                        mc.save()

                msg = mc.publish(request)
                cluster.xdcount.add(mc)
                cluster.save()

            elif rec.dt_type == 'xdquantity':
                u, new = Units.objects.get_or_create(project=dm.project, label=rec.units_name, lang=lang, description='Units for ' + rec.label + '. ' + rec.description, enums=rec.units_name, definitions=rec.units_uri)
                if new:
                    rdf = PredObj.objects.create(po_name='Definition for ' + u.label, predicate=pred, object_uri=rec.units_uri, project=dm.project)
                    u.pred_obj.add(rdf)
                    u.save()
                if u.published is False:
                    u.publish(request)

                mc = XdQuantity.objects.create(project=dm.project, label=rec.label, lang=lang, description=rec.description, min_inclusive=rec.min_inclusive, max_inclusive=rec.max_inclusive, min_exclusive=rec.min_exclusive, max_exclusive=rec.max_exclusive, total_digits=rec.total_digits, units=u)

                defs = rec.definitions.splitlines()
                if len(defs) <= 0:
                    mc.pred_obj.add(dmd_po)
                else:
                    for d in defs:
                        rdf = PredObj.objects.create(po_name='Definition for ' + mc.label, predicate=pred, object_uri=d, project=obj.project)
                        mc.pred_obj.add(rdf)
                        mc.save()

                msg = mc.publish(request)
                cluster.xdquantity.add(mc)
                cluster.save()

            elif rec.dt_type == 'xdtemporal':
                mc = XdTemporal.objects.create(project=dm.project, label=rec.label, lang=lang, description=rec.description, allow_duration=rec.allow_duration, allow_ymduration=rec.allow_ymduration, allow_dtduration=rec.allow_dtduration, allow_date=rec.allow_date, allow_time=rec.allow_time, allow_datetime=rec.allow_datetime, allow_datetimestamp=rec.allow_datetimestamp, allow_day=rec.allow_day, allow_month=rec.allow_month, allow_year=rec.allow_year, allow_year_month=rec.allow_year_month, allow_month_day=rec.allow_month_day)

                defs = rec.definitions.splitlines()
                if len(defs) <= 0:
                    mc.pred_obj.add(dmd_po)
                else:
                    for d in defs:
                        rdf = PredObj.objects.create(po_name='Definition for ' + mc.label, predicate=pred, object_uri=d, project=obj.project)
                        mc.pred_obj.add(rdf)
                        mc.save()

                msg = mc.publish(request)
                cluster.xdtemporal.add(mc)
                cluster.save()

            else:
                modeladmin.message_user(request, "Something broke while finding your datatype!", messages.ERROR)

        msg = cluster.publish(request)
        msg = entry.publish(request)

        # need to send a queryset to the call to generate_dm from the dmgen admin
        qs = DM.objects.filter(ct_id=dm.ct_id)
        generate_dm(modeladmin, request, qs)

        if obj.data_gen:
            modeladmin.message_user(request, "Generating data files..........", messages.SUCCESS)
            dataGen(obj, dm)

        modeladmin.message_user(request, msg[0], msg[1])
dmgen.short_description = _("Generate a Data Model")


class DMDAdmin(admin.ModelAdmin):
    list_filter = ['project', 'author']
    actions = ['delete_selected', make_records, dmgen,]
    list_display = ('title', 'project',)

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': (('title', 'project'),)}),
        (None, {'classes': ('wide',),
                                     'fields': ('description','definitions','delim','lang','author', 'contrib', 'data_gen', 'csv_file',)}),
    )

admin.site.register(DMD, DMDAdmin)

class RecordAdmin(admin.ModelAdmin):
    list_filter = ['dmd', 'dt_type']
    actions = ['delete_selected', ]
    readonly_fields = ['header', 'dmd',]
    list_display = ('header','dt_type','dmd', )

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': (('dmd', 'header'),)}),
        ("General", {'classes': ('wide',),
                                     'fields': ('label','description','dt_type','definitions',)}),
        ("Text", {'classes': ('collapse',),
                'fields': ('min_length', 'max_length', 'exact_length','enums','def_val',)}),
        ("Numbers", {'classes': ('collapse',),
                'fields': ('min_inclusive', 'max_inclusive', 'min_exclusive', 'max_exclusive','total_digits', 'units_name', 'units_uri', )}),
        ("Date/Time", {'classes': ('collapse',),
                'fields': (('allow_date', 'allow_time', 'allow_datetime', 'allow_datetimestamp', 'allow_day', 'allow_month',
                                                        'allow_year'),('allow_year_month', 'allow_month_day','allow_duration', 'allow_ymduration', 'allow_dtduration'),),'description': _('Select the specific temporal type in this column. ONE and ONLY ONE!')}),
    )
admin.site.register(Record, RecordAdmin)
