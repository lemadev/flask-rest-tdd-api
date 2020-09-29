from app import db
from flask_marshmallow import Marshmallow
from marshmallow import fields

ma = Marshmallow()

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20))
    apellido = db.Column(db.String(20))
    email = db.Column(db.String(30))
    encuestas = db.relationship('Encuesta', backref='usuario', lazy=True)

    def __init__(self, nombre, apellido, email):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email

class UsuarioSchema(ma.Schema):
    id_usuario = fields.Integer(dump_only=True)
    nombre = fields.String(required=True)
    apellido = fields.String(required=True)
    email = fields.String(required=True)

class Etiqueta(db.Model):
    id_etiqueta = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50))
    encuestas = db.relationship('Encuesta', backref='etiqueta', lazy=True)

    def __init__(self, description):
        self.description = description

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class EtiquetaSchema(ma.Schema):
    id_etiqueta = fields.Integer(dump_only=True)
    description = fields.String(required=True)

class Encuesta(db.Model):
    id_encuesta = db.Column(db.Integer, primary_key=True)
    id_etiqueta = db.Column(db.Integer, db.ForeignKey('etiqueta.id_etiqueta'),
        nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'),
        nullable=False)

    def __init__(self, id_etiqueta, id_usuario):
        self.id_etiqueta = id_etiqueta
        self.id_usuario = id_usuario

class EncuestaSchema(ma.Schema):
    id_encuesta = fields.Integer(dump_only=True)
    id_usuario = fields.Integer(required=True)
    id_etiqueta = fields.Integer(required=True)
