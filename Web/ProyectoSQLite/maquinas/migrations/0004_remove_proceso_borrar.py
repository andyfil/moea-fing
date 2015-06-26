# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maquinas', '0003_proceso_borrar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proceso',
            name='borrar',
        ),
    ]
