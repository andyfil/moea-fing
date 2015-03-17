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
		"Metodo que procesa un json recibido y lo almacena"
		pass