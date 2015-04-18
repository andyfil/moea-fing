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
                    i+= 1
            stateProcess = strTarea[i-1+6]
            if stateProcess == "Running":
                self.cantProcessActive += 1
            if stateProcess == "Unknown":
                self.cantProcessSleep += 1

    def get_total_memory(self):
        """Get total amount of RAM memory installed in the pc measured in MB"""
        total = float(psutil.virtual_memory()[0]) /1024
        total /= 1024
        return total

    def get_state(self):
        users = psutil.users()
        if (len(users) == 0):
            state = "SLEEP"
        else:
            state = "RUNNING"
        return state

    def get_on_time(self):
        tiempos = psutil.cpu_times()
        onTime = int(tiempos[2]/60/60)
        return onTime

    def get_users(self):
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

    def get_proc(self):
        cantProcess = len(self.tareas) - 5
        return cantProcess

    def get_proc_active(self):
        return self.cantProcessActive

    def get_proc_sleep(self):
        return self.cantProcessSleep

    def get_proc_per_user(self):
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

    def get_cpu_use(self):
        cpu_use = round(psutil.cpu_percent(),1)
        return cpu_use

    def get_mem_use(self):
        percentMem = psutil.virtual_memory()[2]
        return percentMem
