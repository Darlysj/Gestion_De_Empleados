from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators, SelectField, RadioField, SelectMultipleField, PasswordField, TextAreaField
from wtforms.fields.html5 import EmailField, DateField
from wtforms import validators
from wtforms.validators import DataRequired, InputRequired

from models import Empleados

TIPO_USER = [1,2,3]

class registroForm(FlaskForm):
      id = StringField('Nº de Identificación', validators=[InputRequired('El campo es requerido')])
      
      nombre = StringField('Nombre', validators=[InputRequired('El campo es requerido'),
                              validators.length( min=3, max=30, message='Minimo 3 caracteres')])

      apellido = StringField('Apellido',[validators.Required(message='El campo es requerido'),
                              validators.length( min=3, max=30, message='Minimo 3 caracteres')])	

      email = EmailField('Email',[validators.Required(message='El campo es requerido')])

      direccion = StringField('Dirección',
                              [validators.Required(message='El campo es requerido')])

      ciudad = StringField('Ciudad',
                              [validators.Required(message='El campo es requerido')])	

      pais = StringField('País',[validators.Required(message='El campo es requerido')])

      telefono = StringField('Teléfono',
                              [validators.Required(message='El campo es requerido')])

      fecha_De_Ingreso = DateField('Fecha de Ingreso', format='%Y-%m-%d', 
                              validators=(validators.DataRequired(message='ingrese dato'),))

      tipo_Contrato = StringField('Tipo de Contrato', 
                              validators=(validators.DataRequired(message='ingrese dato'),))

      terminacion_Contrato  = DateField('Terminacion de Contrato', format='%Y-%m-%d', 
                              validators=(validators.DataRequired(message='ingrese dato'),))

      cargo = StringField('Cargo',
                              [validators.Required(message='El campo es requerido')])
      
      dependencia = StringField('Dependencia',
                              [validators.Required(message='El campo es requerido')])

      salario = StringField('Salario',
                          [validators.Required(message='El campo es requerido')])                     
                                             
      comentario =TextAreaField(label=' ')

      

class control_UserForm(FlaskForm):
      id = StringField('Nº de Identificacion')
      tipo_user = SelectField('Tipo De Usuario',choices=TIPO_USER)


class loginForm(FlaskForm):
      id = StringField(label = ' ')
      password = PasswordField(label = ' ')


class singUpForm(FlaskForm):
      id = IntegerField(label = ' ')
      password = PasswordField(label = ' ')


class desempenoForm(FlaskForm):
      id = IntegerField('Nº de Identificación', validators=[InputRequired('El campo es requerido')])
      
      empleado = StringField('Nombre y Apellidos', validators=[InputRequired('El campo es requerido'),
                              validators.length( min=3, max=30, message='Minimo 3 caracteres')])

      puntaje = IntegerField('Puntaje', validators=[InputRequired('El campo es requerido')])

      desempeno = TextAreaField('Desempeño', validators=[InputRequired('El campo es requerido')])