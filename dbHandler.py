import json
import sys

import MySQLdb

from  dataHandler import DataHandler
import constantes as cts

def _armar_salon(fila):
    salon = {}
    salon[cts.ident] = fila[0]
    salon[cts.nombre] = fila[1]
    salon[cts.lugar] = fila[2]
    salon[cts.prioridad] = fila[3]
    return salon

class BDHandler(DataHandler):
    """Clase que implementa a dataHandler,
    permite almacenar la informacion obtenida en base de datos"""

    host = cts.host
    user = cts.user
    password = cts.password
    database = cts.database

    def __init__(self):
        self.db = MySQLdb.connect(self.host, self.user, self.password,
                                  self.database)
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

    def execute(self, query, datos_query):
        try:
            self.cursor.execute(query,datos_query)
            self.db.commit()
        except MySQLdb.Error, exep:
            try:
                print "MySQL Error [%d]: %s" % (exep.args[0], exep.args[1])
            except IndexError, e2:
                print "MySQL Error: %s" % str(e2)
            except AttributeError, e3:
                print e3
            finally:
                self.db.rollback()
        except:
            print "Unexpected error:", sys.exc_info()[0]
            self.db.rollback()

    def save_json(self, jdata):
        query = """INSERT INTO %s (`pc`,`timestamp`,`state`,`on_time`,`users`,\
            `process`, `process_active`,`process_sleep`, `process_per_user`,\
            `cpu_use`,`memory_use`) """ %cts.tabla_registro
        query += "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        datos_query = (jdata[cts.pc], jdata[cts.timestamp], jdata[cts.state],
                       jdata[cts.on_time], jdata[cts.users], jdata[cts.process],
                       jdata[cts.process_active], jdata[cts.process_sleep],
                       json.dumps(jdata[cts.process_per_user]),
                       jdata[cts.cpu_use], jdata[cts.memory_use])
        self.execute(query, datos_query)


    def save_salon(self, jdata):
        "Metodo que agrega un salon a la estructura de datos"
        query = "INSERT INTO %s (`nombre`,`lugar`,`prioridad`) "\
         %cts.tabla_salon
        query += "VALUES(%s,%s,%s);"
        jdata[cts.prioridad] = 0
        datos_query = (jdata[cts.nombre], jdata[cts.lugar], jdata[cts.prioridad])
        self.execute(query, datos_query)

    def register_pc(self, jdata):
        """Metodo que registra una pc
        y devuelve el identificador de la misma"""
        try:
            ident = 0
            query = "SELECT id FROM %s WHERE mac = %s "% cts.tabla_pc, "%s"
            self.cursor.execute(query,(jdata["mac"]))
            datos = self.cursor.fetchone()
            if datos is None:
                query = "INSERT INTO %s " % cts.tabla_pc
                query += "(`nombre`,`mac`,`so`,`ram`,`cpu`,`estado`,\
                    `cant_usuarios`,`salon_id`) VALUES "
                query += "%s,%s,%s,%s,%s,%s,%s,%s"
                data = (jdata[cts.reg_nombre], jdata[cts.reg_mac], \
                    jdata[cts.reg_so], jdata[cts.reg_ram], jdata[cts.reg_cpu],\
                     jdata[cts.reg_estado], jdata[cts.reg_users], \
                     jdata[cts.reg_salon])
                self.cursor.execute(query, data)
                self.db.commit()
                ident = self.db.insert_id()
            else:
                ident = datos[cts.ident]
            return ident
        except:
            print "Error: no se pudo registrar la pc"
            self.db.rollback()

    def get_salon(self, jdata):
        "Metodo para obtener informacion de un salon"
        try:
            query = "SELECT id,nombre,lugar,prioridad FROM %s"% cts.tabla_salon
            if jdata is not None:
                where = ""
                if jdata[cts.ident] is not None:
                    where += "WHERE id = %s"% jdata[cts.ident]
                if jdata[cts.nombre] is not None:
                    if where == "":
                        where = "WHERE"
                    else:
                        where += " and "
                    where += "id = %s"% jdata[cts.ident]
            query += where
            self.cursor.execute(query)
            datos = self.cursor.fetchall()
            return [_armar_salon(salon) for salon in datos]
        except:
            print "Error: no se pudo obtener datos de salon de la base de datos"


    def update_salon(self, jdata):
        "Metodo para actualizar la informacion de un salon"
        pass
