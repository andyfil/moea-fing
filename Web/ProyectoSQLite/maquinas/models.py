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

class Usuario(models.Model):
	nombre = models.CharField(max_length=200)
	tiempo_ini = models.DateTimeField('Tiempo de inicio')
	tiempo = models.DateTimeField('Tiempo')
	memoria = models.IntegerField()
	cpu = models.DecimalField(max_digits=3, decimal_places=1)

class Proceso(models.Model):
	pid = models.IntegerField()
	user = models.ForeignKey(Usuario)
	name =  models.CharField(max_length=200)
	tiempo_ini = models.DateTimeField('Tiempo de inicio')
	tiempo = models.DateTimeField('Tiempo')
	comando = models.CharField(max_length=200)
	memoria = models.IntegerField()
	cpu = models.DecimalField(max_digits=3, decimal_places=1)

class Proc(models.Model):
	user = models.ForeignKey(Usuario)
	pid = models.ForeignKey(Proceso)
	cpu = models.DecimalField(max_digits=3, decimal_places=1)
	mem = models.IntegerField()
	vsz = models.CharField(max_length=200)
	rss = models.CharField(max_length=200)
	tty = models.CharField(max_length=200)
	stat = models.CharField(max_length=200)
	start = models.CharField(max_length=200)
	time = models.DateTimeField('Tiempo')
	cmd = models.CharField(max_length=200)

