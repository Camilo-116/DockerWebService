from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Column,Integer,String,DateTime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:123456@localhost:3306/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# class tablaS(db.Model):
#     __tablename__= 'tablas'
#     id = db.Column(db.Integer, primary_key=True)
#     hash = db.Column(db.String)
#     timeStamp = db.Column(db.DateTime)

# class tablaA(db.Model):
#     __tablename__= 'tablaa'

#     id_a = db.Column(db.Integer, primary_key=True)
#     id = db.Column(db.Integer)
#     hash = db.Column(db.String)
#     timeStamp = db.Column(db.DateTime)
#     answer = db.Column(db.String)

# db.create_all()

# class tablaSchema(ma.Schema):
#     class Meta:
#         fields = ('id','hash','hashmap')

# tabla_Schema = tablaSchema()
# tabla_Schema = tablaSchema(many=True)

@app.route('/')
def conexion():
    return 'primer backend :D'

if __name__ == '__main__':
    app.run(debug=True,port=8000)

#methods=['GET'] para obtener datos
#methods=['POST'] para guardar datos
#methods=['PUT'] para actualizar datos
#methods=['DELETE'] para eliminar datos