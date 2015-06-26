# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maquinas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proceso',
            name='id_pc',
            field=models.ForeignKey(db_column=b'id_pc', blank=True, to='maquinas.Pc', null=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='id_pc',
            field=models.ForeignKey(db_column=b'id_pc', blank=True, to='maquinas.Pc', null=True),
        ),
    ]
