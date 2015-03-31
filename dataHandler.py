from abc import ABCMeta, abstractmethod

class DataHandler():
	__metaclass__ = ABCMeta
		
	@abstractmethod
	def __init__(self):
		pass
	@abstractmethod
	def __del__(self):
		pass

	@abstractmethod
	def saveJson(self,jdata):
		"Metodo que procesa un registro en formato json y lo almacena"
		pass

#begin Salon
	@abstractmethod
	def saveSalon(self,jdata):
		"Metodo que agrega un salon a la estructura de datos"
		pass

	@abstractmethod
	def getSalon(self,jdata):
		"Metodo para obtener informacion de un salon"

	@abstractmethod
	def updateSalon(self,jdata):
		"Metodo para obtener informacion de un salon"
#end Salon

	@abstractmethod
	def registerPC(self,jdata):
		"Metodo que registra una pc y devuelve el identificador de la misma"
		pass

