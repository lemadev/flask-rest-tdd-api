from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from services.etiqueta import EtiquetaAPI
from services.usuario import UsuarioAPI
from services.encuesta import EncuestaAPI
from instance.config import app_config

from models import db

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)
    app.config['SECRET_KEY']='key_secret'
    return app;

app = create_app(config_name='development')
api = Api(app)
api.add_resource(EtiquetaAPI, '/etiqueta/', '/etiqueta/<int:id>/')
api.add_resource(UsuarioAPI, '/usuario/', '/usuario/<int:id>/')
api.add_resource(EncuestaAPI, '/encuesta/', '/encuesta/<int:id>/')

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
