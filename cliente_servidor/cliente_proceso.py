#Revision number $Revision: 164 $
#Date $Date: 2015-05-06 20:28:50 -0300 (Wed, 06 May 2015) $

import time

from modelo import Usuario, Proceso
import topWin_v1
import topLin_v1
import os


if os.name == "posix":
    #print "SO: LINUX"
    from topLin_v1 import TopLin_v1
    _top = TopLin_v1()
else: #nt
    #print "SO: WINDOWS"
    from topWin_v1 import TopWin_v1
    _top = TopWin_v1()

_user_bd = _top.get_users_data()
_proc_bd = _top.get_process_data()



def report_proc(p_process):
    """Proceso que registra en la API rest el proceso una vez que terminio"""
    print p_process.pid, p_process.comando

def report_user(p_user):
    """Proceso que registra en la API rest el usuario
        una vez que cierra sesion"""
    print p_user.nombre

if __name__ == '__main__':
    i = 0
    while i < 100:
        user_list = _top.get_users_data()
        proc_list = _top.get_process_data()
        #prcesos
        for proc in _proc_bd:
            p = next((x for x in proc_list if x.pid == proc.pid), None)
            if p is None: #El proceso proc termino su ejecucion
                report_proc(proc)
                _proc_bd.remove(proc)
            else: #El proceso sigue ejecutando
                proc.update(p)
                proc_list.remove(p)
        for proc in proc_list: #Los procesos nuevos
            _proc_bd.append(proc)
        #usuarios
        for user in _user_bd:
            u = next((x for x in user_list if x.nombre == user.nombre), None)
            if u is None: #El usuario user termino su sesion
                report_user(user)
                _user_bd.remove(user)
            else: #El usuario sigue logeado
                user.update(u)
                user_list.remove(u)
        for user in user_list: #Los usuarios nuevos
            _user_bd.append(user)
        time.sleep(5)
        i += 1
