from datetime import datetime
import hashlib
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import create_engine
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import Session
import yaml as yml

#Import database connection credentials from docker-compose file
with open('docker-compose.yml') as fh:
    docker_compose = yml.load(fh, Loader=yml.FullLoader)
password,host,database = [docker_compose['services']['db']['environment']['MYSQL_ROOT_PASSWORD'],docker_compose['services']['db']['hostname'],docker_compose['services']['db']['environment']['MYSQL_DATABASE']]

app = Flask(__name__)
uri = 'mysql+pymysql://root:'+password+'@'+host+'/'+database
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SQLALCHEMY_DATABASE_URI']= uri
engine = create_engine(uri)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class tablaS(db.Model):
    __tablename__= 'tablas'
    id = db.Column(db.Integer)
    hash = db.Column(db.String(70), primary_key=True)
    timeStamp = db.Column(db.DateTime)

    def __init__(self,id,hash,timeStamp):
        self.id = id
        self.hash = hash
        self.timeStamp = timeStamp

class tablaA(db.Model):
    __tablename__= 'tablaa'
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(70), primary_key=True)
    timeStamp = db.Column(db.DateTime)
    answer = db.Column(db.String(70))

    def __init__(self,id,hash,timeStamp,answer):
        self.id = id
        self.hash = hash
        self.timeStamp = timeStamp
        self.answer = answer


if not database_exists(engine.url):
    print('Database didn\'t exist, creating...')
    create_database(engine.url)

db.create_all()

class tablaS_Schema(ma.Schema):
    class Meta:
        fields = ('id','hash','timeStamp')

class tablaA_Schema(ma.Schema):
    class Meta:
        fields = ('id','hash','timeStamp','answer')

tS_Schema = tablaS_Schema()
tSs_Schema = tablaS_Schema(many=True)
tA_Schema = tablaA_Schema()
tAs_Schema = tablaA_Schema(many=True)

#Verificando conexión a la base de datos
@app.route('/')
def conexion():
    try:
        with Session(engine) as session:
            return 'ok\n'
    except Exception as e:
        return 'nok\n'

#Creando sesiones en la tabla S
@app.route('/tablaS/<id>',methods=['GET'])
def createS(id):
    timestamp = datetime.now()
    hasher = hashlib.sha256()
    s = str(id) + str(timestamp)  # concatenate strings, then hash
    hasher.update(s.encode('utf-8'))
    hash = hasher.hexdigest()
    new_session = tablaS(id, hash, timestamp)
    try:
        db.session.add(new_session)
        db.session.commit()
        return 'Hash created: '+hash+'\n'
    except:
        return 'Could not create hash with id: '+id+" and time Stamp: "+timestamp+'\n'

#Creando sesiones en la tabla S (timeStamp manual)
@app.route('/tablaS/<id>/<ts>',methods=['GET'])
def createS_manual(id,ts):
    timestamp = datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S')
    hasher = hashlib.sha256()
    s = str(id) + str(timestamp)  # concatenate strings, then hash
    hasher.update(s.encode('utf-8'))
    hash = hasher.hexdigest()
    new_session = tablaS(id, hash, timestamp)
    try:
        db.session.add(new_session)
        db.session.commit()
        return 'Hash created: '+hash+'\n'
    except:
        return 'Could not create hash with id: '+id+' and time Stamp: '+timestamp+'\n'

#Creando sesiones en la tabla A
@app.route('/tablaA/<id>/<hash>',methods=['GET'])
def createA(id, hash):
    timestamp = datetime.now()
    sesion_timeStamp = tablaS.query.get(hash).timeStamp
    if (timestamp-sesion_timeStamp).total_seconds() <= 3600*4:
        answer = 'ok\n\nValid Hash.\n'
        print((timestamp-sesion_timeStamp).total_seconds()/60)
        new_assistance = tablaA(id, hash, timestamp,answer)
        try:
            db.session.add(new_assistance)
            db.session.commit()
            return answer
        except:
            return 'Duplicate key, entry not valid.\n'
    else:
        return 'nok\n\nHash not valid, more then 4 hours have passed since creation.\n'

#Obteniendo información de la tabla de sesiones
@app.route('/tablaS',methods=['GET'])
def get_TablaS():
    tablas = tablaS.query.all()
    resultS = tSs_Schema.dump(tablas)
    return tSs_Schema.jsonify(resultS)

#Obteniendo información de la tabla de asistencias
@app.route('/tablaA',methods=['GET'])
def get_TablaA():
    tablaa = tablaA.query.all()
    resultA = tAs_Schema.dump(tablaa)
    return tAs_Schema.jsonify(resultA)
    
#Eliminando las tablas
@app.route('/delete', methods=['GET'])
def delete_ID():
    try:
        db.session.query(tablaS).delete()
        db.session.query(tablaA).delete()
        db.session.commit()
        return 'ok\n'
    except:
        return 'nok\n'

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
