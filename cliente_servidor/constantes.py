# datos conexion BD
DB_HOST = 'fingproy.cloudapp.net'
DB_USER = 'user'
DB_PASS = 'user'
DB_DATABASE = 'web'

#respuestas api rest
API_RESULT = 'result'
API_ID = 'id'

#constantes de nombre json
#dato PC
PC = 'pc'
TIMESTAMP = 'timestamp'
STATE = 'state'
ON_TIME = 'on_time'
USERS = 'users'
PROC = 'process'
PROC_ACTIVE = 'process_active'
PROC_SLEEP = 'process_sleep'
PROC_PER_USER = 'process_per_user'
CPU_USE = 'cpu_use'
MEM_USE = 'memory_use'

#pc registro
REG_NOMBRE = 'nombre'
REG_MAC = 'mac'
REG_SO = 'so'
REG_RAM = 'ram'
REG_CPU = 'cpu'
REG_IP = 'ip'
REG_STATE = 'estado'
REG_USERS = 'cant_usuarios'
REG_SALON = 'salon_id'
REG_ARCH = 'cpu_arch'

#dato salon
SAL_ID = 'id'
SAL_NOMBRE = 'Nombre'
SAL_LUGAR = 'Ubicacion'
SAL_PRIORITY = 'Prioridad'
SAL_CANT = 'Cantidad'

#datos usuario
U_NAME = 'name'
U_TIME_INI = 'tiempo_ini'
U_TIME = 'tiempo'
U_MEM = 'memoria'
U_MEM_MIN = 'mem_min'
U_MEM_AVG = 'mem_avg'
U_MEM_MAX = 'mem_max'
U_PROC = 'cpu'
U_PROC_MIN = 'proc_min'
U_PROC_AVG = 'proc_avg'
U_PROC_MAX = 'proc_max'

#datos procesos
P_ID = 'pid'
P_NAME = 'name'
P_USER = 'user'
P_TIME_INI = 'tiempo_ini'
P_TIME = 'tiempo'
P_CMD = 'cmd'
P_MEM = 'memoria'
P_MEM_MIN = 'mem_min'
P_MEM_AVG = 'mem_avg'
P_MEM_MAX = 'mem_max'
P_CPU = 'cpu'
P_PROC_MIN = 'proc_min'
P_PROC_AVG = 'proc_avg'
P_PROC_MAX = 'proc_max'
P_MEDIDAS = 'medidas'

#constantes de columnas tablas BD


#constantes de nombre de tabla BD
TABLE_SALON = 'maquinas_salon'
TABLE_PC = 'maquinas_pc'
TABLE_REGISTRY = 'datos'
TABLE_PROC = 'maquinas_proceso'
TABLE_USER = 'maquinas_usuario'

#errors
ERR_REG_PC = 1

#config
CFG_FILE = 'config.cfg'
CFG_SECT = 'main' #config section
CFG_SECT_USER = 'user'
CFG_SECT_PROC = 'proc'
CFG_ID = 'id' #id of the pc on the system
CFG_DIR = 'configs/'
