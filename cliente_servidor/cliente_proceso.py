# Revision number $Revision: 164 $
#Date $Date: 2015-05-06 20:28:50 -0300 (Wed, 06 May 2015) $

import time
import ConfigParser as Config
import os

from modelo import Usuario, Proceso
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

cfg = Config.RawConfigParser()
_user_bd = []
_proc_bd = []


def read_from_file(section):
    """Funcion que lee de un archivo de configuracion una seccion y devuelve
        la lista de json en la misma"""
    return [cfg.get(section, i) for i in cfg.options(section)]


def init():
    if not os.path.exists(cts.CFG_DIR):
        os.makedirs(cts.CFG_DIR)
    result = cfg.read(CFG_NAME)
    if not result:
        with open(CFG_NAME, 'wb') as config_file:
            cfg.add_section(cts.CFG_SECT_USER)
            cfg.add_section(cts.CFG_SECT_PROC)
            cfg.write(config_file)
    else:
        _user_bd = [Usuario.from_json(i) for i in
                    read_from_file(cts.CFG_SECT_USER)]
        _proc_bd = [Proceso.from_json(i) for i in
                    read_from_file(cts.CFG_SECT_PROC)]


def close():
    """Actualiza la informacion en el archivo,
        asume que el archivo de config y la lista estan sincronizadas"""
    for user in _user_bd:
        cfg.set(cts.CFG_SECT_USER, user.nombre, user.to_json())
    for proc in _proc_bd:
        cfg.set(cts.CFG_SECT_PROC, str(proc.pid), proc.to_json())
    with open(CFG_NAME, 'wb') as config_file:
        cfg.write(config_file)


def report_proc(proc):
    """Proceso que registra en la API rest el proceso una vez que terminio,
        y luego borra de la bd local"""
    print proc.pid, proc.comando
    cfg.remove_option(cts.CFG_SECT_PROC, str(proc.pid))


def report_user(user):
    """Proceso que registra en la API rest el usuario
        una vez que cierra sesion, y luego borra de la bd local"""
    print user.nombre
    cfg.remove_option(cts.CFG_SECT_USER, user.nombre)


def add_user(user):
    cfg.set(cts.CFG_SECT_USER, user.nombre, user.to_json())
    _user_bd.append(user)


def add_proc(proc):
    cfg.set(cts.CFG_SECT_PROC, str(proc.pid), proc.to_json())
    _proc_bd.append(proc)


if __name__ == '__main__':
    contador = 0
    init()
    user_list = []
    proc_list = []
    while contador < 5:
        user_list = _top.get_users_data()
        proc_list = _top.get_process_data()
        # TODO falta actualizar la info de cpu y memoria
        #prcesos
        for proc in _proc_bd:
            p = next((x for x in proc_list if x.pid == proc.pid), None)
            if p is None:  #El proceso proc termino su ejecucion
                report_proc(proc)
                _proc_bd.remove(proc)
            else:  #El proceso sigue ejecutando
                proc.update(p)
                proc_list.remove(p)
        for proc in proc_list:  #Los procesos nuevos
            add_proc(proc)
        #usuarios
        for user in _user_bd:
            u = next((x for x in user_list if x.nombre == user.nombre), None)
            if u is None:  #El usuario user termino su sesion
                report_user(user)
                _user_bd.remove(user)
            else:  #El usuario sigue logeado
                user.update(u)
                user_list.remove(u)
        for user in user_list:  #Los usuarios nuevos
            add_user(user)
        time.sleep(2)
        contador += 1
    close()
