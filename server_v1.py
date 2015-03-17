import SocketServer
import sys
import json
import os
import MySQLdb #descomentar para utilizar la base de datos
import dataHandler
from fileHandler import FileHandler
from dbHandler import BDHandler

TCP_IP = '' #direccion ip donde escucha se deja vacia para escuchar en todas
TCP_PORT = 80 #puerto donde escucha
BUFFER_SIZE = 1024  #tamano del buffer, ajustarlo al tamano maximo del paquete json
datos = []
data_handler = None

class TCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
		self.data = self.request.recv(BUFFER_SIZE).strip()
		if(self.data == '' or self.data == None):
                        return
                else:
                        print "{} wrote".format(self.client_address[0])
                        j = json.loads(self.data, object_hook=_decode_dict)
                        dataHandler.saveJson(j)
		
if __name__ == "__main__":
	if(len(sys.argv) > 1 and sys.argv[1] == "bd"):
		data_handler = BDHandler()
	else:
		data_handler = FileHandler()
	server = SocketServer.TCPServer((TCP_IP, TCP_PORT), TCPHandler)
	server.serve_forever()