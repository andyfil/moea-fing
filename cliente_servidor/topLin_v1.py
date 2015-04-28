import os
import re
import time

import top

class TopLin_v1(top.Top):

    def __init__(self):
        print "Inciciando Top de linux"
        self.lineas = os.popen("/usr/bin/top -icbd.1 -n 1").readlines()
		self.firstLine = self.lineas[0].split(",")
        self.tokens = self.firstLine[0].split()
        self.secondLine = self.lineas[1].split(",")

    def _parse_memory(self):
        line = re.sub(r'\x1b[^m]*m', '', self.lineas[3])
        line = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', line)
        line = line.split(",")
        return line

    def get_total_memory(self):
        """Get total amount of RAM memory installed in the pc measured in MB"""
        line = self._parse_memory()
        tokens = line[0].split()
        mem_total = float(tokens[3][:-1])
        return mem_total

    def get_state(self):
        state = self.tokens[3]
        return state

    def get_on_time(self):
        with open('/proc/uptime', 'r') as time_file:
            uptime_seconds = float(time_file.readline().split()[0])
            return uptime_seconds / (60*60)

    def get_users(self):
        tokens = self.firstLine[2].split()
        cant_users = tokens[0]
        return cant_users

    def get_proc(self):
        tokens = self.secondLine[0].split()
        cant_process = int(tokens[1])
        return cant_process

    def get_proc_active(self):
        tokens = self.secondLine[1].split()
        cant_process_active = tokens[0]
        return cant_process_active

    def get_proc_sleep(self):
        tokens = self.secondLine[2].split()
        cant_process_sleep = tokens[0]
        return cant_process_sleep

    def get_proc_per_user(self):
        lineas_procesos = self.lineas[7:-1]
        diccionario = {}
        reg_user = re.compile(r'\d+\s(\w+)')
        for linea_proc in lineas_procesos:
            res = reg_user.findall(linea_proc.strip())
            user = res[0]
            if user in diccionario:
                diccionario[user] += 1
            else:
                diccionario[user] = 1
        return diccionario

    def get_cpu_use(self):
        cpu = re.sub(r'\x1b[^m]*m', '', self.lineas[2].strip())
        cpu = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', cpu)
        reg_cpu = re.compile(r'([0-9\.]){1,5}\sid')
        res = reg_cpu.findall(cpu)
        cpu_use = float(res[0])
        return cpu_use

    def get_mem_use(self):
        line = self._parse_memory()
        tokens = line[1].split()
        mem_used = float(tokens[0][:-1])
        mem_total = self.get_total_memory()
        return round((mem_used/mem_total)*100, 1)
