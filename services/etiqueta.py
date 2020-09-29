from flask_restful import Resource
from flask_requests import request
from models import Etiqueta, EtiquetaSchema
from database import db

etiquetas_schema = EtiquetaSchema(many=True)
etiqueta_schema = EtiquetaSchema()

class EtiquetaAPI(Resource):
    def get(self, id=None):
        if id:
            tiqueta = Etiqueta.query.get(id)
            if not etiqueta:
                return {'etiqueta':'No existe la etiqueta'}, 400
            else:
                data = etiqueta_schema.dump(etiqueta)
                return {'etiqueta':data}, 204
        else:
            etiquetas = Etiqueta.query.all()
            etiquetas_lst = etiquetas_schema.dump(etiquetas)
            return {'etiqueta':etiquetas_lst}

    def delete(self, id):
        if id:
            etiqueta = Etiqueta.query.get(id) 
            if not etiqueta:
                return {'data':'No existe la etiqueta'}, 400
            else:
                etiqueta.delete()
                return {'status': 'success'}, 204
        else:
            abort(400)
            
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        errors = etiqueta_schema.validate(json_data)
        if errors:
            return {'message': 'Dato incorrecto'}, 500
        etiqueta = Etiqueta(
            description=json_data['description']
        )
        etiqueta.save()
        return {'status': 'success', 'data': json_data}, 201