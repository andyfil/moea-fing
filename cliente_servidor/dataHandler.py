from abc import ABCMeta, abstractmethod

class DataHandler():
    """Clase que define los metodos a implementar
    por las clases que administren el acceso a los datos"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass
    @abstractmethod
    def __del__(self):
        pass

    @abstractmethod
    def save_json(self, jdata):
        "Metodo que procesa un registro en formato json y lo almacena"
        pass

#begin Salon
    @abstractmethod
    def save_salon(self, jdata):
        "Metodo que agrega un salon a la estructura de datos"
        pass

    @abstractmethod
    def get_salon(self, jdata):
        "Metodo para obtener informacion de un salon"

    @abstractmethod
    def update_salon(self, jdata):
        "Metodo para actualizar la informacion de un salon"
#end Salon

    @abstractmethod
    def register_pc(self, jdata):
        "Metodo que registra una pc y devuelve el identificador de la misma"
        pass

