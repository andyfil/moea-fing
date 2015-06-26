# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maquinas', '0002_auto_20150626_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='proceso',
            name='borrar',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
