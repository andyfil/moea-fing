from abc import ABCMeta, abstractmethod
import os

class Top():
	__metaclass__ = ABCMeta

	def obtener_datos(self, top):
		
		JSON = 	{}
		JSON['pc'] = top.obtenerPc()
		JSON['timestampc'] = top.obtenerTimestamp()
		JSON['state'] = top.obtenerState()
		JSON['on_time'] = top.obtenerOn_time()
		JSON['users'] = top.obtenerUsers()
		JSON['process'] = top.obtenerProcess()
		JSON['process_active'] = top.obtenerProcess_active()
		JSON['process_sleep'] = top.obtenerProcess_sleep()
		JSON['process_per_user'] = top.obtenerProcess_per_user()
		JSON['cpu_use'] = top.obtenerCpu_use()
		JSON['memory_use'] = top.obtenerMemory_use()
		
		return JSON.dumps()


	@abstractmethod
	def obtenerPc(self):
			"Obtengo la pc"
			pass
			
	@abstractmethod
	def obtenerTimestamp(self):
			"Obtengo fecha y hora"
			pass
		
	@abstractmethod
	def obtenerState(self):
			"Obtengo el estado de la pc"
			pass
			
	@abstractmethod
	def obtenerOn_time(self):
			"Obtengo tiempo iniciada"
			pass
	
	@abstractmethod
	def obtenerUsers(self):
			"Obtengo cantidad de usuarios"
			pass
		
	@abstractmethod
	def obtenerProcess(self):
			"Obtengo cantidad de procesos"
			pass
			
	@abstractmethod
	def obtenerProcess_active(self):
			"Obtengo cantidad de procesos activos"
			pass
			
	@abstractmethod
	def obtenerPC(self):
			"Obtengo cantidad de procesos dormidos"
			pass
			
	@abstractmethod
	def obtenerProcess_per_user(self):
			"Obtengo procesos por usuario"
			pass
			
	@abstractmethod
	def obtenerCpu_use(self):
			"Obtengo porcentaje de uso cpu"
			pass
			
	@abstractmethod
	def obtenerPC(self):
			"Obtengo porcentaje de uso de memoria"
			pass