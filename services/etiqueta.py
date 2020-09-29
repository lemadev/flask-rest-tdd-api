from flask import Blueprint, abort
from flask_restful import Resource
from models import Etiqueta, EtiquetaSchema
from database import db

etiquetas_schema = EtiquetaSchema(many=True)
etiqueta_schema = EtiquetaSchema()

etiqueta = Blueprint('etiqueta', __name__, template_folder='routes')

class EtiquetaMethods(Resource):
    def get(self, id):
        if id:
            tiqueta = Etiqueta.query.get(id)
            if not etiqueta:
                return {'etiqueta':'No existe la etiqueta'}, 400
            else:
                data = etiqueta_schema.dump(etiqueta)
                return {'etiqueta':data}, 200
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
                db.session.delete(etiqueta)
                db.session.commit()
                return {'status': 'success'}, 204
        else:
            abort(400)
            
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        #data, errors = encuesta_schema.load(json_data)
        #if errors:
        #    return {"status": "error", "data": errors}, 422
        data = etiqueta_schema.load(json_data)
        etiqueta = Etiqueta(
            description=data['description']
        )
        db.session.add(etiqueta)
        db.session.commit()
        return {'status': 'success', 'data': json_data}, 201