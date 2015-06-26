#Revision number $Revision$

import time
import ConfigParser as Config
import os
import requests as rq
from json import dumps
import sys

from modelo import Usuario, Proceso
from cliente_v1 import register
import constantes as cts


if os.name == "posix":
    #print "SO: LINUX"
    from topLin_v1 import TopLin_v1

    _top = TopLin_v1()
else:  #nt
    #print "SO: WINDOWS"
    from topWin_v1 import TopWin_v1

    _top = TopWin_v1()

CFG_NAME = cts.CFG_DIR + _top.get_pc_name() + '.cfg'
PROXY = "http://proxy.fing.edu.uy"
#PROXY = ""
PROXY_PORT = 3128
BASE_URL = "http://fingproy.cloudapp.net:80/proy/api/v1"
HEADERS = {'content-type': 'application/json'}
MIN_TIEMPO_EJECUCION = 0
IDENT = ''

cfg = Config.RawConfigParser()

class Datos:
    user_bd = []
    proc_bd = []

datos = Datos()

def read_from_file(section):
    """Funcion que lee de un archivo de configuracion una seccion y devuelve
        la lista de json en la misma"""
    return [cfg.get(section, i) for i in cfg.options(section)]


def init():
    if not os.path.exists(cts.CFG_DIR):
        os.makedirs(cts.CFG_DIR)
    IDENT = register()
    result = cfg.read(CFG_NAME)
    if not result:
        with open(CFG_NAME, 'wb') as config_file:
            cfg.add_section(cts.CFG_SECT_USER)
            cfg.add_section(cts.CFG_SECT_PROC)
            cfg.write(config_file)
    else:
        if not cfg.has_section(cts.CFG_SECT_PROC):
            cfg.add_section(cts.CFG_SECT_PROC)
        if not cfg.has_section(cts.CFG_SECT_USER):
            cfg.add_section(cts.CFG_SECT_USER)
        datos.user_bd = [Usuario.from_json(i) for i in
                    read_from_file(cts.CFG_SECT_USER)]
        datos.proc_bd = [Proceso.from_json(i) for i in
                    read_from_file(cts.CFG_SECT_PROC)]

def _proxi():
    if PROXY:
        return {"http":PROXY +':'+ str(PROXY_PORT)}
    else:
        return {}

def close():
    """Actualiza la informacion en el archivo,
        asume que el archivo de config y la lista estan sincronizadas"""
    for u_iter in datos.user_bd:
        cfg.set(cts.CFG_SECT_USER, u_iter.nombre, u_iter.to_str())
    for p_iter in datos.proc_bd:
        cfg.set(cts.CFG_SECT_PROC, str(p_iter.pid), p_iter.to_str())
    with open(CFG_NAME, 'wb') as config_file:
        cfg.write(config_file)


def report_proc(p_proc):
    """Proceso que registra en la API rest el proceso una vez que terminio,
        y luego borra de la bd local"""
    cfg.remove_option(cts.CFG_SECT_PROC, str(p_proc.pid))
    url = BASE_URL + '/procs/' + IDENT
    data = p_proc.to_json()
    data[cts.U_PROC_MIN] = p_proc.cpu_min
    data[cts.U_PROC_MAX] = p_proc.cpu_max
    data[cts.U_PROC_AVG] = p_proc.cpu_avg
    data[cts.U_MEM_MIN] = p_proc.memoria_min
    data[cts.U_MEM_MAX] = p_proc.memoria_max
    data[cts.U_MEM_AVG] = p_proc.memoria_avg
    del data[cts.P_CPU]
    del data[cts.P_MEM]
    result = rq.post(url, data=dumps(data), headers=HEADERS, proxies=_proxi())
    if result.status_code != 200:
        print result


def report_user(p_user):
    """Proceso que registra en la API rest el usuario
        una vez que cierra sesion, y luego borra de la bd local"""
    cfg.remove_option(cts.CFG_SECT_USER, user.nombre)
    url = BASE_URL + '/users/' + IDENT
    data = p_user.to_json()
    data[cts.U_PROC_MIN] = p_user.cpu_min
    data[cts.U_PROC_MAX] = p_user.cpu_max
    data[cts.U_PROC_AVG] = p_user.cpu_avg
    data[cts.U_MEM_MIN] = p_user.memoria_min
    data[cts.U_MEM_MAX] = p_user.memoria_max
    data[cts.U_MEM_AVG] = p_user.memoria_avg
    del data[cts.P_CPU]
    del data[cts.P_MEM]
    result = rq.post(url, data=dumps(data), headers=HEADERS, proxies=_proxi())
    if result.status_code != 200:
        print result



def add_user(p_user):
    cfg.set(cts.CFG_SECT_USER, p_user.nombre, p_user.to_str())
    datos.user_bd.append(p_user)


def add_proc(p_proc):
    cfg.set(cts.CFG_SECT_PROC, str(p_proc.pid), p_proc.to_str())
    datos.proc_bd.append(p_proc)


if __name__ == '__main__':
    try:
        contador = 0
        init()
        user_list = []
        proc_list = []
        while contador < 3:
            user_list = _top.get_users_data()
            proc_list = _top.get_process_data()
            # TODO falta actualizar la info de cpu y memoria
            #prcesos
            for proc in datos.proc_bd:
                p = next((x for x in proc_list if x.pid == proc.pid), None)
                if p is None:  #El proceso proc termino su ejecucion
                    report_proc(proc)
                    datos.proc_bd.remove(proc)
                else:  #El proceso sigue ejecutando
                    proc.update(p)
                    proc_list.remove(p)
            for proc in proc_list:  #Los procesos nuevos
                if(proc.user != 'root' and proc.user != 'martin.+' and
                   proc.user != 'daniel.+'):
                    add_proc(proc)
            #usuarios
            for user in datos.user_bd:
                u = next((x for x in user_list if x.nombre == user.nombre), None)
                if u is None:  #El usuario user termino su sesion
                    report_user(user)
                    datos.user_bd.remove(user)
                else:  #El usuario sigue logeado
                    user.update(u)
                    user_list.remove(u)
            for user in user_list:  #Los usuarios nuevos
                if user.nombre != 'root':
                    add_user(user)
            time.sleep(15)
            contador += 1
        close()
    except:
        print IDENT, " Excepcion " + sys.exc_info()
