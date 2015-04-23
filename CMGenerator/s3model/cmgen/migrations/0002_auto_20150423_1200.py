# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmgen', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='predicate',
            options={'ordering': ['pred_def'], 'verbose_name_plural': 'Predicates', 'verbose_name': 'Predicate'},
        ),
        migrations.AlterModelOptions(
            name='predobj',
            options={'ordering': ['name', 'pred'], 'verbose_name_plural': 'Predicate/Object', 'verbose_name': 'Predicate/Object'},
        ),
        migrations.AddField(
            model_name='predobj',
            name='prj_name',
            field=models.ForeignKey(to='cmgen.Project', help_text='Choose the name of your Project.', default=1, verbose_name='Project Name'),
        ),
        migrations.AlterField(
            model_name='attestation',
            name='published',
            field=models.BooleanField(help_text='Published must be a green check icon in order to use this in a CM. This is not user editable. It is managed by the publication process.', verbose_name='published', default=False),
        ),
        migrations.AlterField(
            model_name='audit',
            name='published',
            field=models.BooleanField(help_text='Published must be a green check icon in order to use this in a CM. This is not user editable. It is managed by the publication process.', verbose_name='published', default=False),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='published',
            field=models.BooleanField(help_text='Published must be a green check icon in order to use this in a CM. This is not user editable. It is managed by the publication process.', verbose_name='published', default=False),
        ),
        migrations.AlterField(
            model_name='concept',
            name='published',
            field=models.BooleanField(help_text='Published must be a green check icon in order to use this in a CM. This is not user editable. It is managed by the publication process.', verbose_name='published', default=False),
        ),
        migrations.AlterField(
            model_name='dvboolean',
            name='false_values',
            field=models.TextField(help_text="Enter the set of values that are Boolean FALSEs. For instance, if this is a 'Yes/No' type of concept, usually the 'No' is a Boolean FALSE. Enter one per line without blank lines.", verbose_name='false options'),
        ),
        migrations.AlterField(
            model_name='dvboolean',
            name='published',
            field=models.BooleanField(help_text='Published must be a green check icon in order to use this in a CM. This is not user editable. It is managed by the publication process.', verbose_name='published', default=False),
        ),
        migrations.AlterField(
            model_name='dvboolean',
            name='true_values',
            field=models.TextField(help_text="Enter the set of values that are Boolean TRUEs. For instance, if this is a 'Yes/No' type of concept, usually the 'Yes' is a Boolean TRUE. Enter one per line without blank lines.", verbose_name='true options'),
        ),
        migrations.AlterField(
            model_name='dvcount',
            name='published',
            field=models.BooleanField(help_text='Published must be a green check icon in order to use this in a CM. This is not user editable. It is managed by the publication process.', verbose_name='published', default=False),
        ),
        migrations.AlterField(
            model_name='dvinterval',
            name='published',
            field=models.BooleanField(help_text='Published must be a green check icon in order to use this in a CM. This is not user editable. It is managed by the publication process.', verbose_name='published', default=False),
        ),
        migrations.AlterField(
            model_name='dvlink',
            name='published',
            field=models.BooleanField(help_text='Published must be a green check icon in order to use this in a CM. This is not user editable. It is managed by the publication process.', verbose_name='published', default=False),
        ),
        migrations.AlterField(
            model_name='dvmedia',
            name='published',
            field=models.BooleanField(help_text='Published must be a green check icon in order to use this in a CM. This is not user editable. It is managed by the publication process.', verbose_name='published', default=False),
        ),
        migrations.AlterField(
            model_name='dvordinal',
            name='published',
            field=models.BooleanField(help_text='Published must be a green check icon in order to use this in a CM. This is not user editable. It is managed by the publication process.', verbose_name='published', default=False),
        ),
        migrations.AlterField(
            model_name='dvparsable',
            name='published',
            field=models.BooleanField(help_text='Published must be a green check icon in order to use this in a CM. This is not user editable. It is managed by the publication process.', verbose_name='published', default=False),
        ),
        migrations.AlterField(
            model_name='dvquantity',
            name='published',
            field=models.BooleanField(help_text='Published must be a green check icon in order to use this in a CM. This is not user editable. It is managed by the publication process.', verbose_name='published', default=False),
        ),
        migrations.AlterField(
            model_name='dvratio',
            name='published',
            field=models.BooleanField(help_text='Published must be a green check icon in order to use this in a CM. This is not user editable. It is managed by the publication process.', verbose_name='published', default=False),
        ),
        migrations.AlterField(
            model_name='dvstring',
            name='published',
            field=models.BooleanField(help_text='Published must be a green check icon in order to use this in a CM. This is not user editable. It is managed by the publication process.', verbose_name='published', default=False),
        ),
        migrations.AlterField(
            model_name='dvtemporal',
            name='published',
            field=models.BooleanField(help_text='Published must be a green check icon in order to use this in a CM. This is not user editable. It is managed by the publication process.', verbose_name='published', default=False),
        ),
        migrations.AlterField(
            model_name='participation',
            name='published',
            field=models.BooleanField(help_text='Published must be a green check icon in order to use this in a CM. This is not user editable. It is managed by the publication process.', verbose_name='published', default=False),
        ),
        migrations.AlterField(
            model_name='party',
            name='published',
            field=models.BooleanField(help_text='Published must be a green check icon in order to use this in a CM. This is not user editable. It is managed by the publication process.', verbose_name='published', default=False),
        ),
        migrations.AlterField(
            model_name='referencerange',
            name='published',
            field=models.BooleanField(help_text='Published must be a green check icon in order to use this in a CM. This is not user editable. It is managed by the publication process.', verbose_name='published', default=False),
        ),
    ]
