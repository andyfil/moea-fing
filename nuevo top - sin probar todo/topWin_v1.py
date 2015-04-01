import top
import os
from subprocess import Popen
import re
import time
import socket
import subprocess
import json
import psutil

class TopWin_v1(top.Top):

	tareas = subprocess.check_output(['tasklist', '-v']).split("\n")
	
	cantProcessActive = 0
	cantProcessSleep = 0
	for indice in range(4,len(tareas)-1):
		strTarea = tareas[indice].split()
		# Busco comienzo del PID 
		i = 1
		while (not strTarea[i].isdigit()):
				i+=1
		stateProcess = strTarea[i-1+6]
		if (stateProcess == "Running"):
			cantProcessActive += 1
		if (stateProcess == "Unknown"):
			cantProcessSleep += 1

			
	def obtenerPc(self):
		host = subprocess.check_output(['hostname']).strip()
		return host
			
	def obtenerTimestamp(self):
		fechaHoy = time.strftime("%Y/%m/%d %H:%M:%S")
		return fechaHoy

	def obtenerState(self):
		users = psutil.users()
		if (len(users) == 0):
			state = "SLEEP"
		else:
			state = "RUNNING"
		return state
			
	def obtenerOn_time(self):
		tiempos = psutil.cpu_times()
		onTime = int(tiempos[2]/60/60)
		return onTime
	
	def obtenerUsers(self):
		users = []
		for indice in range(3,len(tareas)-1):
				strTarea = tareas[indice].split()
				i = 1
				while (not strTarea[i].isdigit()):
						i+=1
				user = int(strTarea[i- 1 + 3])
				users.append(user)
		cantUsers = len(list(set(users)))
		return cantUsers

	def obtenerProcess(self):
		cantProcess = len(tareas) - 5
		return cantProcess
		
	def obtenerProcess_active(self):
		return cantProcessActive
			
	def obtenerPC(self):
		return cantProcessSleep
			
	def obtenerProcess_per_user(self):
		diccionario = {}
		#p = re.compile('\d+\s(\w+)')
		for indice in range(4, len(tareas)-1): #lineas_procesos:
			# Busco comienzo del PID 
			i = 1
			while (not strTarea[i].isdigit()):
					i+=1
			user = (tareas[indice].split())[i-1+3]
			if (user in diccionario):
				diccionario[user] += 1
			else:
				diccionario[user] = 1
		return json.dumps(diccionario)

	def obtenerCpu_use(self):
		cpu_use = round(psutil.cpu_percent(),1)
		return cpu_use
			
	def obtenerPC(self):
		percentMem = psutil.virtual_memory()[2]
		return percentMem
