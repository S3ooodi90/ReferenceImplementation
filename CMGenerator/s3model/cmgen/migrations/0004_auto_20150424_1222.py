# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmgen', '0003_auto_20150423_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='dvstring',
            name='is_units_def',
            field=models.BooleanField(help_text='Is this PcT for defining units for other PcTs?', verbose_name='Units Def?', default=False),
        ),
        migrations.AlterField(
            model_name='audit',
            name='system_id',
            field=models.ForeignKey(null=True, verbose_name='system id', help_text='A model for an Identifier of the system which handled the information item.', to='cmgen.DvString'),
        ),
        migrations.AlterField(
            model_name='dvinterval',
            name='lower',
            field=models.CharField(null=True, verbose_name='Lower Value', max_length=110, help_text='Enter the lower value of the interval. This will be used to set the minInclusive facet.', blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='dvinterval',
            name='lower_bounded',
            field=models.BooleanField(help_text='Uncheck this box if the lower value is unbounded.', verbose_name='Lower Bounded?', default=True),
        ),
        migrations.AlterField(
            model_name='dvinterval',
            name='upper',
            field=models.CharField(null=True, verbose_name='Upper Value', max_length=110, help_text='Enter the upper value of the interval. This will be used to set the maxInclusive facet.', blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='dvinterval',
            name='upper_bounded',
            field=models.BooleanField(help_text='Uncheck this box if the lower value is unbounded.', verbose_name='Upper Bounded?', default=True),
        ),
        migrations.AlterField(
            model_name='dvmedia',
            name='content',
            field=models.CharField(choices=[(None, 'Default is allow user choice'), ('user', 'User Choice'), ('url', 'Via URL'), ('embed', 'Embedded in data')], help_text="Select the location of the data. Allow the end user to choose or restrict to 'via a URL' or 'embedded' in the data instance.", verbose_name='Media Content', max_length=20, default='user'),
        ),
        migrations.AlterField(
            model_name='dvmedia',
            name='media_type',
            field=models.TextField(help_text="The allowed Media Types of the included data, one per line; i.e. application/rdf+xml, image/jpeg, video/mp4. See <a href='http://www.iana.org/assignments/media-types/media-types.xhtml'>IANA Listing</a>.", verbose_name='Media Type', blank=True),
        ),
        migrations.AlterField(
            model_name='dvordinal',
            name='symbols_def',
            field=models.TextField(help_text='Enter a URI for each symbol. One per line. These are used as rdf:isDefinedBy in the semantics. If the same URI is to be used for all symbols then enter it on the first line only.', verbose_name='symbols definition'),
        ),
        migrations.AlterField(
            model_name='dvstring',
            name='lang_required',
            field=models.BooleanField(help_text='Require a language element in instance data?', verbose_name='Language Required?', default=False),
        ),
        migrations.AlterField(
            model_name='dvstring',
            name='pattern',
            field=models.CharField(help_text="Enter a REGEX pattern to constrain string if desired. See <a href='http://www.regular-expressions.info/xml.html'>options</a>", verbose_name='Pattern', max_length=255, blank=True),
        ),
    ]
