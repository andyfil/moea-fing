# Revision number $Revision: 164 $
# Date $Date: 2015-05-06 20:28:50 -0300 (Wed, 06 May 2015) $

import json


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
        j = {'nombre': self.nombre, 'tiempo_ini': self.tiempo_ini, 'tiempo': self.tiempo, 'memoria': self.memoria,
             'cpu': self.cpu}
        return json.dumps(j)

    @staticmethod
    def from_json(data):
        j_data = json.loads(data)
        name = j_data['nombre']
        tiempo = j_data['tiempo_ini']
        user = Usuario(name, tiempo)
        user.tiempo = j_data['tiempo']
        user.memoria = j_data['memoria']
        user.cpu = j_data['cpu']
        return user

    @property
    def memoria_max(self):
        """Devuelve el maximo valor de memoria"""
        return max(self.memoria)

    @property
    def cpu_max(self):
        """Devuelve el maximo valor de cpu"""
        return max(self.cpu)

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
        self.memoria = []
        self.cpu = []

    def reg_data(self, tiempo, memoria, cpu):
        self.tiempo = tiempo
        self.memoria.append(memoria)
        self.cpu.append(cpu)

    def update(self, process):
        self.tiempo = process.tiempo
        self.memoria.extend(process.memoria)
        self.cpu.extend(process.cpu)

    def to_json(self):
        j = {'pid': self.pid, 'name': self.name, 'user': self.user, 'tiempo_ini': self.tiempo_ini,
             'tiempo': self.tiempo, 'memoria': self.memoria, 'cpu': self.cpu, 'comando': self.comando}
        return json.dumps(j)

    @staticmethod
    def from_json(data):
        j_data = json.loads(data)
        proc = Proceso(j_data['pid'], j_data['name'], j_data['user'], j_data['tiempo_ini'],
                       j_data['comando'])
        proc.tiempo = j_data['tiempo']
        proc.memoria = j_data['memoria']
        proc.cpu = j_data['cpu']
        return proc

    @property
    def memoria_max(self):
        """Devuelve el maximo valor de memoria"""
        return max(self.memoria)

    @property
    def cpu_max(self):
        """Devuelve el maximo valor de cpu"""
        return max(self.cpu)

    def __str__(self):
        return self.comando


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
        return Proceso(self.pid, name, self.user, self.time, self.cmd)
