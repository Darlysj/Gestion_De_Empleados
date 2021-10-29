from flask import Flask,redirect,url_for,render_template,request, flash
from sqlalchemy.orm import with_expression
from wtforms import form
import forms
from flask import make_response, session
from flask_wtf import CSRFProtect, csrf
from config import DevelopmentConfig
from models import db
from models import Usuarios, Desempeno, Empleados, Comentarios



app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()



@app.route('/cookie')
def cookie():
    response = make_response(render_template('cookie.html'))
    response.set_cookie('datos_cookie', 'Undefained')
    return response 
    


@app.route('/')
@app.route('/index.html')
def index():   
    return render_template('index.html')



@app.route('/login.html', methods=['GET', 'POST'])
def login():
    login_form = forms.loginForm(request.form)
    if request.method=='POST' and login_form.validate():
        password = login_form.password.data
        n_identidad = login_form.id.data

        # saber si el usuario existe en la tabla usuarios 
        user = Usuarios.query.filter_by(n_identidad = n_identidad).first()# consulta en la bdd
        tipo = db.session.query(Empleados.tipo_user).filter_by(id = n_identidad).first()
        # si el usuario existe en la bdd y la contaseña es la misma que esta encriptada en la bdd
        if user is not None and user.verify_password(password) and tipo is not None: #verify_password es una funcion del modelo usuario
            # entonces ingresara a la pagina del tipo de usuario
            
            cant_user = Usuarios.query.count()# consulta en la bdd el numero de usuarios
            empleados = Empleados.query.count()# consulta en la bdd el numero de empleados
            session['cant_user'] = cant_user
            session['empleados'] = empleados
            session['usuario'] = n_identidad
            session['tipo_user'] = tipo[0]
            if tipo[0] == 1:
                
                return redirect('infoEmpleado.html')
                
            elif tipo[0] == 2:
                return redirect('consultar.html')

            elif  tipo[0] == 3:  
                return redirect('consultar.html')  

            else:
                # sino
                message = '¡Usuario o Contraseña incorrecta!'
                flash(message)

        else:
            # sino
            message = 'El usuario no existe'
            flash(message)

        return redirect('login.html')
    return render_template('login.html', form=login_form)



@app.route('/singUp.html', methods=['GET', 'POST'])
def singUp():
    singUp_form = forms.singUpForm(request.form)
    if request.method=='POST' and singUp_form.validate():
        id = singUp_form.id.data

        user = Empleados.query.filter_by(id = id).first()
        user2 = Usuarios.query.filter_by(n_identidad = id).first()
        if user is not None and user2 is None:
            singUp = Usuarios(  #solo le paso los parametros ya que estan inicializados en el modelo para encriptar password
                                singUp_form.id.data,
                                singUp_form.password.data
                            )
            db.session.add(singUp)
            db.session.commit()
            message = '¡nuevo usuario!'
            flash(message)
            return redirect('singUp.html')
        
        elif user is not None and user2 is not None:
            message = '¡El usuario ya existe!'
            flash(message)

        else:
            message = 'Nº de documento invalido'
            flash(message)  
            return render_template('singUp.html', form=singUp_form) 
   
    return render_template('singUp.html', form=singUp_form)
    


@app.route('/registrar.html', methods=['GET', 'POST'])
def Registro():
    registro_form = forms.registroForm(request.form)
    if request.method=='POST' and registro_form.validate():
        registro = Empleados( 
                                id = registro_form.id.data,
                                tipo_user= 1,
                                nombre = registro_form.nombre.data,
                                apellido = registro_form.apellido.data,
                                email = registro_form.email.data,
                                direccion = registro_form.direccion.data,
                                ciudad = registro_form.ciudad.data,
                                pais = registro_form.pais.data,
                                telefono = registro_form.telefono.data,
                                fecha_De_Ingreso = registro_form.fecha_De_Ingreso.data,
                                tipo_Contrato = registro_form.tipo_Contrato.data,
                                terminacion_Contrato = registro_form.terminacion_Contrato.data,
                                cargo = registro_form.cargo.data,
                                dependencia = registro_form.dependencia.data,
                                salario = registro_form.salario.data
                            )

        db.session.add(registro)
        db.session.commit()
        message = '¡ha sido registrado!'
        flash(message)      
        return redirect('registrar.html')
    return render_template('registrar.html', form=registro_form)  


@app.route('/consultar.html', methods=['GET', 'POST'])
def Consultar():
    registro_form = forms.registroForm(request.form)
    if request.method=='POST':
        id = registro_form.id.data
        lista = []
        registro =db.session.query(
                                    Empleados.nombre, Empleados.apellido, Empleados.email, Empleados.direccion, 
                                    Empleados.ciudad, Empleados.pais, Empleados.telefono, Empleados.tipo_Contrato,
                                    Empleados.fecha_De_Ingreso, Empleados.terminacion_Contrato, Empleados.cargo,
                                    Empleados.dependencia, Empleados.salario
                                    
                                ).filter_by(id = id).first()                           
        if registro:
            for i in registro:
                lista.append(i)
            return render_template('consultar.html', form=registro_form, lista = lista)
        else:
            message = 'NO EXISTE ESTE NUMERO DE ID'
            flash(message)    

    return render_template('consultar.html', form=registro_form)



