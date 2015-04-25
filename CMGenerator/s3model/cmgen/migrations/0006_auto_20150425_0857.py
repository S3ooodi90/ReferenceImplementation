# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmgen', '0005_auto_20150424_1344'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='units',
            options={'verbose_name': 'Units', 'ordering': ['prj_name', 'data_name'], 'verbose_name_plural': 'Units'},
        ),
        migrations.AddField(
            model_name='concept',
            name='ns_defs',
            field=models.TextField(verbose_name='encoding', default='\n  xmlns:xs="http://www.w3.org/2001/XMLSchema"\n  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n  xmlns:owl="http://www.w3.org/2002/07/owl#"\n  xmlns:dcterms="http://purl.org/dc/terms/"\n  xmlns:foaf="http://xmlns.com/foaf/0.1/" xmlns:sawsdl="http://www.w3.org/ns/sawsdl"\n  xmlns:sawsdlrdf="http://www.w3.org/ns/sawsdl#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"\n  xmlns:vc="http://www.w3.org/2007/XMLSchema-versioning" xmlns:s3m="http://www.s3model.com/"\n  targetNamespace="http://www.s3model.com/" vc:minVersion="1.1"\n    ', help_text='Define additional namespace abbreviations here, one per line. Do not edit or remove the existing definitions'),
        ),
        migrations.AlterField(
            model_name='units',
            name='enums',
            field=models.TextField(verbose_name='abbreviations', help_text='Enter the abbreviations for the units, one per line.'),
        ),
        migrations.AlterField(
            model_name='units',
            name='enums_def',
            field=models.TextField(verbose_name='abbreviation definitions', help_text='Enter a URI for each unit. One per line. These are used as rdf:isDefinedBy in the semantics. If the same URI is to be used for all enumeration then enter it on the first line only.'),
        ),
    ]
