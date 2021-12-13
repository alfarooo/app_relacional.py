#Importacion de las librerias de flask y SQLAlchemy
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

#Las importaciones utilizadas para SQLalchemy en relacion y estructura de las tablas
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

app = Flask (__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:root2001@localhost/uni_db'

db = SQLAlchemy(app)
Base = declarative_base()

#---------------------------------------------

association_table = Table('association', db.Model.metadata,
        Column('catedratico_id', ForeignKey('catedratico.id')),
        Column('materia_id', ForeignKey('materia.id'))
)

#--------------------------------------------


#Tabla estudiantes - uno a muchos / uno a uno
class universitario(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        primer_nombre = db.Column(db.String(20), unique=False, nullable=False)
        segundo_nombre = db.Column(db.String(20), unique=False, nullable=False)
        apellidos = db.Column(db.String(50), unique=False, nullable=False)
        edad = db.Column(db.Integer, nullable=False)
        cod_estudiantes =db.Column(db.Integer, db.ForeignKey('codigo_estudiante.id'))
        id_facultad = db.Column(db.Integer, db.ForeignKey('facultad_universitaria.id'))

        def as_dict(self):
                return {i.name: getattr(self, i.name) for i in self.__table__.columns}

        def __repr__(self):
                return f"apellidos : {self.apellidos}, codigo_estudiante: {self.cod_estudiantes}"


#Tabla profesores - muchos a muchos
class catedratico(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        materia_id = relationship(
        'materia',
        secondary=association_table,
        back_populates='materia')
        primer_nombre = db.Column(db.String(20), unique=False, nullable=False)
        segundo_nombre = db.Column(db.String(20), unique=False, nullable=False)
        apellidos = db.Column(db.String(50), unique=False, nullable=False)
        edad = db.Column(db.Integer, nullable=False)

        def as_dict(self):
                return {i.name: getattr(self, i.name) for i in self.__table__.columns}

        def __repr__(self):
                return f"Catedratico : {self.primer_nombre}, Facultad: {self.id_facultad}"


#Tabla facultad - uno a muchos
class facultad_universitaria(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        nombre_facultad = db.Column(db.String(20), unique=False, nullable=False)
        estudiante = db.relationship('universitario', backref='facultad')

        def as_dict(self):
                return {i.name: getattr(self, i.name) for i in self.__table__.columns}

        def __repr__(self):
                return f"id : {self.id}, nombre_facultad: {self.nombre_facultad}"


#Tabla materia - muchos a muchos
class materia(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        catedratico_id = db.relationship(
        'catedratico',
        secondary=association_table,
        back_populates="maestro")
        materia = db.Column(db.String(20), unique=False, nullable=False)

        def as_dict(self):
                return {i.name: getattr(self, i.name) for i in self.__table__.columns}

        def __repr__(self):
                return f"id : {self.id}, materia: {self.materia}"


#Tabla codigo_estudiante - uno a uno
class codigo_estudiante(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        cod_estudiante = db.Column(db.String(20), unique=False, nullable=False)
        estudiante = db.relationship('universitario', back_populates='cod', uselist=False)

        def as_dict(self):
                return {i.name: getattr(self, i.name) for i in self.__table__.columns}

        def __repr__(self):
                return f"id : {self.id}, codigo_estudiante: {self.cod_estudiante}"



#------------------------------------------------------------------------
#modulo principal INDEX
@app.route('/')
def index():
        return {"status": 200, "message": "The server is working"}



#------------------------------------------------------------------------ GET ALL
#modulo de GET de todos los estudiantes
@app.route('/estudiante/', methods=['GET'])
def get_all_estudiante():
        data = []
        items = universitario.query.all()
        for i in items:
                data.append({
                        "id": i.id,
                        "primer_nombre": i.primer_nombre,
                        "segundo_nombre": i.segundo_nombre,
                        "apellidos": i.apellidos,
                        "edad": i.edad,
                        "cod_estudiantes": i.cod_estudiantes,
                        "id_facultad": i.id_facultad
                })
        return {"status":200, "data": data}

#modulo de GET de todos los profesores
@app.route('/profesor/', methods=['GET'])
def get_all_profesor():
        data = []
        items = catedratico.query.all()
        for i in items:
                data.append({
                        "id": i.id,
                        "materia_id": i.materia_id,
                        "primer_nombre": i.primer_nombre,
                        "segundo_nombre": i.segundo_nombre,
                        "apellidos": i.apellidos,
                        "edad": i.edad
                })
        return {"status":200, "data": data}

#modulo de GET de todas las facultades
@app.route('/facultades/', methods=['GET'])
def get_all_facultades():
        data = []
        items = facultad_universitaria.query.all()
        for i in items:
                data.append({
                        "id": i.id,
                        "nombre_facultad": i.nombre_facultad
                })
        return {"status":200, "data": data}

#modulo de GET de todas las materias
@app.route('/materias/', methods=['GET'])
def get_all_materias():
        data = []
        items = materia.query.all()
        for i in items:
                data.append({
                        "id": i.id,
                        "catedratico_id": i.catedratico_id,
                        "materia": i.materia
                })
        return {"status":200, "data": data}

#modulo de GET de todos los codigos estudiantiles
@app.route('/codigo/', methods=['GET'])
def get_all_codigo():
        data = []
        items = codigo_estudiante.query.all()
        for i in items:
                data.append({
                        "id": i.id,
                        "cod_estudiante": i.cod_estudiante
                })
        return {"status":200, "data": data}

#------------------------------------------------------------------------GET ONE
#modulo de GET para un estudiante especifico por su ID
@app.route('/estudiante/<int:id>/', methods=['GET'])
def get_estudiante_by_id(id):
        item = universitario.query.get(id)
        if item:
                result = {
                        "id": i.id,
                        "primer_nombre": i.primer_nombre,
                        "segundo_nombre": i.segundo_nombre,
                        "apellidos": i.apellidos,
                        "edad": i.edad,
                        "cod_estudiantes": i.cod_estudiantes,
                        "id_facultad": i.id_facultad
                }
                return {"status":200, "data": result}
        return {"status":404, "data": {}}


#----------------------------------------------------------------------------POST
#modulo de POST para enviar informacion de los estudiantes
@app.route('/estudiante/', methods=['POST'])
def create_estudiante():
        data = request.json
        item = universitario(
                primer_nombre=data['primer_nombre'],
                segundo_nombre=data['segundo_nombre'],
                apellidos=data['apellidos'],
                edad=data['edad'],
                cod_estudiantes=data['cod_estudiantes'],
                id_facultad=data['id_facultad']
        )
        db.session.add(item)
        db.session.commit()
        db.session.refresh(item)
        return {"status": 201, "new_id": item.id}

#modulo de POST para enviar informacion de los profesores
@app.route('/profesor/', methods=['POST'])
def create_profesor():
        data = request.json
        item = catedratico(
                materia_id=data['materia_id'],
                primer_nombre=data['primer_nombre'],
                segundo_nombre=data['segundo_nombre'],
                apellidos=data['apellidos'],
                edad=data['edad']
        )
        db.session.add(item)
        db.session.commit()
        db.session.refresh(item)
        return {"status": 201, "new_id": item.id}

#modulo de POST para enviar informacion de las facultades
@app.route('/facultad/', methods=['POST'])
def create_facultad():
        data = request.json
        item = facultad_universitaria(
                nombre_facultad=data['nombre_facultad'],
                estudiantes=data['estudiantes']
        )
        db.session.add(item)
        db.session.commit()
        db.session.refresh(item)
        return {"status": 201, "new_id": item.id}

#modulo de POST para enviar informacion de materia
@app.route('/materias/', methods=['POST'])
def create_materias():
        data = request.json
        item = materia(
                materia=data['materia'],
                catedratico_id=data['catedratico_id']
        )
        db.session.add(item)
        db.session.commit()
        db.session.refresh(item)
        return {"status": 201, "new_id": item.id}

#modulo de POST para enviar informacion de los codigos estudiantiles
@app.route('/codigo/', methods=['POST'])
def create_codigo():
        data = request.json
        item = universitario(
                cod_estudiante=data['cod_estudiante']
        )
        db.session.add(item)
        db.session.commit()
        db.session.refresh(item)
        return {"status": 201, "new_id": item.id}


#-----------------------------------------------------------------------------PUT
#modulo de PUT para actualizar la informacion de los estudiantes
@app.route('/estudiante/<int:id>/', methods=['PUT'])
def update_estudiante(id):
        data = request.json
        item = universitario.query.get(id)
        if item:
                if 'primer_nombre' in data:
                        item.primer_nombre = data['primer_nombre']
                if 'segundo_nombre' in data:
                        item.segundo_nombre = data['segundo_nombre']
                if 'apellidos' in data:
                        item.apellidos = data['apellidos']
                if 'edad' in data:
                        item.edad = data['edad']
                if 'cod_estudiantes' in data:
                        item.cod_estudiantes = data['cod_estudiantes']
                if 'id_facultad' in data:
                        item.id_facultad = data['id_facultad']
                db.session.commit()
                return {"status": 200, "message": "Update successfully"}
        return {"status": 404, "message": "Not found item"}


#---------------------------------------------------------------------------DELETE
#modulo de DELETE para eliminar la informacion de un estudiante
@app.route('/estudiante/<int:id>/', methods=['DELETE'])
def delete_estudiante(id):
        item = universitario.query.get(id)
        if item:
                db.session.delete(item)
                db.session.commit()
                return {"status": 200, "message": "Item deleted"}
        return {"status": 404, "message": "Not found item"}

if __name__ == '__main__':
        app.run()




