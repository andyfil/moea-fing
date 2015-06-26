#Revision number $Revision$

import json
import sys

import MySQLdb

from  dataHandler import DataHandler
import constantes as cts

def _armar_salon(fila):
    salon = {cts.SAL_ID: fila[0],
             cts.SAL_NOMBRE: fila[1],
             cts.SAL_LUGAR: fila[2],
             cts.SAL_PRIORITY: fila[3]}
    return salon

class BDHandler(DataHandler):
    """Clase que implementa a dataHandler,
    permite almacenar la informacion obtenida en base de datos"""

    host = cts.DB_HOST
    user = cts.DB_USER
    password = cts.DB_PASS
    database = cts.DB_DATABASE

    def __init__(self):
        super(BDHandler, self).__init__()
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

    def save_json(self, ident, jdata):
        query = """INSERT INTO %s (`id_pc`,`pc`,`timestamp`,`state`,`on_time`,\
            `users`,`process`, `process_active`,`process_sleep`, \
            `process_per_user`,`cpu_use`,`memory_use`) """ %cts.TABLE_REGISTRY
        query += "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        datos_query = (ident, jdata[cts.PC], jdata[cts.TIMESTAMP],
                       jdata[cts.STATE], jdata[cts.ON_TIME], jdata[cts.USERS],
                       jdata[cts.PROC], jdata[cts.PROC_ACTIVE],
                       jdata[cts.PROC_SLEEP], json.dumps(jdata[cts.PROC_PER_USER]),
                       jdata[cts.CPU_USE], jdata[cts.MEM_USE])
        self.execute(query, datos_query)


    def save_salon(self, jdata):
        "Metodo que agrega un salon a la estructura de datos"
        try:
            query = "INSERT INTO %s (`nombre`,`lugar`,`prioridad`) "\
            %cts.TABLE_SALON
            query += "VALUES(%s,%s,%s);"
            jdata[cts.SAL_PRIORITY] = 0
            datos_query = (jdata[cts.SAL_NOMBRE], jdata[cts.SAL_LUGAR],
                            jdata[cts.SAL_PRIORITY])
            self.execute(query, datos_query)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            self.db.rollback()

    def register_pc(self, jdata):
        """Metodo que registra una pc
        y devuelve el identificador de la misma"""
        ident = 0
        try:
            query = "SELECT id FROM %s " % cts.TABLE_PC
            query += "WHERE mac = %s"
            self.cursor.execute(query, jdata["mac"])
            datos = self.cursor.fetchone()
            if datos is None:
                query = "INSERT INTO %s " % cts.TABLE_PC
                query += "(`nombre`,`mac`,`so`,`ram`,`cpu`,`estado`,\
                           `ip`,`arq`)\
                           VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                data = (jdata[cts.REG_NOMBRE], jdata[cts.REG_MAC],
                        jdata[cts.REG_SO], jdata[cts.REG_RAM],
                        jdata[cts.REG_CPU], jdata[cts.REG_STATE],
                        jdata[cts.REG_IP], jdata[cts.REG_ARCH])
                self.cursor.execute(query, data)
                self.db.commit()
                ident = self.cursor.lastrowid
            else:
                ident = long(datos[0])
        except IndexError, ex_2:
            print "MySQL Error: %s" % str(ex_2)
            self.db.rollback()
        except AttributeError, ex_3:
            print ex_3
            self.db.rollback()
        except:
            print "Unexpected error:", sys.exc_info()[0]
            self.db.rollback()
        finally:
            return ident #en caso de error ident = 0

    def get_salon(self, jdata):
        "Metodo para obtener informacion de un salon"
        try:
            query = "SELECT id,nombre,lugar,prioridad FROM %s"% cts.TABLE_SALON
            where = ""
            if jdata is not None:
                if jdata[cts.SAL_ID] is not None:
                    where += "WHERE id = %s"% jdata[cts.SAL_ID]
                if jdata[cts.SAL_NOMBRE] is not None:
                    if where == "":
                        where = "WHERE"
                    else:
                        where += " and "
                    where += "id = %s"% jdata[cts.SAL_ID]
            query += where
            self.cursor.execute(query)
            datos = self.cursor.fetchall()
            return [_armar_salon(salon) for salon in datos]
        except:
            print "Error: no se pudo obtener datos de salon de la base de datos"


    def update_salon(self, jdata):
        "Metodo para actualizar la informacion de un salon"
        pass

    def save_user(self, jdata, ident):
        "Metodo que registra los datos de una sesion de usuario en la bd"
        query = """INSERT INTO %s (`pc_id`,`nombre`,`tiempo_ini`,`tiempo`,\
                        `memoria_minimo`,`memoria_promedio`,`memoria_maximo`,\
                        `cpu_minimo`,`cpu_promedio`,
                        `cpu_maximo`) """ % cts.TABLE_USER
        query += "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        datos_query = (ident, jdata[cts.U_NAME], jdata[cts.U_TIME_INI],
                       jdata[cts.U_TIME], jdata[cts.U_MEM_MIN],
                       jdata[cts.U_MEM_AVG], jdata[cts.U_MEM_MAX],
                       jdata[cts.U_PROC_MIN], jdata[cts.U_PROC_AVG],
                       jdata[cts.U_PROC_MAX])
        self.execute(query, datos_query)

    def save_proc(self, jdata, ident):
        query = """INSERT INTO %s (`pc_id`,`pid`,`user_id`,`name`,`tiempo_ini`,\
                    `tiempo`,`comando`,`memoria_minimo`,`memoria_promedio`,\
                    `memoria_maximo`,`cpu_minimo`,`cpu_promedio`,\
                    `cpu_maximo`) """ % cts.TABLE_PROC
        query += "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        datos_query = (ident, jdata[cts.P_ID], jdata[cts.P_USER], jdata[cts.P_NAME],
                       jdata[cts.P_TIME_INI], jdata[cts.P_TIME], jdata[cts.P_CMD],
                       jdata[cts.P_MEM_MIN], jdata[cts.P_MEM_AVG], jdata[cts.P_MEM_MAX],
                       jdata[cts.P_PROC_MIN], jdata[cts.P_PROC_AVG], jdata[cts.P_PROC_MAX])
        self.execute(query, datos_query)
