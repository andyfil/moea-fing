import SocketServer
import sys
import json
import os
import MySQLdb #descomentar para utilizar la base de datos

TCP_IP = '' #direccion ip donde escucha se deja vacia para escuchar en todas
TCP_PORT = 80 #puerto donde escucha
BUFFER_SIZE = 1024  #tamano del buffer, ajustarlo al tamano maximo del paquete json
datos = []

def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

class BDHandler():
	host = '127.0.0.1'
	user = 'user'
	password = 'user'
	db = 'fing'
    
	def __init__(self):
		self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db)
		self.cursor = self.connection.cursor()
	
	def __del__(self):
		self.connection.close()	
		
	def saveJson(self, jdata):
		try:
			query = "INSERT INTO datos 	(`pc`,`timestamp`,`state`,`on_time`,`users`,`process`, `process_active`,`process_sleep`, `process_per_user`,`cpu_use`,`memory_use`) VALUES	( %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
			print "query: ",query
			datos_query = (jdata['pc'],jdata['timestamp'],jdata['state'],jdata['on_time'],jdata['users'],jdata['process'],jdata['process_active'],jdata['process_sleep'],json.dumps(jdata['process_per_user']),jdata['cpu_use'],jdata['memory_use'])
			#datos_query = (jdata['pc'],jdata['timestamp'],jdata['state'],jdata['on_time'],jdata['users'],jdata['process'],jdata['process_active'],jdata['process_sleep'],'',jdata['cpu_use'],jdata['memory_use'])
			print "datos: ",datos_query
			self.cursor.execute(query,datos_query)
			self.connection.commit()
		except MySQLdb.Error, e:
                        try:
                                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                        except IndexError:
                                print "MySQL Error: %s" % str(e)
                        self.connection.rollback()
                except AttributeError, e:
                        print e
		except:
                        print "Unexpected error:", sys.exc_info()[0]
			self.connection.rollback()

		
class FileHandler():
		
	def __init__(self):
			self.f = open("archivo.log",'w')	
			self.f.write('pc;timestamp;state;on_time;users;process;process_active;process_sleep;process_per_user;cpu_use;memory_use\n')
			self.f.flush()
			os.fsync(self.f)	
	def __del__(self):
		self.f.close()
		
	
	def saveJson(self,jdata):
		csv = '{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10}\n'.format(jdata['pc'],jdata['timestamp'],jdata['state'],jdata['on_time'],jdata['users'],jdata['process'],jdata['process_active'],jdata['process_sleep'],jdata['process_per_user'],jdata['cpu_use'],jdata['memory_use'])
		self.f.write(csv)
		self.f.flush()

		
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
	dataHandler = BDHandler()
	#dataHandler = FileHandler()
	server = SocketServer.TCPServer((TCP_IP, TCP_PORT), TCPHandler)
	server.serve_forever()