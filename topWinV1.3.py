#!/usr/bin/python

import os
from subprocess import Popen
import re
import time
import socket
import subprocess
import json
import psutil


print "COMIENZO A LEER"

while 1:
	#op"lineas = os.popen("tasklist -n 1").readlines()
	
	#Gral. Inf. of pc
	# Variable de JSON
	JSON = ""
	tareas = subprocess.check_output(['systeminfo']).split("\n")
	########################################
	#f = open("C:\Users\Martin\Desktop\salidaSystemInfo.txt", "w")
	#for tarea in tareas:
#		f.write(tarea)
#	f.close()
	########################################
	memVirMax = float ((tareas[26].split())[4])
	memVirUse = float ((tareas[28].split())[4])
	porcMemUse = round((memVirUse*100)/memVirMax,1)
	# PC 
	strHost = tareas[1].split()
	JSON += '"pc": "%s"' %strHost[2] + ",\n"
	# TimeStamp
	fechaHoy = time.strftime("%c")
	JSON += '"timestamp": "%s"' %fechaHoy + ",\n"
	# State
	state = ""
	JSON += '"state": "%s"' %state + ",\n"
	# On time
	print tareas[1]
	onTime = tareas[1].split()[6]
	JSON += '"on_time": "%s"' %onTime + ",\n"
	# Users
	tareas = subprocess.check_output(['tasklist', '-v']).split("\n")
	########################################
	#f = open("C:\Users\usuario\Desktop\salidaTaskListV.txt", "w")
	#for tarea in tareas:
#		f.write(tarea)
	#f.close()
	########################################
	users = []
	for indice in range(3,len(tareas)-1):
		strTarea = tareas[indice].split()
		user = int(strTarea[3])
		users.append(user)
	cantUsers = len(list(set(users)))
	JSON += '"users": ' + str(cantUsers) + ",\n"
	# Process
	cantProcess = len(tareas) - 5 # System Idle Process no cuenta
	JSON += '"proces": ' + str(cantProcess) + ",\n"
	# Process Active
	cantProcessActive = 0
	cantProcessSleep = 0
	for indice in range(4,len(tareas)-1):
		strTarea = tareas[indice].split()
		stateProcess = strTarea[6]
		if (stateProcess == "Running"):
			cantProcessActive += 1
		if (stateProcess == "Unknown"):
			cantProcessSleep += 1
	JSON += '"process_active": ' + str(cantProcessActive) + ",\n"		
	# Process Sleep
	JSON += '"process_sleep": ' + str(cantProcessSleep) + ",\n"
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
		user = (tareas[indice].split())[3]
		if (user in diccionario):
			diccionario[user] += 1
		else:
			diccionario[user] = 1
	JSON += '"process_per_user": '+ json.dumps(diccionario)+ ",\n"
	# Cpu Use
	JSON += '"cpu_use": '+ str(round(psutil.cpu_percent(),1))+ ",\n"
	# %Mem used
	percentMem = psutil.virtual_memory()[2]
	JSON += '"memory_use": '+ str(percentMem) + ",\n"
	print JSON

	time.sleep(5)
		
print "TERMINO DE LEER DEL TOP" # Nunca lo va a mostrar