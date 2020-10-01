from models import Usuario, UsuarioSchema
from flask_restful import Resource
from flask_requests import request

usuarios_schema = UsuarioSchema(many=True)
usuario_schema = UsuarioSchema()

class UsuarioAPI(Resource):
    def get(self, id=None):
        if id:
            usuario = Usuario.query.get(id)
            if not usuario:
                return {'usuario':'No existe el usuario'}, 400
            else:
                user = usuario_schema.dump(usuario)
                return {'usuario':user}
        else:
            usuarios = Usuario.query.all()
            usuarios_lst = usuarios_schema.dump(usuarios)
            return {'usuarios':usuarios_lst}

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        errors = usuario_schema.validate(json_data)
        if errors:
            return {'message': 'Datos incorrectos'}, 500
        crear_usuario(json_data).save()
        return {'status': 'success', 'data': json_data}, 201

    def delete(self, id):
        usuario = Usuario.query.get(id) 
        if not usuario:
            return {'data':'No existe el usuario'}, 400
        else:
            usuario.delete()
            return {'status': 'success'}, 204

def crear_usuario(data):
    usuario = Usuario(
            nombre=data['nombre'],
            apellido=data['apellido'],
            email=data['email']
        )
    return usuario