from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Column,Integer,String,DateTime,create_engine
from sqlalchemy.orm import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:123456@localhost/prueba'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
engine = create_engine('mysql+pymysql://root:123456@localhost/prueba')


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

db.create_all()

class tablaSchema(ma.Schema):
    class Meta:
        fields = ('id','hash','hashmap')

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
@app.route('/sesion/<id>',methods=['GET'])
def get_ID(id):
    sesion = tablaS.query.get(id)
    return tablas_Schema.jsonify(sesion)

#Buscando y actualizando en la tabla de sesiones por ID
@app.route('/sesion/<id>',methods=['PUT'])
def update_ID(id):
    sesion = tablaS.query.get(id)

    idS = request.json['id']
    hash = request.json['hash']
    timeStamp = request.json['timeStamp']

    tablaS.id = idS
    tablaS.hash = hash
    tablaS.timeStamp = timeStamp

    db.session.commit()

    return tablas_Schema.jsonify(sesion)

#Buscando y Eliminando en la tabla de sesiones por ID
@app.route('/sesion/<id>', methods=['DELETE'])
def delete_ID(id):
    sesion = tablaS.query.get(id)
    db.session.delete(sesion)
    db.session.commit()

    return tablas_Schema.jsonify(sesion)

if __name__ == '__main__':
    app.run(debug=True,port=8000)