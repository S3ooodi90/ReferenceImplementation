# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmgen', '0002_auto_20150423_1200'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='predobj',
            options={'verbose_name_plural': 'Predicates+Objects', 'ordering': ['name', 'pred'], 'verbose_name': 'Predicate+Object'},
        ),
        migrations.RemoveField(
            model_name='dvmedia',
            name='size',
        ),
        migrations.RemoveField(
            model_name='dvparsable',
            name='size',
        ),
    ]
