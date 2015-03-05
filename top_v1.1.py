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
	JSON += '"process_sleep": ' + tokens[1] + "," + "\n"
	# Procces x User
	lineas_procesos = lineas[7:-1]
	diccionario = {}
	reg_user = re.compile('\d+\s(\w+)')
	for linea_proc in lineas_procesos:
		res = reg_user.findall(linea_proc.strip())
		user = res[0]
		if (user in diccionario):
			diccionario[user] += 1
		else:
			diccionario[user] = 1
	JSON += '"process_per_user": '+ json.dumps(diccionario)+ ",\n"
	cpu = re.sub(r'\x1b[^m]*m','',lineas[2].strip())
	cpu = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', cpu)
	reg_cpu = re.compile('([0-9\.]){1,5}\sid')
	res = reg_cpu.findall(cpu)
	cpu_use = 100 - float(res[0])
	JSON += '"cpu_use": ' +  str(cpu_use) + "," + "\n"
	fourthLine = re.sub(r'\x1b[^m]*m','',lineas[3])
	fourthLine = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', fourthLine)
	fourthLine = fourthLine.split(",") # Memory use
	tokens = fourthLine[0].split()
	memTotal = float(tokens[3][:-1]) 
	tokens = fourthLine[1].split()
	memUsed = float(tokens[0])
	strPorcMem = str(round((memUsed/memTotal)*100,1))
	JSON += '"memory_used": ' + strPorcMem + "\n"
	print "JSON\n",JSON	
	time.sleep(5)	
print "TERMINO DE LEER DEL TOP"
