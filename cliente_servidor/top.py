from abc import ABCMeta, abstractmethod
from platform import node, processor, system
from uuid import getnode as get_mac
from socket import gethostbyname, getfqdn
from multiprocessing import cpu_count
from time import strftime

import constantes as cs

class Top():
    __metaclass__ = ABCMeta

    def obtener_datos(self):
        data = {cs.PC: self.get_pc_name(),
                cs.TIMESTAMP: self.get_timestamp(),
                cs.STATE: self.get_state(),
                cs.ON_TIME: self.get_on_time(),
                cs.USERS: self.get_users(),
                cs.PROC: self.get_proc(),
                cs.PROC_ACTIVE: self.get_proc_active(),
                cs.PROC_SLEEP: self.get_proc_sleep(),
                cs.PROC_PER_USER: self.get_proc_per_user(),
                cs.CPU_USE: self.get_cpu_use(),
                cs.MEM_USE: self.get_mem_use()}
        return data

    def get_os(self):
        "Get the host operative system family"
        return system()

    def get_timestamp(self):
        "Obtengo fecha y hora"
        return strftime("%Y-%m-%d %H:%M:%S")

    def get_ip(self):
        """Get the ip assigned to external network interface"""
        return gethostbyname(getfqdn())

    def get_pc_name(self):
        """Devuelve el nombre de la pc"""
        return node()

    def get_mac(self):
        """Get the mac address of the pc"""
        return str(get_mac())

    def get_cpu_architecture(self):
        """Get the brand and model of the cpu"""
        return processor()

    def get_cpu_cores(self):
        """Get the number of cpu cores in the pc"""
        return cpu_count()

    @abstractmethod
    def get_total_memory(self):
        """Get total amount of RAM memory installed in the pc measured in MB"""
        pass

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_state(self):
        "Obtengo el estado de la pc"
        pass

    @abstractmethod
    def get_on_time(self):
        "Obtengo tiempo iniciada"
        pass

    @abstractmethod
    def get_users(self):
        "Obtengo cantidad de usuarios"
        pass

    @abstractmethod
    def get_proc(self):
        "Obtengo cantidad de procesos"
        pass

    @abstractmethod
    def get_proc_active(self):
        "Obtengo cantidad de procesos activos"
        pass

    @abstractmethod
    def get_proc_sleep(self):
        "Obtengo cantidad de procesos dormidos"
        pass

    @abstractmethod
    def get_proc_per_user(self):
        "Obtengo procesos por usuario"
        pass

    @abstractmethod
    def get_cpu_use(self):
        "Obtengo porcentaje de uso cpu"
        pass

    @abstractmethod
    def get_mem_use(self):
        "Obtengo porcentaje de uso de memoria"
        pass
