#Revision number $Revision$
#Date $Date$

import sys

from flask import Flask, jsonify, abort, make_response, request
from flask.ext.restful import Api, Resource, reqparse, fields, marshal

import dataHandler
from dbHandler import BDHandler
import constantes as ct


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
    ct.SAL_NOMBRE: fields.String,
    ct.SAL_LUGAR: fields.String,
    ct.SAL_CANT: fields.Integer,
    'uri': fields.Url('salon')
}

campos_pc = {
    'Nombre': fields.String,
    'Salon': fields.String,
    'uri': fields.Url('pc')
}

campos_registro = {
    ct.PC: fields.String,
    ct.TIMESTAMP : fields.DateTime(dt_format = 'iso8601'),
    ct.STATE : fields.String,
    ct.ON_TIME : fields.Float,
    ct.USERS : fields.Integer,
    ct.PROC : fields.Integer,
    ct.PROC_ACTIVE : fields.Integer,
    ct.PROC_SLEEP : fields.Integer,
    ct.PROC_PER_USER : fields.String,
    ct.CPU_USE : fields.Float,
    ct.MEM_USE : fields.Float
}

class SalonAPI(Resource):
    #decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('Nombre', type=str, required=True,
            help='Se debe introducir un nombre para el salon',
            location='json')
        self.reqparse.add_argument('Ubicacion', type=str, default="",
            location='json')
        self.reqparse.add_argument('Cantidad', type=int, default=0,
            location='json')
        super(SalonAPI, self).__init__()

    def get(self):
        return {'salones': [marshal(s, campos_salon) for s in salones]}



    def post(self):
        args = self.reqparse.parse_args()
        salon = {
            ct.SAL_NOMBRE: args['Nombre'],
            ct.SAL_LUGAR: args['Ubicacion'],
            ct.SAL_CANT: 0
        }
        data.save_salon(salon)
        salon[ct.SAL_ID] = 3
        return {'salon': marshal(salon, campos_salon)}, 201

class Salon_PCAPI(Resource):
    # decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('Nombre', type=str, location='json',
                                         required=True,
                                         help='La PC debe tener nombre')
        self.reqparse.add_argument('Salon', type=str, location='json')
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
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('Nombre', type=str, location='json', required=True, help='Se debe proveer un nombre para la PC')
        self.reqparse.add_argument('Salon', type=str, location='json')
        self.regparse = reqparse.RequestParser()
        self.regparse.add_argument(ct.PC, type=str, location='json', required=True, help = 'Se debe proveer un nombre para la PC')
        self.regparse.add_argument(ct.TIMESTAMP, type=str, location='json', required=True, help='Se debe introducir un timestamp')
        self.regparse.add_argument(ct.STATE, type=str, location='json', required=True, help='se debe indicar el estado de la pc')
        self.regparse.add_argument(ct.ON_TIME, type=float, location='json', required=True, help='se debe indicar el tiempo que lleva encendida')
        self.regparse.add_argument(ct.USERS, type=int, location='json', required=True, help='se debe indicar la cantidad de usuarios')
        self.regparse.add_argument(ct.PROC, type=int, location='json', required=True, help='se debe indicar la cantidad total de procesos')
        self.regparse.add_argument(ct.PROC_ACTIVE, type=int, location='json', required=True, help='se debe indicar la cantidad de procesos activos')
        self.regparse.add_argument(ct.PROC_SLEEP, type=int, location='json', required=True, help='se debe indicar la cantidad de procesos dormidos')
        self.regparse.add_argument(ct.PROC_PER_USER, type=dict, location='json', required=False, help='se debe discriminar los procesos por usuario')
        self.regparse.add_argument(ct.CPU_USE, type=float, location='json', required=True, help='se debe indicar el uso de cpu')
        self.regparse.add_argument(ct.MEM_USE, type=float, location='json', required=True, help='se debe indicar el uso de memoria')
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
        args = self.reqparse.parse_args()
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
        #encontrar id en bd de la pc
        try:
            j = self.regparse.parse_args()
            data.save_json(j)
        except Exception:
            print "Error ", sys.exc_info()
            abort(500)

class PC_sola_API(Resource):
    """API para el registro de pcs"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(ct.REG_NOMBRE, type=str, location='json')
        self.reqparse.add_argument(ct.REG_MAC, type=str, location='json')
        self.reqparse.add_argument(ct.REG_SO, type=str, location='json')
        self.reqparse.add_argument(ct.REG_RAM, type=float, location='json')
        self.reqparse.add_argument(ct.REG_ARCH, type=str, location='json')
        self.reqparse.add_argument(ct.REG_CPU, type=int, location='json')
        self.reqparse.add_argument(ct.REG_STATE, type=str, location='json')
        self.reqparse.add_argument(ct.REG_IP, type=str, location='json')
        super(PC_sola_API, self).__init__()

    def post(self):
        try:
            j = self.reqparse.parse_args()
            ident = data.register_pc(j)
            return {ct.API_RESULT:ident != 0, ct.API_ID:ident}
        except Exception:
            print "Error ", sys.exc_info()
            abort(500)

api.add_resource(Salon_PCAPI, '/proy/api/v1/salones/<string:salon>', endpoint='salon_pc')
api.add_resource(SalonAPI, '/proy/api/v1/salones', endpoint='salon')
api.add_resource(PCAPI, '/proy/api/v1/pcs/<int:ident>', endpoint='pc')
api.add_resource(PC_sola_API, '/proy/api/v1/pcs', endpoint='pc_sola')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
