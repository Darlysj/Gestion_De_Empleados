from enum import unique
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash #genera contraseñas encriptadas
from werkzeug.security import check_password_hash #para verificar que las contraseñas sean iguales
import datetime

db = SQLAlchemy()

class Empleados(db.Model):
    __tablename__ = 'empleados'

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    tipo_user = db.Column(db.Integer)
    nombre = db.Column(db.String)
    apellido = db.Column(db.String)
    email = db.Column(db.String)
    direccion = db.Column(db.String)
    ciudad = db.Column(db.String)
    pais = db.Column(db.String)
    telefono = db.Column(db.Integer)
    fecha_De_Ingreso = db.Column(db.String)
    tipo_Contrato = db.Column(db.String)
    terminacion_Contrato = db.Column(db.String)
    cargo = db.Column(db.String)
    dependencia = db.Column(db.Integer)
    salario = db.Column(db.String)
    desempeno = db.relationship('Desempeno')
    comentarios = db.relationship('Usuarios')
    fecha_registro = db.Column(db.Date, default = datetime.datetime.now)

    


class Desempeno(db.Model):
    __tablename__ = 'desempeño'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fk_id = db.Column(db.Integer, db.ForeignKey('empleados.id'))
    empleado = db.Column(db.String)
    puntaje = db.Column(db.Integer)
    desempeno = db.Column(db.Text)
    fecha_De_Comentario = db.Column(db.Date, default = datetime.datetime.now)


class Usuarios(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    n_identidad = db.Column(db.Integer, db.ForeignKey('empleados.id'), unique=True)
    password = db.Column(db.String(70))
    comentario = db.relationship('Comentarios')
    fecha_creacion = db.Column(db.Date, default = datetime.datetime.now)

    #lo siguiente es para encriptar las contraseñas usando generate_password_hash
    # 1 inicializamos los datos
    def __init__(self, n_identidad, password):
        self.n_identidad = n_identidad
        self.password = self.create_password(password)

    # 2 creo funcion para generar el password, luego en el app.py les paso los datos al modelo en la bdd
    def create_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, password): # comparar si la contraseña que estan enviando es la misma que en texto plano
        return check_password_hash(self.password, password) # devolvera un booleano



class Comentarios(db.Model):
    __tablename__ = 'comentarios'

    id = db.Column(db.Integer, primary_key=True)
    fk_usuario = db.Column(db.String, db.ForeignKey('usuarios.n_identidad'))
    comentario = db.Column(db.Text)
    fecha_Comentario = db.Column(db.Date, default = datetime.datetime.now)    