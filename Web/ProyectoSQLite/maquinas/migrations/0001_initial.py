# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Datos',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('pc', models.CharField(max_length=45)),
                ('timestamp', models.DateTimeField(null=True, blank=True)),
                ('state', models.CharField(max_length=45, blank=True)),
                ('on_time', models.IntegerField(null=True, blank=True)),
                ('users', models.IntegerField(null=True, blank=True)),
                ('process', models.IntegerField(null=True, blank=True)),
                ('process_active', models.IntegerField(null=True, blank=True)),
                ('process_sleep', models.IntegerField(null=True, blank=True)),
                ('process_per_user', models.CharField(max_length=500, blank=True)),
                ('cpu_use', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
                ('memory_use', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
            ],
            options={
                'db_table': 'datos',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Datos_Lecturas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pc', models.CharField(max_length=200)),
                ('timestamp', models.DateTimeField(verbose_name=b'Timestamp')),
                ('state', models.CharField(max_length=200)),
                ('on_time', models.IntegerField()),
                ('users', models.IntegerField()),
                ('process', models.IntegerField()),
                ('process_active', models.IntegerField()),
                ('process_sleep', models.IntegerField()),
                ('process_per_user', models.CharField(max_length=500)),
                ('cpu_use', models.DecimalField(max_digits=10, decimal_places=2)),
                ('memory_use', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='LecturaTop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tiempo_lectura', models.DateTimeField(verbose_name=b'Tiempo de lectura')),
                ('cant_usuarios', models.IntegerField()),
                ('mem_perc', models.IntegerField()),
                ('cpu_perc', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Pc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('ip', models.CharField(max_length=150)),
                ('mac', models.CharField(max_length=200)),
                ('so', models.CharField(max_length=100)),
                ('ram', models.IntegerField()),
                ('cpu', models.DecimalField(max_digits=3, decimal_places=1)),
                ('arq', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Proceso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pid', models.IntegerField()),
                ('user_id', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=200)),
                ('tiempo_ini', models.FloatField()),
                ('tiempo', models.FloatField()),
                ('comando', models.CharField(max_length=200)),
                ('memoria_minimo', models.IntegerField()),
                ('memoria_promedio', models.IntegerField()),
                ('memoria_maximo', models.IntegerField()),
                ('cpu_minimo', models.DecimalField(max_digits=3, decimal_places=1)),
                ('cpu_promedio', models.DecimalField(max_digits=3, decimal_places=1)),
                ('cpu_maximo', models.DecimalField(max_digits=3, decimal_places=1)),
            ],
        ),
        migrations.CreateModel(
            name='RegistroPc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_alta', models.DateTimeField(verbose_name=b'Fecha de alta')),
                ('pc', models.ForeignKey(to='maquinas.Pc')),
            ],
        ),
        migrations.CreateModel(
            name='Salon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('lugar', models.CharField(max_length=200)),
                ('prioridad', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('tiempo_ini', models.FloatField()),
                ('tiempo', models.FloatField()),
                ('memoria_minimo', models.IntegerField()),
                ('memoria_promedio', models.IntegerField()),
                ('memoria_maximo', models.IntegerField()),
                ('cpu_minimo', models.DecimalField(max_digits=3, decimal_places=1)),
                ('cpu_promedio', models.DecimalField(max_digits=3, decimal_places=1)),
                ('cpu_maximo', models.DecimalField(max_digits=3, decimal_places=1)),
            ],
        ),
        migrations.AddField(
            model_name='pc',
            name='salon',
            field=models.ForeignKey(to='maquinas.Salon'),
        ),
        migrations.AddField(
            model_name='lecturatop',
            name='pc',
            field=models.ForeignKey(to='maquinas.Pc'),
        ),
        migrations.AddField(
            model_name='datos',
            name='id_pc',
            field=models.ForeignKey(db_column=b'id_pc', blank=True, to='maquinas.Pc', null=True),
        ),
    ]
