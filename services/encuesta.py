from models import Encuesta, EncuestaSchema
from flask_restful import Resource
from flask_requests import request
from impl import db_impl

encuestas_schema = EncuestaSchema(many=True)
encuesta_schema = EncuestaSchema()

class EncuestaAPI(Resource):
    def get(self, id=None):
        if id:
            encuesta = Encuesta.query.get(id)
            if not encuesta:
                return {'encuesta':'No existe la encuesta'}, 400
            else:
                en = encuesta_schema.dump(encuesta)
                return {'encuesta':en}
        else:
            encuestas = Encuesta.query.all()
            encuestas_lst = encuestas_schema.dump(encuestas)
            return {'encuestas':encuestas_lst}

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        errors = encuesta_schema.validate(json_data)
        if errors:
            return {'message': 'Datos incorrectos'}, 500
        db_impl.save(crear_encuesta(json_data))
        return {'status': 'success', 'data': json_data}, 201

    def delete(self, id):
        encuesta = Encuesta.query.get(id) 
        if not encuesta:
            return {'data':'No existe la encuesta'}, 400
        else:
            db_impl.delete(encuesta)
            return {'status': 'success'}, 204

def crear_encuesta(data):
    encuesta = Encuesta(
            id_etiqueta=data['id_etiqueta'],
            id_usuario=data['id_usuario']
        )
    return encuesta

