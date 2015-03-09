#!/usr/bin/python

import os
from subprocess import Popen
import re
import time
import socket
import subprocess
import json
import psutil

while 1:
	#op"lineas = os.popen("tasklist -n 1").readlines()
	
	#Gral. Inf. of pc
	#tareas = subprocess.check_output(['systeminfo']).split("\n")
	########################################
	#f = open("C:\Users\usuario\Desktop\salidaSystemInfo.txt", "w")
	#for tarea in tareas:
	#	f.write(tarea)
	#f.close()
	########################################
	#memVirMax = float ((tareas[26].split())[4])
	#memVirUse = float ((tareas[28].split())[4])
	#porcMemUse = round((memVirUse*100)/memVirMax,1)
	# Variable de JSON
	JSON = "{"#comienzo JSON
	# PC 
	users = psutil.users()
	hostIP = str(str(users[0]).split(",")[2]).split("=")[1]
	strHostIP = hostIP.replace("'", "")        # Elimino el caracter '
	JSON += '"pc": "' + strHostIP + '", '
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
	########################################
	f = open("C:\Users\usuario\Desktop\salidaTaskListV.txt", "w")
	for tarea in tareas:
		f.write(tarea)
	f.close()
	########################################
	users = []
	for indice in range(3,len(tareas)-1):
		strTarea = tareas[indice].split()
		user = int(strTarea[3])
		users.append(user)
	cantUsers = len(list(set(users)))
	JSON += '"users": ' + str(cantUsers) + ", "
	# Process
	cantProcess = len(tareas) - 5 # System Idle Process no cuenta
	JSON += '"proces": ' + str(cantProcess) + ", "
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
		 #m = p.findall(linea_proc.strip())
		 #user = m[0]
		"""if ( ((tareas[indice].split())[0] == "System") 
		and ((tareas[indice].split())[1] == "Idle") 
		and ((tareas[indice].split())[2] == "Process") ):
			user = "NT AUTHORITY\SYSTEM"
		else:"""
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
	
	print JSON ### PARA PROBAR ###
	#return JSON

	time.sleep(5)
		
print "TERMINO DE LEER DEL TOP" # Nunca lo va a mostrar