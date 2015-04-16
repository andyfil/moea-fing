import sys
import os
if os.name == "posix":
    print "SO: LINUX"
    from topLin_v1 import TopLin_v1
    TOP = TopLin_v1()
else: #nt
    print "SO: WINDOWS"
    from topWin_v1 import TopWin_v1
    TOP = TopWin_v1()

from json import dumps
import requests
import constantes as cts
#import topLin_v1 as top

IDENT = 1 #id de la pc por defecto
BASE_URL = "http://fingproy.cloudapp.net:80/proy/api/v1"
REGISTER_URL = BASE_URL + "/pcs"
DATA_URL = BASE_URL + "/pcs"
#PROXY = "http://proxy.fing.edu.uy"
PROXY = ""
PROXY_PORT = 3128
MESSAGE = '{"pc": "pcunix114","timestamp": "2014-12-10 10:48:20",\
          "state": "working","on_time": 1238.3,"users": 3,"process": 98,\
          "process_active": 5,"process_sleep": 93,"process_per_user":[10,2,4],\
          "cpu_use": 34.2,"memory_use": 45.0}'#Mensaje JSON de prueba

def data_registro():
    reg = {}
    reg[cts.reg_nombre] = TOP.get_pc_name()
    reg[cts.reg_mac] = TOP.get_mac()
    reg[cts.reg_so] = TOP.get_os()
    reg[cts.reg_ram] = TOP.get_total_memory()
    reg[cts.reg_arch] = TOP.get_cpu_architecture()
    reg[cts.reg_cpu] = TOP.get_cpu_cores()
    reg[cts.reg_estado] = TOP.obtenerState()
    reg[cts.reg_ip] = TOP.get_ip()
    return reg

def proxi():
    if PROXY:
        return {"http":PROXY +':'+ str(PROXY_PORT)}
    else:
        return {}

if __name__ == '__main__':
    try:
        HEADERS = {'content-type': 'application/json'}
        R = requests.post(REGISTER_URL, data=dumps(data_registro()),
                          headers=HEADERS, proxies=proxi())
        if R.status_code == 200 and R.json()['result']:
            URL = DATA_URL+"/"+str(R.json()['ident'])
            R2 = requests.post(URL, data=dumps(TOP.obtener_datos()),
                               headers=HEADERS, proxies=proxi())
        else:
            print "Ocurrio un error al intentar registrar la pc "
            print R.json()
    except:
        print "Error inesperado:", sys.exc_info()
    finally:
        print >>sys.stderr, 'Cerrando socket'

