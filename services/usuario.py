from flask import Blueprint
from models import Usuario, UsuarioSchema, Respuesta, Encuesta, Pregunta, EncuestaSchema, RespuestaSchema, PreguntaSchema
from flask_requests import request
from database import db

usuario = Blueprint('usuario', __name__, template_folder='routes')

usuarios_schema = UsuarioSchema(many=True)
usuario_schema = UsuarioSchema()

encuestas_schema = EncuestaSchema(many=True)
encuesta_schema = EncuestaSchema()

respuestas_schema = RespuestaSchema(many=True)
respuesta_schema = RespuestaSchema()

preguntas_schema = PreguntaSchema(many=True)
pregunta_schema = PreguntaSchema()

@usuario.route('/usuarios', methods=['GET'])
def usuarios_get_all():
    usuarios = Usuario.query.all()
    usuarios_lst = usuarios_schema.dump(usuarios)
    return {'usuarios':usuarios_lst}

@usuario.route('/usuarios/<int:id>', methods=['GET'])
def usuarios_get_by_id(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return {'usuario':'No existe el usuario'}, 400
    else:
        user = usuario_schema.dump(usuario)
        return {'usuario':user}

@usuario.route('/usuarios', methods=['POST'])
def usuarios_nuevo_usuario():
    json_data = request.get_json(force=True)
    if not json_data:
        return {'message': 'No input data provided'}, 400
    #data, errors = usuario_schema.load(json_data)
    #if errors:
    #    return {"status": "error", "data": errors}, 422
    #data = usuario_schema.load(json_data)
    usuario = Usuario(
        nombre=json_data['nombre'],
        apellido=json_data['apellido'],
        email=json_data['email']
    )
    db.session.add(usuario)
    db.session.commit()
    return {'status': 'success', 'data': json_data}, 201

@usuario.route('/usuarios/delete/<int:id>', methods=['DELETE'])
def usuarios_delete_by_id(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return {'status': 'success'}, 204

@usuario.route('/usuarios/<int:id>', methods=['PUT'])
def usuarios_update_by_id(id):
    usuario = Usuario.query.get(id)
    data = request.get_json(force=True)
    nuevoNombre = data['nombre']
    usuario.nombre = nuevoNombre
    db.session.add(usuario)
    db.session.commit()
    return {'status': 'success', 'data': data}, 201

@usuario.route('/usuario/encuestas_by_usuario/<int:id>', methods=['GET'])
def usuario_encuestas_get_by_id_usuario(id):
    encuestas = Encuesta.query.filter_by(id_usuario=id).all()
    encuestas_lst = encuestas_schema.dump(encuestas)
    return {'encuestas':encuestas_lst}

@usuario.route('/usuario/encuesta/<int:id>', methods=['GET'])
def usuario_encuestas_get_by_id(id):
    encuesta = Encuesta.query.get(id)
    if not encuesta:
        return {'data':'No existe la encuesta'}, 400
    else:
        data = encuesta_schema.dump(encuesta)
        return {'data':data}

@usuario.route('/usuario/encuesta/delete/<int:id>', methods=['DELETE'])
def usuario_encuestas_delete_by_id(id):
    encuesta = Encuesta.query.get(id) 
    if not encuesta:
        return {'data':'No existe la encuesta'}, 400
    else:
        db.session.delete(encuesta)
        db.session.commit()
        return {'status': 'success'}, 204

@usuario.route('/usuario/encuesta/<int:id>', methods=['PUT'])
def usuario_encuestas_update_by_id(id):
    encuesta = Encuestas.query.get(id)
    if not encuesta:
        return {'data':'No existe la encuesta'}, 400
    else:
        data = request.get_json(force=True)
        nuevaEtiqueta = data['etiqueta']
        encuesta.nombre = nuevaEtiqueta
        db.session.add(encuesta)
        db.session.commit()
    return {'status': 'success', 'data': data}, 201

@usuario.route('/usuario/encuesta', methods=['POST'])
def usuario_encuestas_nueva_encuesta():
    json_data = request.get_json(force=True)
    if not json_data:
        return {'message': 'No input data provided'}, 400
    #data, errors = encuesta_schema.load(json_data)
    #if errors:
    #    return {"status": "error", "data": errors}, 422
    data = encuesta_schema.load(json_data)
    encuesta = Encuesta(
        id_usuario=data['id_usuario'],
        id_etiqueta=data['id_etiqueta']
    )
    db.session.add(encuesta)
    db.session.commit()
    return {'status': 'success', 'data': json_data}, 201

@usuario.route('/usuario/encuesta/preguntas', methods=['POST'])
def usuario_preguntas_nueva_pregunta():
    json_data = request.get_json(force=True)
    if not json_data:
        return {'message': 'No input data provided'}, 400
    #data, errors = encuesta_schema.load(json_data)
    #if errors:
    #    return {"status": "error", "data": errors}, 422
    data = pregunta_schema.load(json_data)
    pregunta = Pregunta(
        description=data['description'],
        numero=data['numero'],
        id_encuesta=data['id_encuesta']
    )
    db.session.add(pregunta)
    db.session.commit()
    return {'status': 'success', 'data': json_data}, 201

@usuario.route('/usuario/encuesta/preguntas/delete/<int:id>', methods=['DELETE'])
def usuario_preguntas_delete_by_id(id):
    pregunta = Pregunta.query.get(id) 
    if not encuesta:
        return {'data':'No existe la pregunta'}, 400
    else:
        db.session.delete(pregunta)
        db.session.commit()
        return {'status': 'success'}, 204

@usuario.route('/usuario/encuesta/preguntas/<int:id>', methods=['PUT'])
def usuario_preguntas_update_by_id(id):
    pregunta = Pregunta.query.get(id)
    data = []
    if not pregunta:
        return {'data':'No existe la pregunta'}, 400
    else:
        data = request.get_json(force=True)
        nuevaPregunta = data['description']
        pregunta.nombre = nuevaPregunta
        db.session.add(pregunta)
        db.session.commit()
    return {'status': 'success', 'data': data}, 201

@usuario.route('/usuario/preguntas/<int:id>', methods=['GET'])
def usuarios_get_preguntas_by_id_usuario(id):
    usuario = Usuario.query.get(id)
    preguntas_lst = []
    if not usuario:
        return {'data':'Usuario no existente'}, 400
    else:
        encuestas = Encuesta.query.filter_by(id_usuario=id).all()
        if len(encuestas) >= 1:
            for i, val in enumerate(encuestas):
                id_encuesta = val.id_encuesta
                preguntas = Pregunta.query.filter_by(id_encuesta=id_encuesta).all()
                if len(preguntas)>= 1:
                    preguntas_lst.append(preguntas_schema.dump(preguntas))            
    
    return {'status':'success','data':preguntas_lst}

@usuario.route('/usuarios/encuesta/pregunta/respuesta', methods=['POST'])
def usuarios_agregar_respuesta_pregunta():
    json_data = request.get_json(force=True)
    id_pregunta = json_data['id_pregunta']
    data = []
    if not id_pregunta:
        return {'data':'La pregunta no existente'}, 400
    else:
        cant_respuestas = Respuesta.query.filter_by(id_pregunta=id_pregunta).count()
        if cant_respuestas<4:
            respuesta = Respuesta(
                description=json_data['description'],
                id_pregunta=json_data['id_pregunta']
            )
            db.session.add(respuesta)
            db.session.commit()
        else:
            data= "La pregunta ya tiene 4 o más respuestas"

    return {'status':'success','data':data}

@usuario.route('/usuarios/encuesta/pregunta/respuesta/delete', methods=['DELETE'])
def usuarios_delete_respuesta():
    respuesta = Respuesta.query.get(id) 
    if not respuesta:
        return {'data':'No existe la respuesta'}, 400
    else:
        db.session.delete(respuesta)
        db.session.commit()
        return {'status': 'success'}, 204

@usuario.route('/usuarios/encuesta/pregunta/respuesta/<int:id>', methods=['GET'])
def usuario_respuesta_get_by_id(id):
    respuesta = Encuesta.query.get(id)
    if not respuesta:
        return {'data':'No existe la respuesta'}, 400
    else:
        data = respuesta_schema.dump(respuesta)
        return {'data':data}

@usuario.route('/usuarios/encuesta/pregunta/respuesta/<int:id>', methods=['PUT'])
def usuario_respuesta_update(id):
    respuesta = Respuesta.query.get(id)
    data = []
    if not respuesta:
        return {'data':'No existe la pregunta'}, 400
    else:
        data = request.get_json(force=True)
        nuevaRespuesta = data['description']
        respuesta.description = nuevaPregunta
        db.session.add(respuesta)
        db.session.commit()
    return {'status': 'success', 'data': data}, 201