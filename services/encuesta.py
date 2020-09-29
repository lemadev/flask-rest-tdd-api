from flask import Blueprint
from models import Encuesta, EncuestaSchema

encuestas_schema = EncuestaSchema(many=True)
encuesta_schema = EncuestaSchema()

encuesta = Blueprint('encuesta', __name__, template_folder='routes')

@encuesta.route('/encuestas', methods=['GET'])
def encuestas_get_all():
    encuestas = Encuesta.query.all()
    encuestas_lst = encuestas_schema.dump(encuestas)
    return {'encuestas':encuestas_lst}

@encuesta.route('/encuestas/etiqueta/<int:id>', methods=['GET'])
def encuestas_get_by_id_etiqueta(id):
    etiqueta = Etiqueta.query.get(id)
    encuestas_lst = []
    if not etiqueta:
        return {'data':'Etiqueta no existente'}, 400
    else:
        encuestas = Encuesta.query.filter_by(id_etiqueta=id).all()
        encuestas_lst = encuestas_schema.dump(encuestas)
    return {'encuestas':encuestas_lst}    