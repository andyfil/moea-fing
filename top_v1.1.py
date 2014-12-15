#!/usr/bin/python

import os
from subprocess import Popen
import re
import time
import socket
import json

print "COMIENZO A LEER DEL TOP"

while 1:
	#salida = os.popen("/usr/bin/top -n 1").read()
	#lineas = salida.split("\n")
	lineas = os.popen("/usr/bin/top -n 1").readlines()
	#print (u''+lineas[7]).split()
	firstLine = lineas[0].split(",") 							#Gral. Inf. of pc
	tokens = firstLine[0].split()
	JSON = ""	
	nombre_pc = socket.gethostname()											# PC
	JSON = '"nombre_pc": ' + nombre_pc + "," + "\n"	
	JSON += '"timestamp": ' + time.strftime("%x") + " " + tokens[2] + "," + "\n" 	# TimeStamp
	JSON += '"state": ' + tokens[3] + "," + "\n"									# State --- No esta levantando el estado del sistema
	JSON += '"on_time": ' + tokens[4] + "," + "\n" 								# On time
	tokens = firstLine[1].split()												# Users
	JSON += '"users": ' + tokens[0] + "," + "\n"
	secondLine = lineas[1].split(",") # Process
	tokens = secondLine[0].split()
	JSON += '"process": ' + tokens[1] + "," + "\n"
	tokens = secondLine[1].split()
	JSON += '"process_active": ' + tokens[1] + "," + "\n"
	tokens = secondLine[2].split()
	JSON += '"process_Sleep": ' + tokens[1] + "," + "\n"
	# Procces x User
	lineas_procesos = lineas[7:-1]
	diccionario = {}
	p = re.compile('\d+\s(\w+)')
	for linea_proc in lineas_procesos:
		m = p.findall(linea_proc.strip())
		user = m[0]
		if (user in diccionario):
			diccionario[user] += 1
		else:
			diccionario[user] = 1
	JSON += '"process_per_user": '+ json.dumps(diccionario)+ ",\n"
	thirdLine = lineas[2].split(",") # CPU use
	tokens = thirdLine[0].split()
	JSON += '"cpu_use": ' + tokens[1][-3] + "," + "\n"
	fourthLine = lineas[3].split(",") # Memory use
	tokens = fourthLine[0].split()
	memTotal = float(tokens[2][:-1])
	tokens = fourthLine[1].split()
	memUsed = float(tokens[1][:-1])
	#print tokens
	strPorcMem = str(round((memUsed/memTotal)*100,1))
	JSON += '"memory_used": ' + strPorcMem + "\n"
	#print "JSON\n",JSON	
	time.sleep(5)	
print "TERMINO DE LEER DEL TOP"
