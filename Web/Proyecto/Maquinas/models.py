from django.db import models
import datetime

class Salon(models.Model):
	nombre = models.CharField(max_length=200)
	lugar = models.CharField(max_length=200)
	prioridad = models.IntegerField()
	def __str__(self):
		return self.nombre
		
class PC(models.Model):
	salon = models.ForeignKey(Salon)
	nombre = models.CharField(max_length=200)
	mac = models.CharField(max_length=200)
	so = models.CharField(max_length=200)
	ram = models.CharField(max_length=200)
	cpu = models.CharField(max_length=200)
	estado = models.CharField(max_length=200)
	cant_usuarios = models.IntegerField()
	def __str__(self):
		return self.nombre
		
class RegistroPC(models.Model):
	pc = models.ForeignKey(PC)
	fecha_alta = models.DateTimeField('Fecha de alta')
	# Datos que registra la PC
	
