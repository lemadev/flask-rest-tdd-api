from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from database import db
from services.encuesta import encuesta
from services.usuario import usuario
from services.etiqueta import EtiquetaAPI
#from services.etiqueta import etiqueta

app = Flask(__name__)

#app.register_blueprint(encuesta)
#app.register_blueprint(usuario)
#app.register_blueprint(etiqueta)

#Configuración de la bd
USER_DB = 'postgres'
PASS_DB = 'admin'
URL_DB = 'localhost'
NAME_DB = 'proyecto_api'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Inicializacion del objeto db de sqlalchemy
#db = SQLAlchemy(app)
db.init_app(app)

#configurar flask-migrate
migrate = Migrate()
migrate.init_app(app, db)

#configuracion de flask-wtf
app.config['SECRET_KEY']='key_secret'


api = Api(app)
api.add_resource(EtiquetaAPI, '/etiqueta/', '/etiqueta/<int:id>/')


@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
