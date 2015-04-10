import os
if (os.name == "posix"):
    print "SO: LINUX"
    from topLin_v1 import TopLin_v1
    top = TopLin_v1()
else: #nt
    print "SO: WINDOWS"
    from topWin_v1 import TopWin_v1
    top = TopWin_v1()

import sys
import requests
#import topLin_v1 as top

IDENT = 1 #id de la pc por defecto
REGISTER_URL = "http://fingproy.cloudapp.net:80/proy/api/v1/pcs"
BASE_URL = "http://fingproy.cloudapp.net:80/proy/api/v1/pcs/"
#PROXY = "http://proxy.fing.edu.uy"
PROXY = ""
PROXY_PORT = 3128
MESSAGE = '{"pc": "pcunix114","timestamp": "2014-12-10 10:48:20",\
          "state": "working","on_time": 1238.3,"users": 3,"process": 98,\
          "process_active": 5,"process_sleep": 93,"process_per_user":[10,2,4],\
          "cpu_use": 34.2,"memory_use": 45.0}'#Mensaje JSON de prueba


def funcion_top():
    return top.obtener_datos(top)

def proxi():
    if PROXY:
        return {"http":PROXY +':'+ str(PROXY_PORT)}
    else:
        return {}
try:
    URL = BASE_URL + str(id)
    HEADERS = {'content-type': 'application/json'}
    requests.post(REGISTER_URL, )
    print requests.post(URL, data=funcion_top(),
                        headers=HEADERS, proxies=proxi())
except:
    print "Error inesperado:", sys.exc_info()
finally:
    print >>sys.stderr, 'Cerrando socket'

