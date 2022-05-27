from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

app = Flask(__name__)
uri = 'mysql+pymysql://root:123456@localhost/prueba'
app.config['SQLALCHEMY_DATABASE_URI']= uri
engine = create_engine(uri)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class tablaS(db.Model):
    __tablename__= 'tablas'
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(70))
    timeStamp = db.Column(db.DateTime)

    def __init__(self,id,hash,timeStamp):
        self.id = id
        self.hash = hash
        self.timeStamp = timeStamp

class tablaA(db.Model):
    __tablename__= 'tablaa'
    id_a = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    hash = db.Column(db.String(70))
    timeStamp = db.Column(db.DateTime)
    answer = db.Column(db.String(70))

    def __init__(self,id,ida,hash,timeStamp,answer):
        self.id = id
        self.ida = ida
        self.hash = hash
        self.timeStamp = timeStamp
        self.answer = answer

db.create_all()

class tablaSchema(ma.Schema):
    class Meta:
        fields = ('id','ida','hash','timeStamp','answer')

tabla_Schema = tablaSchema()
tablas_Schema = tablaSchema(many=True)

#Verificando conexión a la base de datos
@app.route('/')
def conexion():
    try:
        with Session(engine) as session:
            return 'ok'
    except Exception as e:
        return 'nok'

#Enviando información a las tablas
@app.route('/tablas',methods=['POST'])
def create():
    print(request.json)
    return 'Recibido'

#Obteniendo información de las tablas
@app.route('/tablas',methods=['GET'])
def get_Tabla():
    tablas = tablaS.query.all()
    tablaa = tablaA.query.all()
    resultS = tabla_Schema.dump(tablas)
    resultA = tabla_Schema.dump(tablaa)
    return jsonify(resultS,resultA)

#Buscando en la tabla de sesiones por ID
@app.route('/sesion/<id>')
def get_ID(id):
    sesion = tablaS.query.get(id)
    return tablas_Schema.jsonify(sesion)

#Eliminando las tablas
@app.route('/delete', methods=['DELETE'])
def delete_ID():
    sesionS = tablaS.query.all()
    db.session.delete(sesionS)
    sesionA = tablaS.query.all()
    db.session.delete(sesionA)
    db.session.commit()

    return tablas_Schema.jsonify(sesionS,sesionA)

@app.route('sesion/<id>/<hash>')
def checkerID_Hash(id,hash):
    if tablaS.query.get(hash) != "{''}":
        answer = 'ok'
        #Almacenar id, hash, timeStamp y answer a tabla A
        return answer
    else:
        answer = 'nok'
        #Almacenar id, hash, timeStamp y answer a tabla A
        return answer

if __name__ == '__main__':
    app.run(debug=True,port=8000)
