#!/usr/bin/python

import os
from subprocess import Popen
import re
import time
import socket
import subprocess
import json


print "COMIENZO A LEER"

while 1:
	#op"lineas = os.popen("tasklist -n 1").readlines()
	
	#Gral. Inf. of pc
	# Variable de JSON
	JSON = ""
	tareas = subprocess.check_output(['systeminfo']).split("\n")
	########################################
	f = open("C:\Users\usuario\Desktop\salidaSystemInfo.txt", "w")
	for tarea in tareas:
		f.write(tarea)
	f.close()
	########################################
	memVirMax = float ((tareas[26].split())[4])
	memVirUse = float ((tareas[28].split())[4])
	porcMemUse = round((memVirUse*100)/memVirMax,1)
	# PC 
	strHost = tareas[1].split()
	JSON += '"pc": "%s"' %strHost[3] + ",\n"
	# TimeStamp
	fechaHoy = time.strftime("%c")
	JSON += '"timestamp": "%s"' %fechaHoy + ",\n"
	# State
	state = ""
	#JSON += '"state": "%s"' %state + ",\n"
	# On time
	#JSON += '"on_time": "%s"' %on_time + ",\n"
	# Users
	tareas = subprocess.check_output(['tasklist', '-v']).split("\n")
	maxUser = -1
	########################################
	f = open("C:\Users\usuario\Desktop\salidaTaskListV.txt", "w")
	for tarea in tareas:
		f.write(tarea)
	f.close()
	########################################
	for indice in range(3,len(tareas)-1):
		strTarea = tareas[indice].split()
		user = int(strTarea[3])
		if (user > maxUser):
			maxUser = user
	cantUsers = maxUser + 1
	JSON += '"users": ' + str(cantUsers) + ",\n"
	# Process
	cantProcess = len(tareas) - 4
	JSON += '"proces": ' + str(cantProcess) + ",\n"
	# Process Active
	cantProcessActive = 1
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
	print JSON
	# Procces x User
	 #lineas_procesos = lineas[7:-1]
	diccionario = {}
	 #p = re.compile('\d+\s(\w+)')
	for indice in range(3, len(tareas)-1): #lineas_procesos:
		 #m = p.findall(linea_proc.strip())
		 #user = m[0]
		if ( ((tareas[indice].split())[0] == "System") 
		and ((tareas[indice].split())[1] == "Idle") 
		and ((tareas[indice].split())[2] == "Process") ):
			user = "NT AUTHORITY\SYSTEM"
		else:
			user = (tareas[indice].split())[7]
		if (user == "Responding"):
			user = (tareas[indice].split())[8]
		if (user in diccionario):
			diccionario[user] += 1
		else:
			diccionario[user] = 1
	JSON += '"process_per_user": '+ json.dumps(diccionario)+ ",\n"
	# Cpu Use
	# %Mem used
	JSON += '"memory_use": '+ str(porcMemUse) + ",\n"
	print JSON

	time.sleep(5)
		
print "TERMINO DE LEER DEL TOP" # Nunca lo va a mostrar