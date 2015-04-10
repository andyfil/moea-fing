import os
from subprocess import Popen
import re
import top
import os
from subprocess import Popen
import re
import time
import socket
import json

class TopLin_v1(top.Top):

	def __init__(self):
		print "Inciciando Top de linux"
		self.lineas = os.popen("/usr/bin/top -n 1").readlines()
		self.firstLine = self.lineas[0].split(",")
		self.tokens = self.firstLine[0].split()
			
			
	def obtenerPc(self):
		host = socket.gethostname() 
		return host
			
	def obtenerTimestamp(self):
		fechaHoy = time.strftime("%Y/%m/%d %H:%M:%S")
		return fechaHoy

	def obtenerState(self):
		state = self.tokens[3]
		return state
			
	def obtenerOn_time(self):
		days = float(self.tokens[4])
		horas = abs(days*24)
		horas_restantes = float(self.firstLine[1].split(":")[0])
		on_time = horas + horas_restantes
		return on_time
	
	def obtenerUsers(self):
		tokens = self.firstLine[2].split()
		cantUsers = tokens[0]
		return cantUsers

	def obtenerProcess(self):
		self.secondLine = self.lineas[1].split(",")
		tokens = self.secondLine[0].split()
		cantProcess = int(tokens[1])
		return cantProcess
		
	def obtenerProcess_active(self):
		tokens = self.secondLine[1].split()
		cantProcessActive = tokens[1]
		return cantProcessActive
			
	def obtenerProcess_sleep(self):
		tokens = self.secondLine[2].split()
		cantProcessSleep = tokens[1] 
		return cantProcessSleep
		
	def obtenerProcess_per_user(self):
		lineas_procesos = self.lineas[7:-1]
		diccionario = {}
		reg_user = re.compile('\d+\s(\w+)')
		for linea_proc in lineas_procesos:
				res = reg_user.findall(linea_proc.strip())
				user = res[0]
				if (user in diccionario):
						diccionario[user] += 1
				else:
						diccionario[user] = 1
		return diccionario

	def obtenerCpu_use(self):
		cpu = re.sub(r'\x1b[^m]*m','',self.lineas[2].strip())
		cpu = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', cpu)
		reg_cpu = re.compile('([0-9\.]){1,5}\sid')
		res = reg_cpu.findall(cpu)
		cpu_use = float(res[0])
		return cpu_use
		
	def obtenerMemory_use(self):
		fourthLine = re.sub(r'\x1b[^m]*m','',self.lineas[3])
		fourthLine = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', fourthLine)
		fourthLine = fourthLine.split(",")
		tokens = fourthLine[0].split()
		memTotal = float(tokens[3][:-1]) 
		tokens = fourthLine[1].split()
		memUsed = float(tokens[0][:-1])
		percentMem = round((memUsed/memTotal)*100,1)
		return percentMem
