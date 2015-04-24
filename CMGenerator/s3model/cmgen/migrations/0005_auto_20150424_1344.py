# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cmgen', '0004_auto_20150424_1222'),
    ]

    operations = [
        migrations.CreateModel(
            name='Units',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('ct_id', django_extensions.db.fields.UUIDField(help_text='A unique identifier for this PCT.', editable=False, blank=True, verbose_name='UUID')),
                ('created', models.DateTimeField(help_text='The dateTime that the PCT was created.', auto_now_add=True, verbose_name='created')),
                ('last_updated', models.DateTimeField(help_text='Last update.', auto_now=True, verbose_name='last updated')),
                ('published', models.BooleanField(help_text='Published must be a green check icon in order to use this in a CM. This is not user editable. It is managed by the publication process.', default=False, verbose_name='published')),
                ('description', models.TextField(help_text='Enter a free text description for this complexType. Include a usage statement and any possible misuses. This is used as the annotation for the PcT.', null=True, verbose_name='description')),
                ('schema_code', models.TextField(help_text='This is only writable from the CMGEN, not via user input. It contains the code required for each component to create an entry in a CM.', null=True, default='', blank=True, verbose_name='Schema Code')),
                ('asserts', models.TextField(help_text='Valid XPath 2.0 assert statements. See the documentation for details. One per line.', null=True, default='', blank=True, verbose_name='asserts')),
                ('lang', models.CharField(help_text='Choose the language of this PcT.', default='en-US', choices=[('en-US', 'US English'), ('pt-BR', 'Brazilian Portuguese'), ('af', 'Afrikaans'), ('ar', 'Arabic'), ('ast', 'Asturian'), ('az', 'Azerbaijani'), ('bg', 'Bulgarian'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('br', 'Breton'), ('bs', 'Bosnian'), ('ca', 'Catalan'), ('cs', 'Czech'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('el', 'Greek'), ('en', 'English'), ('en-au', 'Australian English'), ('en-gb', 'British English'), ('eo', 'Esperanto'), ('es', 'Spanish'), ('es-ar', 'Argentinian Spanish'), ('es-mx', 'Mexican Spanish'), ('es-ni', 'Nicaraguan Spanish'), ('es-ve', 'Venezuelan Spanish'), ('et', 'Estonian'), ('eu', 'Basque'), ('fa', 'Persian'), ('fi', 'Finnish'), ('fr', 'French'), ('fy', 'Frisian'), ('ga', 'Irish'), ('gl', 'Galician'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('hr', 'Croatian'), ('hu', 'Hungarian'), ('ia', 'Interlingua'), ('id', 'Indonesian'), ('io', 'Ido'), ('is', 'Icelandic'), ('it', 'Italian'), ('ja', 'Japanese'), ('ka', 'Georgian'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('kn', 'Kannada'), ('ko', 'Korean'), ('lb', 'Luxembourgish'), ('lt', 'Lithuanian'), ('lv', 'Latvian'), ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('mr', 'Marathi'), ('my', 'Burmese'), ('nb', 'Norwegian Bokmal'), ('ne', 'Nepali'), ('nl', 'Dutch'), ('nn', 'Norwegian Nynorsk'), ('os', 'Ossetic'), ('pa', 'Punjabi'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('pt-br', 'Brazilian Portuguese'), ('ro', 'Romanian'), ('ru', 'Russian'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('sq', 'Albanian'), ('sr', 'Serbian'), ('sr-latn', 'Serbian Latin'), ('sv', 'Swedish'), ('sw', 'Swahili'), ('ta', 'Tamil'), ('te', 'Telugu'), ('th', 'Thai'), ('tr', 'Turkish'), ('tt', 'Tatar'), ('udm', 'Udmurt'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('vi', 'Vietnamese'), ('zh-cn', 'Simplified Chinese'), ('zh-hans', 'Simplified Chinese'), ('zh-hant', 'Traditional Chinese'), ('zh-tw', 'Traditional Chinese')], max_length=40, verbose_name='language')),
                ('r_code', models.TextField(help_text='This is only writable from the CMGEN, not via user input. It contains the code required for each component to create a function for the R data analysis.', null=True, default='', blank=True, verbose_name='R Code')),
                ('xqr_code', models.TextField(help_text='This is only writable from the CMGEN, not via user input. It contains the code required to create a XQuery to read the PcT.', null=True, default='', blank=True, verbose_name='XQuery Read')),
                ('xqw_code', models.TextField(help_text='This is only writable from the CMGEN, not via user input. It contains the code required to create a XQuery to write the PcT.', null=True, default='', blank=True, verbose_name='XQuery Write')),
                ('data_name', models.CharField(help_text='Type a name for this ComplexType.', db_index=True, max_length=110, verbose_name='data name')),
                ('adapter_id', django_extensions.db.fields.UUIDField(help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific DvAdapter complexType.', editable=False, blank=True, verbose_name='Element UUID')),
                ('vtb_required', models.BooleanField(help_text='Require a Valid begin time?', default=False, verbose_name='VTB Required?')),
                ('vte_required', models.BooleanField(help_text='Require a Valid end time?', default=False, verbose_name='VTE Required?')),
                ('min_length', models.IntegerField(help_text='Enter the minimum number of characters that are required for this concept. If the character is optional, leave it blank.', null=True, blank=True, verbose_name='minimum length')),
                ('max_length', models.IntegerField(help_text='Enter the maximum number of characters that are required for this concept. If the character is optional, leave it blank.', null=True, blank=True, verbose_name='maximum length')),
                ('exact_length', models.IntegerField(help_text='Enter the exact length of the concept. It should be defined only when the number of characters is always fixed (e.g. codes and identifiers).', null=True, blank=True, verbose_name='exact length')),
                ('default_value', models.CharField(help_text='Enter a default value for the string if desired.', max_length=255, blank=True, verbose_name='default value')),
                ('enums', models.TextField(help_text='Enter the categories values of the concept (e.g.Male,Female). One per line.', blank=True, verbose_name='enumerations')),
                ('enums_def', models.TextField(help_text='Enter a URI for each enumeration. One per line. These are used as rdf:isDefinedBy in the semantics. If the same URI is to be used for all enumeration then enter it on the first line only.', blank=True, verbose_name='enumerations definition')),
                ('pattern', models.CharField(help_text="Enter a REGEX pattern to constrain string if desired. See <a href='http://www.regular-expressions.info/xml.html'>options</a>", max_length=255, blank=True, verbose_name='Pattern')),
                ('whitespace', models.CharField(help_text="Whitespace handling. See <a href=''>here</a>.", default='preserve', choices=[(None, 'Default is to preserve whitespace.'), ('preserve', 'Preserve'), ('replace', 'Replace'), ('collapse', 'Collapse')], max_length=8, verbose_name='Whitespace')),
                ('lang_required', models.BooleanField(help_text='Require a language element in instance data?', default=False, verbose_name='Language Required?')),
                ('prj_name', models.ForeignKey(help_text='Choose the name of your Project.', to='cmgen.Project', verbose_name='Project Name')),
                ('semantics', models.ManyToManyField(help_text='Select one or more Predicate/Object combinations for the semantics. You must select at least one.', to='cmgen.PredObj', verbose_name='semantics')),
            ],
            options={
                'verbose_name': 'DvString',
                'ordering': ['prj_name', 'data_name'],
                'verbose_name_plural': 'DvStrings',
            },
        ),
        migrations.RemoveField(
            model_name='dvstring',
            name='is_units_def',
        ),
        migrations.AlterField(
            model_name='dvcount',
            name='units',
            field=models.ForeignKey(help_text='Choose a DvString for the allowed units of measurement of this concept.', blank=True, null=True, to='cmgen.Units', verbose_name='units'),
        ),
        migrations.AlterField(
            model_name='dvquantity',
            name='units',
            field=models.ForeignKey(help_text='Choose a DvString for the allowed units of measurement of this concept.', blank=True, null=True, to='cmgen.Units', verbose_name='units'),
        ),
        migrations.AlterField(
            model_name='dvratio',
            name='den_units',
            field=models.ForeignKey(help_text='Choose a DvString for the units of measurement of the denominator.', blank=True, null=True, related_name='den_units', to='cmgen.Units', verbose_name='denominator units'),
        ),
        migrations.AlterField(
            model_name='dvratio',
            name='num_units',
            field=models.ForeignKey(help_text='Choose a DvString for the units of measurement of the numerator.', blank=True, null=True, related_name='num_units', to='cmgen.Units', verbose_name='numerator units'),
        ),
        migrations.AlterField(
            model_name='dvratio',
            name='ratio_units',
            field=models.ForeignKey(help_text='Choose a DvString for the units of measurement of the ratio (magnitude).', blank=True, null=True, related_name='ratio_units', to='cmgen.Units', verbose_name='ratio units'),
        ),
    ]
