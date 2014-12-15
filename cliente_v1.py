import socket
import sys
import json

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = '{"pc": "pcunix114",	"timestamp": "2014-12-10 10:48:20",	"state": "working",	"on_time": 1238.3,	"users": 3,	"process": 98,	"process_active": 5,	"process_sleep": 93,	"process_per_user": [10,2,4],	"cpu_use": 34.2,	"memory_use": 45.0}'#Mensaje JSON de prueba

def funcionTop():
	"Funcion que parsea la salida del top y devuelve un json con la informacion"
	return MESSAGE
try:
	server_address = (TCP_IP, TCP_PORT)
	sock = socket.create_connection(server_address)
    # Send data
	data = funcionTop()
    sock.sendall(data)
finally:
    print >>sys.stderr, 'Cerrando socket'
    sock.close()