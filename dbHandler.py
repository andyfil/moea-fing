import dataHandler 
import MySQLdb 
import json
import sys
import constantes as cts

class BDHandler(dataHandler.DataHandler):
	"""Clase que implementa a dataHandler, permite almacenar la informacion obtenida en base de datos"""
	host = cts.host
	user = cts.user
	password = cts.password
	database = cts.database
    
	def __init__(self):
		self.db = MySQLdb.connect(self.host, self.user, self.password, self.database)
		self.cursor = self.db.cursor()
	
	def __del__(self):
		self.db.close()	
		
	def armar_salon(fila):
		salon = {}
		salon[cts.ident] = fila[0]
		salon[cts.nombre] = fila[1]
		salon[cts.lugar] = fila[2]
		salon[cts.prioridad] = fila[3]
		return salon

	def execute(self,query, datos_query):
		try:
			self.cursor.execute(query,datos_query)
			self.db.commit()
		except MySQLdb.Error, e:
			try:
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			except IndexError, e2:
				print "MySQL Error: %s" % str(e2)
			except AttributeError, e3:	
				print e3
			finally:
				self.db.rollback()
		except:
			print "Unexpected error:", sys.exc_info()[0]
			self.db.rollback()

	def saveJson(self, jdata):
		query = "INSERT INTO %s	(`pc`,`timestamp`,`state`,`on_time`,`users`,`process`, `process_active`,`process_sleep`, `process_per_user`,`cpu_use`,`memory_use`) " %cts.tabla_registro 
		query += "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
		datos_query = (jdata[cts.pc],jdata[cts.timestamp],jdata[cts.state],jdata[cts.on_time],jdata[cts.users],jdata[cts.process],jdata[cts.process_active],jdata[cts.process_sleep],json.dumps(jdata[cts.process_per_user]),jdata[cts.cpu_use],jdata[cts.memory_use])
		self.execute(query,datos_query)


	def saveSalon(self,jdata):
		"Metodo que agrega un salon a la estructura de datos"
		query = "INSERT INTO %s	(`nombre`,`lugar`,`prioridad`) " %cts.tabla_salon 
		query += "VALUES(%s,%s,%s);"
		jdata[cts.prioridad] = 0
		datos_query = (jdata[cts.nombre],jdata[cts.lugar],jdata[cts.prioridad])
		self.execute(query,datos_query)

	def registerPC(self,jdata):
		"Metodo que registra una pc y devuelve el identificador de la misma"
		pass

	def getSalon(self,jdata):
		"Metodo para obtener informacion de un salon"
		try:
			query = "SELECT id, nombre,lugar,prioridad FROM %s"% cts.tabla_salon
			if jdata:
				where = ""
				if jdata[cts.ident]:
					where += "WHERE id = %s"% jdata[cts.ident]
				if jdata[cts.nombre]:
					if where == "":
						where = "WHERE"
					else:
						where += " and "						
					where += "id = %s"% jdata[cts.ident]
			query += where
			self.cursor.execute(query)
			datos = self.cursor.fetchall()
			return [armar_salon(salon) for salon in datos]
		except:
			print "Error: no se pudo obtener datos de salon de la base de datos"


	def updateSalon(self,jdata):
		"Metodo para obtener informacion de un salon"
		pass