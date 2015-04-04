import sys

from flask import Flask, jsonify, abort, make_response, request
from flask.ext.restful import Api, Resource, reqparse, fields, marshal

import dataHandler
from dbHandler import BDHandler
import constantes as cts


app = Flask(__name__, static_url_path="")
api = Api(app)
data = BDHandler()

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
    cts.lugar: fields.String,
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
    cts.on_time : fields.Float,
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
        self.request_parser = reqparse.RequestParser()
        self.request_parser.add_argument('Nombre', type=str, required=True,
            help='Se debe introducir un nombre para el salon',
            location='json')
        self.request_parser.add_argument('Ubicacion', type=str, default="",
            location='json')
        self.request_parser.add_argument('Cantidad', type=int, default=0,
            location='json')
        super(SalonAPI, self).__init__()

    def get(self):
        return {'salones': [marshal(s, campos_salon) for s in salones]}



    def post(self):
        args = self.request_parser.parse_args()
        salon = {
            cts.nombre: args['Nombre'],
            cts.lugar: args['Ubicacion'],
            cts.cantidad: 0
        }
        data.save_salon(salon)
        salon[cts.ident] = 3
        return {'salon': marshal(salon, campos_salon)}, 201

class Salon_PCAPI(Resource):
    # decorators = [auth.login_required]

    def __init__(self):
        self.request_parser = reqparse.RequestParser()
        self.request_parser.add_argument('Nombre', type=str, location='json',
                                         required=True,
                                         help='La PC debe tener nombre')
        self.request_parser.add_argument('Salon', type=str, location='json')
        super(Salon_PCAPI, self).__init__()

    def get(self, salon):
        pcs_selected = [pc for pc in pcs if pc['Salon'] == salon]
        salon_selected = [s for s in salones if s['Nombre'] == salon]
        if not salon_selected:
            abort(404)
        salon = marshal(salon_selected[0], campos_salon)
        if not pcs_selected:
            abort(404)
        salon['pcs'] = [marshal(pc, campos_pc) for pc in pcs_selected]
        return  {'salon':salon}

class PCAPI(Resource):
    # decorators = [auth.login_required]

    def __init__(self):
        self.request_parser = reqparse.RequestParser()
        self.request_parser.add_argument('Nombre', type=str, location='json', required=True, help='Se debe proveer un nombre para la PC')
        self.request_parser.add_argument('Salon', type=str, location='json')
        self.regparse = reqparse.RequestParser()
        self.regparse.add_argument(cts.pc, type=str, location='json', required=True, help = 'Se debe proveer un nombre para la PC')
        self.regparse.add_argument(cts.timestamp, type=str, location='json', required=True, help='Se debe introducir un timestamp')
        self.regparse.add_argument(cts.state, type=str, location='json', required=True, help='se debe indicar el estado de la pc')
        self.regparse.add_argument(cts.on_time, type=float, location='json', required=True, help='se debe indicar el tiempo que lleva encendida')
        self.regparse.add_argument(cts.users, type=int, location='json', required=True, help='se debe indicar la cantidad de usuarios')
        self.regparse.add_argument(cts.process, type=int, location='json', required=True, help='se debe indicar la cantidad total de procesos')
        self.regparse.add_argument(cts.process_active, type=int, location='json', required=True, help='se debe indicar la cantidad de procesos activos')
        self.regparse.add_argument(cts.process_sleep, type=int, location='json', required=True, help='se debe indicar la cantidad de procesos dormidos')
        self.regparse.add_argument(cts.process_per_user, type=dict, location='json', required=False, help='se debe discriminar los procesos por usuario')
        self.regparse.add_argument(cts.cpu_use, type=float, location='json', required=True, help='se debe indicar el uso de cpu')
        self.regparse.add_argument(cts.memory_use, type=float, location='json', required=True, help='se debe indicar el uso de memoria')
        super(PCAPI, self).__init__()

    def get(self, ident):
        pcs_selected = [pc for pc in pcs if pc['id'] == ident]
        if not pcs_selected:
            abort(404)
        return {'pc': marshal(pcs_selected[0], campos_pc)}

    def put(self, ident):
        pcs_selected = [pc for pc in pcs if pc['id'] == ident]
        if not pcs_selected:
            abort(404)
        pc = pcs_selected[0]
        args = self.request_parser.parse_args()
        for k, v in args.items():
            if v is not None:
                pc[k] = v
        return {'pc': marshal(pc, campos_pc)}

    def delete(self, ident):
        pcs_selected = [pc for pc in pcs if pc['id'] == ident]
        if not pcs_selected:
            abort(404)
        pcs.remove(pcs_selected[0])
        return {'result': True}

    def post(self, ident):
        pcs_selected = [pc for pc in pcs if pc['id'] == ident]
        if not pcs_selected:
            abort(404)
        try:
            j = self.regparse.parse_args()
            data.save_json(j)
        except Exception:
            print "Error ", sys.exc_info()




api.add_resource(Salon_PCAPI, '/proy/api/v1/salones/<string:salon>', endpoint='salon_pc')
api.add_resource(SalonAPI, '/proy/api/v1/salones', endpoint='salon')
api.add_resource(PCAPI, '/proy/api/v1/pcs/<int:ident>', endpoint='pc')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
