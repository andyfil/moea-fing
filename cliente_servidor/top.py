from abc import ABCMeta, abstractmethod

class Top():
    __metaclass__ = ABCMeta

    def obtener_datos(self):
        data = {}
        data['pc'] = self.obtenerPc()
        data['timestamp'] = self.obtenerTimestamp()
        data['state'] = self.obtenerState()
        data['on_time'] = self.obtenerOn_time()
        data['users'] = self.obtenerUsers()
        data['process'] = self.obtenerProcess()
        data['process_active'] = self.obtenerProcess_active()
        data['process_sleep'] = self.obtenerProcess_sleep()
        data['process_per_user'] = self.obtenerProcess_per_user()
        data['cpu_use'] = self.obtenerCpu_use()
        data['memory_use'] = self.obtenerMemory_use()
        return data

    @abstractmethod
    def get_cpu_architecture(self):
        """Get the brand and model of the cpu"""
        pass

    @abstractmethod
    def get_cpu_cores(self):
        """Get the number of cpu cores in the pc"""
        pass

    @abstractmethod
    def get_total_memory(self):
        """Get total amount of RAM memory installed in the pc measured in MB"""
        pass

    @abstractmethod
    def __init__(self):
        pass

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
    def obtenerProcess_sleep(self):
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
    def obtenerMemory_use(self):
        "Obtengo porcentaje de uso de memoria"
        pass
