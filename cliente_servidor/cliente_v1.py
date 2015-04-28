import sys
import os
from json import dumps
import requests as rq
import ConfigParser as config

import constantes as cts
if os.name == "posix":
    print "SO: LINUX"
    from topLin_v1 import TopLin_v1
    TOP = TopLin_v1()
else: #nt
    print "SO: WINDOWS"
    from topWin_v1 import TopWin_v1
    TOP = TopWin_v1()
IDENT = 1 #id de la pc por defecto
BASE_URL = "http://fingproy.cloudapp.net:80/proy/api/v1"
REGISTER_URL = BASE_URL + "/pcs"
DATA_URL = BASE_URL + "/pcs"
HEADERS = {'content-type': 'application/json'}
PROXY = "http://proxy.fing.edu.uy"
#PROXY = ""
PROXY_PORT = 3128
MESSAGE = '{"pc": "pcunix114","timestamp": "2014-12-10 10:48:20",\
          "state": "working","on_time": 1238.3,"users": 3,"process": 98,\
          "process_active": 5,"process_sleep": 93,"process_per_user":[10,2,4],\
          "cpu_use": 34.2,"memory_use": 45.0}'#Mensaje JSON de prueba

def _save_id(p_ident):
    with open(cts.CFG_FILE, 'wb') as config_file:
        _cfg = config.RawConfigParser()
        _cfg.add_section(cts.CFG_SECT)
        _cfg.set(cts.CFG_SECT, cts.CFG_ID, p_ident)
        _cfg.write(config_file)

def data_registro():
    reg = {}
    reg[cts.REG_NOMBRE] = TOP.get_pc_name()
    reg[cts.REG_MAC] = TOP.get_mac()
    reg[cts.REG_SO] = TOP.get_os()
    reg[cts.REG_RAM] = TOP.get_total_memory()
    reg[cts.REG_ARCH] = TOP.get_cpu_architecture()
    reg[cts.REG_CPU] = TOP.get_cpu_cores()
    reg[cts.REG_STATE] = TOP.get_state()
    reg[cts.REG_IP] = TOP.get_ip()
    return reg

def _proxi():
    if PROXY:
        return {"http":PROXY +':'+ str(PROXY_PORT)}
    else:
        return {}

if __name__ == '__main__':
    try:
        cfg = config.RawConfigParser()
        cfg_file = cfg.read(cts.CFG_FILE)
        ident = ''
        if cfg_file == []:
            r = rq.post(REGISTER_URL, data=dumps(data_registro()),
                        headers=HEADERS, proxies=_proxi())
            if r.status_code == 200 and bool(r.json()[cts.API_RESULT]):
                ident = str(r.json()[cts.API_ID])
                _save_id(ident)
            else:
                print "Error registering pc ", r.json()
                sys.exit(cts.ERR_REG_PC)
        else:
            ident = cfg.get(cts.CFG_SECT,cts.CFG_ID)
        URL = DATA_URL+"/"+ ident
        j = TOP.obtener_datos()
	R2 = rq.post(URL, data=dumps(j),
                     headers=HEADERS, proxies=_proxi())
        print "Exito"
    except:
        print "Error inesperado:", sys.exc_info()
