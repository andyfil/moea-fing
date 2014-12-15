import SocketServer
import json
import MySQLdb

TCP_IP = '127.0.0.1' #direccion ip donde escucha
TCP_PORT = 5005 #puerto donde escucha
BUFFER_SIZE = 1024  #tamano del buffer, ajustarlo al tamano maximo del paquete json
datos = []


class BDHandler():
	host = 'localhost'
	user = 'root'
	password = 'root'
	db = 'proy'
    
	def __init__(self):
		self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db)
		self.cursor = self.connection.cursor()
	
	def __del__(self):
		self.connection.close()	
		
	def saveJson(self, jdata):
		try:
			csv = "'{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}'".format(jdata['pc'],jdata['timestamp'],jdata['state'],jdata['on_time'],jdata['users'],jdata['process'],jdata['process_active'],jdata['process_sleep'],jdata['process_per_user'],jdata['cpu_use'],jdata['memory_use'])
			query = "INSERT INTO datos 	(`pc`,`timestamp`,`state`,`on_time`,`users`,`process`, `process_active`,`process_sleep`, `process_per_user`,`cpu_use`,`memory_use`) VALUES	("+ csv+ ");"
			#query = "INSERT INTO `proy`.`datos` (`pc`) VALUES ('pc23');"
			print 'ejecute comando'
			print self.cursor.execute(query)
			self.connection.commit()
		except:
			self.connection.rollback()
	
		
class FileHandler():
		
	def __init__(self):
			self.f = open("archivo.log",'w')	
			self.f.write('pc;timestamp;state;on_time;users;process;process_active;process_sleep;process_per_user;cpu_use;memory_use\n')
	
	def __del__(self):
		self.f.close()
		
	
	def saveJson(self,jdata):
		print(jdata['pc'])
		print(jdata['timestamp'])
		print(jdata['state'])
		print(jdata['on_time'])
		print(jdata['users'])
		print(jdata['process'])
		print(jdata['process_active'])
		print(jdata['process_sleep'])
		print(jdata['cpu_use'])
		print(jdata['memory_use'])
		csv = '{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10}\n'.format(jdata['pc'],jdata['timestamp'],jdata['state'],jdata['on_time'],jdata['users'],jdata['process'],jdata['process_active'],jdata['process_sleep'],jdata['process_per_user'],jdata['cpu_use'],jdata['memory_use'])
		self.f.write(csv) 

		
class TCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
		self.data = self.request.recv(BUFFER_SIZE).strip()
		print "{} wrote".format(self.client_address[0])
		j = json.loads(self.data)
		dataHandler.saveJson(j)
		
		
if __name__ == "__main__":
	#dataHandler = BDHandler()
	dataHandler = FileHandler()
	server = SocketServer.TCPServer((TCP_IP, TCP_PORT), TCPHandler)
	server.serve_forever()
	 
	 