#!flask/bin/python

from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
import dataHandler
from fileHandler import FileHandler
from dbHandler import BDHandler
import constantes as cts
import sys

app = Flask(__name__, static_url_path="")
api = Api(app)
dataHandler = BDHandler()

salones = [
	{
		'id': 1,
		'Nombre': u'315',
		'Ubicacion': u'Tercer piso ',
		'Cantidad': 30
	}
]
pcs = [
	{
		'id': 1,
		'Nombre': u'PCUNIX114',
		'Salon': u'315',
	}
]

campos_salon = {
	cts.nombre: fields.String,
	cts.ubicacion: fields.String,
	cts.cantidad: fields.Integer,
	'uri': fields.Url('salon')
}

campos_pc = {
	'Nombre': fields.String,
	'Salon': fields.String,
	'uri': fields.Url('pc')
}

campos_registro = {
	cts.pc: fields.String,
	cts.timestamp : fields.DateTime(dt_format = 'iso8601'),
	cts.state : fields.String,
	cts.on_time : fileds.Float,
	cts.users : fields.Integer,
	cts.process : fields.Integer,
	cts.process_active : fields.Integer,
	cts.process_sleep : fields.Integer,
	cts.process_per_user : fields.String,
	cts.cpu_use : fields.Float,
	cts.memory_use : fields.Float
}

class SalonAPI(Resource):
	#decorators = [auth.login_required]

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('Nombre', type=str, required=True,help='Se debe introducir un nombre para el salon', location='json')
		self.reqparse.add_argument('Ubicacion', type=str, default="",  location='json')
		self.reqparse.add_argument('Cantidad', type=int, default=0, location='json')
		super(SalonAPI, self).__init__()

	def get(self):
		return {'salones': [marshal(s, campos_salon) for s in salones]}
	


	def post(self):
		args = self.reqparse.parse_args()
		salon = {
			cts.nombre: args['Nombre'],
			cts.lugar: args['Ubicacion'],
			cts.cantidad: 0
		}
		dataHandler.saveSalon(salon)
		salon[cts.ident] = 3
		return {'salon': marshal(salon, campos_salon)}, 201

class Salon_PCAPI(Resource):
	# decorators = [auth.login_required]

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('Nombre', type=str, location='json', required = True, help = 'Se debe proveer un nombre para la PC')
		self.reqparse.add_argument('Salon', type=str, location='json')
		super(Salon_PCAPI, self).__init__()
	
	def get(self, salon):
		pcs_selected = [pc for pc in pcs if pc['Salon'] == salon]
		salon_selected = [s for s in salones if s['Nombre'] == salon]
		if len(salon_selected) == 0:
			abort(404)
		salon = marshal(salon_selected[0], campos_salon)
		if len(pcs_selected) == 0:
			abort(404)
		salon['pcs'] = [marshal(pc, campos_pc) for pc in pcs_selected]
		return 	{'salon':salon}
		
class PCAPI(Resource):
	# decorators = [auth.login_required]

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('Nombre', type=str, location='json', required = True, help = 'Se debe proveer un nombre para la PC')
		self.reqparse.add_argument('Salon', type=str, location='json')
		super(PCAPI, self).__init__()

	def get(self, id):
		pcs_selected = [pc for pc in pcs if pc['id'] == id]
		if len(pcs_selected) == 0:
			abort(404)
		return {'pc': marshal(pcs_selected[0], campos_pc)}
		
	def put(self, id):
		pcs_selected = [pc for pc in pcs if pc['id'] == id]
		if len(pcs_selected) == 0:
			abort(404)
		pc = pcs_selected[0]
		args = self.reqparse.parse_args()
		for k, v in args.items():
			if v is not None:
				pc[k] = v
		return {'pc': marshal(pc, campos_pc)}

	def delete(self, id):
		pcs_selected = [pc for pc in pcs if pc['id'] == id]
		if len(pcs_selected) == 0:
			abort(404)
		pcs.remove(pcs_selected[0])
		return {'result': True}
		
	def post(self,id):
		pcs_selected = [pc for pc in pcs if pc['id'] == id]
		if len(pcs_selected) == 0:
			abort(404)
		try:
			j = request.get_json()
			dataHandler.saveJson(j)
		except:
			print "Error ", sys.exc_info()
		
		


api.add_resource(Salon_PCAPI, '/proy/api/v1/salones/<string:salon>', endpoint='salon_pc')
api.add_resource(SalonAPI, '/proy/api/v1/salones', endpoint='salon')
api.add_resource(PCAPI, '/proy/api/v1/pcs/<int:id>', endpoint='pc')

if __name__ == '__main__':
	app.run(debug=True, host = '0.0.0.0', port = 80)
