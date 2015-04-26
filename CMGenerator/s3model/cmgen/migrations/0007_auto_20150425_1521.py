# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmgen', '0006_auto_20150425_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concept',
            name='ns_defs',
            field=models.TextField(default='  xmlns:xs="http://www.w3.org/2001/XMLSchema"\n  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n  xmlns:owl="http://www.w3.org/2002/07/owl#"\n  xmlns:dcterms="http://purl.org/dc/terms/"\n  xmlns:foaf="http://xmlns.com/foaf/0.1/"\n  xmlns:sawsdl="http://www.w3.org/ns/sawsdl"\n  xmlns:sawsdlrdf="http://www.w3.org/ns/sawsdl#"\n  xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"\n  xmlns:vc="http://www.w3.org/2007/XMLSchema-versioning"\n  xmlns:s3m="http://www.s3model.com/"\n  targetNamespace="http://www.s3model.com/" vc:minVersion="1.1"\n  ', verbose_name='Namespace definitions', help_text='Define additional namespace abbreviations here, one per line. Do not edit or remove the existing definitions'),
        ),
        migrations.RemoveField(
            model_name='referencerange',
            name='data_range',
        ),
        migrations.AddField(
            model_name='referencerange',
            name='data_range',
            field=models.ManyToManyField(help_text='The data range for this meaning. Select the appropriate DvInterval.', to='cmgen.DvInterval', verbose_name='data range'),
        ),
        migrations.AlterField(
            model_name='units',
            name='enums',
            field=models.TextField(help_text='Enter the names for the units, one per line.', verbose_name='Unit names'),
        ),
        migrations.AlterField(
            model_name='units',
            name='enums_def',
            field=models.TextField(help_text='Enter a URI for each unit. One per line. These are used as rdf:isDefinedBy in the semantics. If the same URI is to be used for all names then enter it on the first line only.', verbose_name='Unit links'),
        ),
    ]
