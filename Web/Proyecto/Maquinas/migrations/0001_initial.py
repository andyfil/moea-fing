# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('mac', models.CharField(max_length=200)),
                ('so', models.CharField(max_length=200)),
                ('ram', models.CharField(max_length=200)),
                ('cpu', models.CharField(max_length=200)),
                ('estado', models.CharField(max_length=200)),
                ('cant_usuarios', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RegistroPC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_alta', models.DateTimeField(verbose_name=b'Fecha de alta')),
                ('pc', models.ForeignKey(to='Maquinas.PC')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Salon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('lugar', models.CharField(max_length=200)),
                ('prioridad', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pc',
            name='salon',
            field=models.ForeignKey(to='Maquinas.Salon'),
            preserve_default=True,
        ),
    ]
