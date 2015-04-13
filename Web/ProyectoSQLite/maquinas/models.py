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
	mac = models.CharField(max_length=200)
	so = models.CharField(max_length=100)
	ram = models.IntegerField()
	cpu = models.DecimalField(max_digits=3, decimal_places=1)
	arq = models.CharField(max_length=50)
	cant_cores = models.IntegerField()
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

