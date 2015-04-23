#Revision number $Revision$
#Date $Date$

import dataHandler
import os
import json

class FileHandler(dataHandler.DataHandler):
	"""Clase que permite almacenar la informacion capturada en un archivo csv"""

	def __init__(self):
			self.f = open("archivo.log",'w')
			self.f.write('pc;timestamp;state;on_time;users;process;process_active;process_sleep;process_per_user;cpu_use;memory_use\n')
			self.f.flush()
			os.fsync(self.f)

	def __del__(self):
		self.f.close()


	def save_json(self,jdata):
		csv = '{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10}\n'.format(jdata['pc'],jdata['timestamp'],jdata['state'],jdata['on_time'],jdata['users'],jdata['process'],jdata['process_active'],jdata['process_sleep'],jdata['process_per_user'],jdata['cpu_use'],jdata['memory_use'])
		self.f.write(csv)
		self.f.flush()
