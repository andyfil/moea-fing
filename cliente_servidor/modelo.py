#Revision number $Revision$

import json
import constantes as ct
import time


class Usuario(object):
    """Objeto que almacena la informacion sobre un usuario"""

    def __init__(self, nombre, tiempo):
        self.nombre = nombre
        self.tiempo_ini = tiempo
        self.tiempo = tiempo
        self.memoria = []
        self.cpu = []

    def reg_data(self, tiempo, memoria, cpu):
        self.tiempo = tiempo
        self.memoria.append(memoria)
        self.cpu.append(cpu)

    def update(self, user):
        self.tiempo = user.tiempo
        self.memoria.extend(user.memoria)
        self.cpu.extend(user.cpu)

    def to_json(self):
        return {ct.U_NAME: self.nombre, ct.U_TIME_INI: self.tiempo_ini,
                ct.U_TIME: self.tiempo, ct.U_MEM: self.memoria, ct.U_PROC: self.cpu}

    def to_str(self):
        return json.dumps(self.to_json())

    @staticmethod
    def from_json(data):
        j_data = json.loads(data)
        name = j_data[ct.U_NAME]
        tiempo = j_data[ct.U_TIME_INI]
        user = Usuario(name, tiempo)
        user.tiempo = j_data[ct.U_TIME]
        user.memoria = j_data['memoria']
        user.cpu = j_data['cpu']
        return user

    @property
    def memoria_max(self):
        """Devuelve el maximo valor de memoria"""
        if not self.memoria:
            return 0
        else:
            return max(self.memoria)

    @property
    def memoria_min(self):
        """Devuelve el minimo valor de memoria"""
        if not self.memoria:
            return 0
        else:
            return min(self.memoria)

    @property
    def memoria_avg(self):
        "Devuelve el valor promedio de memoria"
        if not self.memoria:
            return 0
        else:
            return sum(self.memoria)/float(len(self.memoria))

    @property
    def cpu_max(self):
        """Devuelve el maximo valor de cpu"""
        if not self.cpu:
            return 0
        else:
            return max(self.cpu)

    @property
    def cpu_min(self):
        """Devuelve el minimo valor de cpu"""
        if not self.cpu:
            return 0
        else:
            return min(self.cpu)

    @property
    def cpu_avg(self):
        """Devuelve el valor promedio de cpu"""
        if not self.cpu:
            return 0
        else:
            return sum(self.cpu)/float(len(self.cpu))

    @property
    def tiempo_total(self):
        """Devuelve el tiempo transucrido entre tiempo_ini y tiempo"""
        return self.tiempo - self.tiempo_ini

    def __str__(self):
        return self.nombre


