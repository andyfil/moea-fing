import socket
import sys
import json
import topWin_v1 as top
import time
#import topLin_v1 as top

#TCP_IP = '164.73.44.114' pcunix114
TCP_IP = 'fingproy.cloudapp.net'
TCP_PORT = 80
BUFFER_SIZE = 1024
MESSAGE = '{"pc": "pcunix114",	"timestamp": "2014-12-10 10:48:20",	"state": "working",	"on_time": 1238.3,	"users": 3,	"process": 98,	"process_active": 5,	"process_sleep": 93,	"process_per_user": [10,2,4],	"cpu_use": 34.2,	"memory_use": 45.0}'#Mensaje JSON de prueba

def funcionTop():
	"Funcion que parsea la salida del top y devuelve un json con la informacion"
	return top.obtener_datos()

	
server_address = (TCP_IP, TCP_PORT)


for i in range(1,100):
	try:
		sock = socket.create_connection(server_address)
		data = funcionTop()
		#print data
		sock.sendall(data)
		time.sleep(2)
	except:
		print "Error inesperado:", sys.exc_info()
	finally:
		print >>sys.stderr, 'Cerrando socket'
		sock.close()
