import time
import subprocess
import psutil

from top import Top

class TopWin_v1(Top):

	def __init__(self):
		print "Inciciando Top de windows"
		self.tareas = subprocess.check_output(['tasklist', '-v']).split("\n")

		self.cantProcessActive = 0
		self.cantProcessSleep = 0
		for indice in range(4,len(self.tareas)-1):
			strTarea = self.tareas[indice].split()
			# Busco comienzo del PID
			i = 1
			while (not strTarea[i].isdigit()):
					i+=1
			stateProcess = strTarea[i-1+6]
			if (stateProcess == "Running"):
				self.cantProcessActive += 1
			if (stateProcess == "Unknown"):
				self.cantProcessSleep += 1

	def obtenerPc(self):
		host = subprocess.check_output(['hostname']).strip()
		return host

	def obtenerTimestamp(self):
		fechaHoy = time.strftime("%Y/%m/%d %H:%M:%S")
		return fechaHoy

	def obtenerState(self):
		users = psutil.users()
		if (len(users) == 0):
			state = "SLEEP"
		else:
			state = "RUNNING"
		return state

	def obtenerOn_time(self):
		tiempos = psutil.cpu_times()
		onTime = int(tiempos[2]/60/60)
		return onTime

	def obtenerUsers(self):
		users = []
		for indice in range(3,len(self.tareas)-1):
				strTarea = self.tareas[indice].split()
				i = 1
				while (not strTarea[i].isdigit()):
						i+=1
				user = int(strTarea[i- 1 + 3])
				users.append(user)
		cantUsers = len(list(set(users)))
		return cantUsers

	def obtenerProcess(self):
		print "Largo de tareas: " + str(len(self.tareas))
		cantProcess = len(self.tareas) - 5
		return cantProcess

	def obtenerProcess_active(self):
		return self.cantProcessActive

	def obtenerProcess_sleep(self):
		return self.cantProcessSleep

	def obtenerProcess_per_user(self):
		diccionario = {}
		#p = re.compile('\d+\s(\w+)')
		for indice in range(4, len(self.tareas)-1):
			strTarea = self.tareas[indice].split()
			# Busco comienzo del PID
			i = 1
			while (not strTarea[i].isdigit()):
					i+=1
			user = (self.tareas[indice].split())[i-1+3]
			if (user in diccionario):
				diccionario[user] += 1
			else:
				diccionario[user] = 1
		return diccionario

	def obtenerCpu_use(self):
		cpu_use = round(psutil.cpu_percent(),1)
		print "USO CPU: " + str(cpu_use)
		return cpu_use

	def obtenerMemory_use(self):
		percentMem = psutil.virtual_memory()[2]
		return percentMem
