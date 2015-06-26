#Revision number $Revision$

from django.db import models
import datetime

class Salon(models.Model):
	nombre = models.CharField(max_length=200)
	lugar = models.CharField(max_length=200)
	prioridad = models.IntegerField()
	def __str__(self):
		return self.nombre

class Pc(models.Model):
	salon = models.ForeignKey(Salon)
	nombre = models.CharField(max_length=200)
	ip = models.CharField(max_length=150)
	mac = models.CharField(max_length=200)
	so = models.CharField(max_length=100)
	ram = models.IntegerField()
	cpu = models.DecimalField(max_digits=3, decimal_places=1)
	arq = models.CharField(max_length=50)
	estado = models.CharField(max_length=50)
	def __str__(self):
		return self.nombre

class RegistroPc(models.Model):
	pc = models.ForeignKey(Pc)
	fecha_alta = models.DateTimeField('Fecha de alta')
	# Datos que registra la PC

class LecturaTop(models.Model):
	pc = models.ForeignKey(Pc)
	tiempo_lectura = models.DateTimeField('Tiempo de lectura')
	cant_usuarios = models.IntegerField()
	mem_perc = models.IntegerField()
	cpu_perc = models.IntegerField()
	def __str__(self):
		return "Lectura"

class Datos_Lecturas(models.Model):
	pc = models.CharField(max_length=200)
	timestamp = models.DateTimeField('Timestamp')
	state = models.CharField(max_length=200)
	on_time = models.IntegerField()
	users = models.IntegerField()
	process = models.IntegerField()
	process_active = models.IntegerField()
	process_sleep = models.IntegerField()
	process_per_user = models.CharField(max_length=500)
	cpu_use = models.DecimalField(max_digits=10, decimal_places=2)
	memory_use = models.DecimalField(max_digits=10, decimal_places=2)

class Usuario(models.Model):
	id_pc = models.ForeignKey('Pc', db_column='id_pc', blank=True, null=True)
	nombre = models.CharField(max_length=200)
	tiempo_ini = models.FloatField()
	tiempo = models.FloatField()
	memoria_minimo = models.IntegerField()
	memoria_promedio = models.IntegerField()
	memoria_maximo = models.IntegerField()
	cpu_minimo = models.DecimalField(max_digits=3, decimal_places=1)
	cpu_promedio = models.DecimalField(max_digits=3, decimal_places=1)
	cpu_maximo = models.DecimalField(max_digits=3, decimal_places=1)

class Proceso(models.Model):
	id_pc = models.ForeignKey('Pc', db_column='id_pc', blank=True, null=True)
	pid = models.IntegerField()
	user_id = models.CharField(max_length=50)
	name =	models.CharField(max_length=200)
	tiempo_ini = models.FloatField()
	tiempo = models.FloatField()
	comando = models.CharField(max_length=200)
	memoria_minimo = models.IntegerField()
	memoria_promedio = models.IntegerField()
	memoria_maximo = models.IntegerField()
	cpu_minimo = models.DecimalField(max_digits=3, decimal_places=1)
	cpu_promedio = models.DecimalField(max_digits=3, decimal_places=1)
	cpu_maximo = models.DecimalField(max_digits=3, decimal_places=1)

class Datos(models.Model):
	id = models.IntegerField(primary_key=True)	# AutoField?
	id_pc = models.ForeignKey('Pc', db_column='id_pc', blank=True, null=True)
	pc = models.CharField(max_length=45)
	timestamp = models.DateTimeField(blank=True, null=True)
	state = models.CharField(max_length=45, blank=True)
	on_time = models.IntegerField(blank=True, null=True)
	users = models.IntegerField(blank=True, null=True)
	process = models.IntegerField(blank=True, null=True)
	process_active = models.IntegerField(blank=True, null=True)
	process_sleep = models.IntegerField(blank=True, null=True)
	process_per_user = models.CharField(max_length=500, blank=True)
	cpu_use = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	memory_use = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'datos'