@app.route('/editar.html', methods=['GET', 'POST'])
def Editar():
    registro_form = forms.registroForm(request.form)
    search_form = forms.registroForm(request.form)
    if request.method=='POST':
        id = search_form.id.data 

        #  Consultar si el ID existe en la bdd
        empleado = db.session.query(Empleados).filter(Empleados.id == id).first()
        #  Si existe entonces actualiza
        if empleado:
            db.session.query(Empleados).filter(
                Empleados.id == id

                ).update(
                            {
                                Empleados.nombre: registro_form.nombre.data,
                                Empleados.apellido: registro_form.apellido.data,
                                Empleados.email: registro_form.email.data,
                                Empleados.direccion: registro_form.direccion.data,
                                Empleados.ciudad: registro_form.ciudad.data,
                                Empleados.pais: registro_form.pais.data,
                                Empleados.telefono: registro_form.telefono.data,
                                Empleados.tipo_Contrato: registro_form.tipo_Contrato.data,
                                Empleados.fecha_De_Ingreso: registro_form.fecha_De_Ingreso.data,
                                Empleados.terminacion_Contrato: registro_form.terminacion_Contrato.data,
                                Empleados.cargo: registro_form.cargo.data,
                                Empleados.dependencia: registro_form.dependencia.data,
                                Empleados.salario: registro_form.salario.data
                            }
                        )        
            db.session.commit()
            message = 'actualizado'
            flash(message)
            return redirect('editar.html')
        else:
            message = 'NO EXISTE ESTE NUMERO DE ID'
            flash(message)
            return render_template('editar.html', form=registro_form)
            
    return render_template('editar.html', form=registro_form)




@app.route('/eliminar.html', methods=['GET', 'POST'])
def Eliminar():
    registro_form = forms.registroForm(request.form)
    if request.method=='POST':
        id = registro_form.id.data
        lista = []
        registro =db.session.query(
                                    Empleados.nombre, Empleados.apellido, Empleados.cargo,
                                    Empleados.dependencia
                                    
                                ).filter_by(id = id).first()                           
        if registro:
            for i in registro:
                lista.append(i)

            db.session.query(Empleados).filter(
                Empleados.id == id

                ).delete()
            db.session.commit()
            message = '¡Enviado!'
            flash(message)
            return render_template('eliminar.html', form=registro_form, lista = lista) 
        return redirect('eliminar.html')
    return render_template('eliminar.html', form=registro_form)




@app.route('/desempeño.html', methods=['GET', 'POST'])
def agregarDesempeno():
    desempeno_form = forms.desempenoForm(request.form)
    if request.method=='POST':
        desempeno = Desempeno ( 
                                fk_id = desempeno_form.id.data,
                                empleado = desempeno_form.empleado.data,
                                puntaje = desempeno_form.puntaje.data,
                                desempeno = desempeno_form.desempeno.data
                              )

        db.session.add(desempeno)
        db.session.commit()
        message = '¡Enviado!'
        flash(message)
        
        return redirect('desempeño.html')
    return render_template('desempeño.html', form=desempeno_form)




@app.route('/infoEmpleado.html', methods=['GET', 'POST'])
def CrearComentario():
    comentario_form = forms.registroForm(request.form)
    lista = []
    calificacion = []
    empleado = db.session.query ( Empleados.nombre, Empleados.apellido, Empleados.email, Empleados.direccion, 
                                  Empleados.ciudad, Empleados.pais, Empleados.telefono, Empleados.tipo_Contrato,
                                  Empleados.fecha_De_Ingreso, Empleados.terminacion_Contrato, Empleados.cargo,
                                  Empleados.dependencia, Empleados.salario
    
                                ).filter(Empleados.id == session['usuario']).first()
    desempeño = db.session.query(
                                  Desempeno.puntaje, Desempeno.desempeno
                                ).filter(Desempeno.fk_id == session['usuario']).first()                            
    if empleado:
        for i in empleado:
            lista.append(i)
    if desempeño:
        for i in desempeño:
            calificacion.append(i)

    if request.method=='POST':
        comentario = Comentarios( 
                                    fk_usuario = session['usuario'],
                                    comentario = comentario_form.comentario.data
                                )

        db.session.add(comentario)
        db.session.commit()
        message = '¡Enviado!'
        flash(message)
        return redirect('infoEmpleado.html')
    return render_template('infoEmpleado.html', form = comentario_form, lista = lista, calificacion = calificacion)    




@app.route('/asignarUser.html', methods=['GET', 'POST'])
def Asignar_User():
    controlUser_form = forms.control_UserForm(request.form)
    if request.method=='POST':
        id = controlUser_form.id.data
        #  Consultar si el ID existe en la bdd
        empleado = db.session.query(Empleados).filter(Empleados.id == id).first()
        #  Si existe entonces actualiza
        if empleado:
            db.session.query(Empleados).filter(
                Empleados.id == id

                ).update(
                            {
                                Empleados.tipo_user: controlUser_form.tipo_user.data
                            }
                        )        
            db.session.commit()
            message = '¡Usuario Asignado!'
            flash(message)
        return redirect('asignarUser.html')
    return render_template('asignarUser.html', form=controlUser_form)




if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        # db.drop_all() # borra las tablas cada vez que se ejecuta
        db.create_all() # crea las tablas 
    app.run(port=8000)
    