class Proceso(object):
    """Objeto que almacena la informacion sobre un proceso"""

    def __init__(self, pid, name, user, tiempo, comando):
        self.pid = pid
        self.name = name
        self.user = user
        self.tiempo_ini = tiempo
        self.tiempo = tiempo
        self.comando = comando
        self.medidas = 0
        self.mem_min = 100
        self.mem_max = 0
        self.mem_avg = 0
        self._cpu_min = 100
        self._cpu_max = 0
        self._cpu_avg = 0

    def reg_data(self, tiempo, memoria, cpu):
        self.tiempo = tiempo
        self.mem_avg = self.mem_avg*self.medidas / (self.medidas +1) + memoria/(self.medidas +1)
        self._cpu_avg = self._cpu_avg*self.medidas / (self.medidas +1) + cpu/(self.medidas +1)
        self.mem_min = min(self.mem_min, memoria)
        self.mem_max = max(self.mem_max, memoria)
        self._cpu_min = min(self._cpu_min, cpu)
        self._cpu_max = max(self._cpu_max, cpu)
        self.medidas += 1

    def update(self, process):
        self.tiempo = process.tiempo
        self.mem_min = min(self.mem_min, process.mem_min)
        self.mem_max = max(self.mem_max, process.mem_max)
        self.mem_avg = (self.medidas*self.mem_avg + process.medidas*process.mem_avg)/(self.medidas + process.medidas)
        self._cpu_min = min(self._cpu_min, process._cpu_min)
        self._cpu_max = max(self._cpu_max, process._cpu_max)
        self._cpu_avg = (self.medidas*self._cpu_avg + process.medidas*process._cpu_avg)/(self.medidas + process.medidas)
        self.medidas += process.medidas

    def to_json(self):
        return {ct.P_ID: self.pid, ct.P_NAME: self.name, ct.P_USER: self.user,
                ct.P_TIME_INI: self.tiempo_ini, ct.P_TIME: self.tiempo,
                ct.P_MEM_MIN: self.mem_min, ct.P_MEM_MAX: self.mem_max, ct.P_MEM_AVG: self.mem_avg, 
                ct.P_PROC_MIN: self._cpu_min, ct.P_PROC_MAX: self._cpu_max, ct.P_PROC_AVG: self._cpu_avg, 
                ct.P_CMD: self.comando, ct.P_MEDIDAS: self.medidas}

    def to_str(self):
        return json.dumps(self.to_json())

    @staticmethod
    def from_json(data):
        j_data = json.loads(data)
        proc = Proceso(j_data[ct.P_ID], j_data[ct.P_NAME], j_data[ct.P_USER],
                       j_data[ct.P_TIME_INI], j_data[ct.P_CMD])
        proc.tiempo = j_data[ct.P_TIME]
        proc.medidas = j_data[ct.P_MEDIDAS]
        proc.mem_min = j_data[ct.P_MEM_MIN]
        proc.mem_avg = j_data[ct.P_MEM_AVG]
        proc.mem_max = j_data[ct.P_MEM_MAX]
        proc._cpu_min = j_data[ct.P_PROC_MIN]
        proc._cpu_avg = j_data[ct.P_PROC_AVG]
        proc._cpu_max = j_data[ct.P_PROC_MAX]
        return proc

    @property
    def memoria_max(self):
        """Devuelve el maximo valor de memoria"""
        return self.mem_max

    @property
    def memoria_min(self):
        """Devuelve el minimo valor de memoria"""
        return self.mem_min

    @property
    def memoria_avg(self):
        "Devuelve el valor promedio de memoria"
        return self.mem_avg

    @property
    def cpu_max(self):
        """Devuelve el maximo valor de cpu"""
        return self._cpu_max

    @property
    def cpu_min(self):
        """Devuelve el minimo valor de cpu"""
        return self._cpu_min

    @property
    def cpu_avg(self):
        """Devuelve el valor promedio de cpu"""
        return self._cpu_avg

    @property
    def tiempo_total(self):
        """Devuelve el tiempo transucrido entre tiempo_ini y tiempo"""
        return self.tiempo - self.tiempo_ini

    def __str__(self):
        return self.pid, self.name


class Proc(object):
    ''' Data structure for a processes . The class properties are
    process attributes '''

    def __init__(self, proc_info):
        self.user = proc_info[0]
        self.pid = proc_info[1]
        self.cpu = proc_info[2]
        self.mem = proc_info[3]
        self.vsz = proc_info[4]
        self.rss = proc_info[5]
        self.tty = proc_info[6]
        self.stat = proc_info[7]
        self.start = proc_info[8]
        self.time = proc_info[9]
        self.cmd = proc_info[10]

    def to_str(self):
        ''' Returns a string containing minimalistic info
        about the process : user, pid, and command '''
        return '%s %s %s' % (self.user, self.pid, self.cmd)

    def __str__(self):
        return '%s %s %s' % (self.pid, self.user, self.cmd)

    def get_proceso(self):
        max_len = 8 if len(self.cmd) > 8 else len(self.cmd)
        name = self.cmd[0:max_len]
        proc = Proceso(self.pid, name, self.user, time.time(), self.cmd)
        proc.reg_data(time.time(), float(self.mem), float(self.cpu))
        return proc
