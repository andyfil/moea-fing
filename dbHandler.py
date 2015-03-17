import dataHandler 
import MySQLdb 
import json

class BDHandler(dataHandler.DataHandler):
	"""Clase que implementa a dataHandler, permite almacenar la informacion obtenida en base de datos"""
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
			except IndexError, e2:
				print "MySQL Error: %s" % str(e2)
			except AttributeError, e3:	
				print e3
			finally:
				self.connection.rollback()
		except:
			print "Unexpected error:", sys.exc_info()[0]
			self.connection.rollback()