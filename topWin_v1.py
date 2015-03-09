#!/usr/bin/python

import os
from subprocess import Popen
import re
import time
import socket
import subprocess
import json
import psutil

def obtener_datos():
	JSON = "{"#comienzo JSON
	# PC 
	users = psutil.users()
	#hostIP = str(str(users[0]).split(",")[2]).split("=")[1]
	#strHostIP = hostIP.replace("'", "")        # Elimino el caracter '
	#JSON += '"pc": "' + strHostIP + '", '
	host = subprocess.check_output(['hostname']).strip()
	JSON += '"pc": "' + host + '", '
	# TimeStamp
	fechaHoy = time.strftime("%c")
	JSON += '"timestamp": "%s"' %fechaHoy + ", "
	# State
	if (len(users) == 0):
		state = "SLEEP"
	else:
		state = "RUNNING"
	JSON += '"state": "' + state + '", '
	# On time
	tiempos = psutil.cpu_times()
	onTime = int(tiempos[2]/60/60)
	JSON += '"on_time": ' + str(onTime) + ", "
	# Users
	tareas = subprocess.check_output(['tasklist', '-v']).split("\n")
	users = []
	for indice in range(3,len(tareas)-1):
		strTarea = tareas[indice].split()
		i = 1
		while (not strTarea[i].isdigit()):
			i+=1
		user = int(strTarea[i- 1 + 3])
		users.append(user)
	cantUsers = len(list(set(users)))
	JSON += '"users": ' + str(cantUsers) + ", "
	# Process
	cantProcess = len(tareas) - 5 # System Idle Process no cuenta
	JSON += '"process": ' + str(cantProcess) + ", "
	# Process Active
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
	JSON += '"process_active": ' + str(cantProcessActive) + ", "		
	# Process Sleep
	JSON += '"process_sleep": ' + str(cantProcessSleep) + ", "
	# Procces x User
	 #lineas_procesos = lineas[7:-1]
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
	JSON += '"process_per_user": '+ json.dumps(diccionario)+ ", "
	# Cpu Use
	JSON += '"cpu_use": '+ str(round(psutil.cpu_percent(),1))+ ", "
	# %Mem used
	percentMem = psutil.virtual_memory()[2]
	JSON += '"memory_use": '+ str(percentMem)
	JSON += "}" #fin jason
	return JSON