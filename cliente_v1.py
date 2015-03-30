import socket
import sys
import json
import topWin_v1 as top
import time
import requests
#import topLin_v1 as top

#TCP_IP = '164.73.44.114' pcunix114
TCP_IP = 'fingproy.cloudapp.net'
TCP_PORT = 80
id = 1
BASE_URL = "http://fingproy.cloudapp.net:5000/proy/api/v1/pcs/"
PROXY="http://proxy.fing.edu.uy"
#PROXY=""
PROXY_PORT=3128
MESSAGE = '{"pc": "pcunix114","timestamp": "2014-12-10 10:48:20","state": "working","on_time": 1238.3,"users": 3,"process": 98,"process_active": 5,"process_sleep": 93,"process_per_user":[10,2,4],"cpu_use": 34.2,"memory_use": 45.0}'#Mensaje JSON de prueba

def funcionTop():
	"Funcion que parsea la salida del top y devuelve un json con la informacion"
	#aca se deberia hacer que en base al SO del cliente eliga cual de los top debe tomar, en lugar de tener que hacer la configuracion manual
	return top.obtener_datos()
	
def proxi():
	if PROXY:
		return {"http":PROXY +':'+ str(PROXY_PORT)}
	else:
		return {}
try:
	data = funcionTop()
	url = BASE_URL + str(id)
	headers = {'content-type': 'application/json'}
	r = requests.post(url,data = data,headers = headers, proxies= proxi())
	print r
except:

	print "Error inesperado:", sys.exc_info()
finally:
	print >>sys.stderr, 'Cerrando socket'