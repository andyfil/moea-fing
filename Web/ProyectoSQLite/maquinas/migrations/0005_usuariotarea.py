# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maquinas', '0004_remove_proceso_borrar'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioTarea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('usuario', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('archivo', models.FileField(upload_to=b'archivos/%Y/%m/%d')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
