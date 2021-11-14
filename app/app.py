from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_wtf import CSRFProtect
from werkzeug.utils import secure_filename
from config import DevelopmentConfig
import os

from bdd_controller import inicio_sesion
from investigador_controller import tipo_usuario, info_investigadores, info_grupos, perfil_investigador, actualizar_perfil
from carpetas_controller import comprobar_carpetas, mostrar_carpetas, actualizar_info_carpeta, nombre_carpeta, nueva_carpetaOS, nueva_carpetaBDD
from archivos_controller import comprobar_archivos, mostrar_archivos, actualizar_info_archivo, nombre_archivo, descargar_archivo, subir_archivos, nombre_archivo_compartido, compartir_archivo, archivos_compartidos
from usuarios_controller import info_usuarios, comprobar_usuario, ingresar_usuarioBDD, registrar_usuarioBDD

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)

@app.route("/")
@app.route("/home")
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():

    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        conexion = inicio_sesion(username, password)

        if conexion == True:
            session['username'] = username
            session['password'] = password

            tipoUsuario = tipo_usuario(username, password)
            session['usertype'] = tipoUsuario[0]

            if session['usertype'] == 'I':
                comprobar_carpetas(username, password)
                return redirect(url_for('folder'))

            elif session['usertype'] == 'A':
                return redirect(url_for('users'))

        elif conexion == False:
            msg = 'Usuario o contraseña incorrecto'
            
    elif 'username' in session and session['usertype'] == 'I':
        return redirect(url_for('folder'))
        
    elif 'username' in session and session['usertype'] == 'A':
        return redirect(url_for('users')) #Cambiar a direccion de Admin

    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
        session.pop('password', None)
        session.pop('usertype', None)
    return redirect(url_for('index'))

@app.route("/recover")
def recover():
    return render_template('password.html')

@app.route("/folders")
def folder():
    if 'username' in session and session['usertype'] == 'I':
        carpetas = mostrar_carpetas(session['username'], session['password'])
        return render_template('folder.html', carpetas=carpetas)
        
    return redirect(url_for('login'))

@app.route("/update_folder", methods=['POST'])
def update_info_folder():
    if 'username' in session:
        if request.method == 'POST' and 'descripcion' in request.form:
            nombre = request.form['nombreCarpeta']
            descripcion = request.form['descripcion']
            opcion = 'S' if 'opcion' in request.form else 'N'

            actualizar_info_carpeta(session['username'], session['password'], descripcion, opcion, nombre)
            return redirect(url_for('folder'))

    return redirect(url_for('login'))

@app.route("/create_folder", methods=['POST'])
def create_folder():

    msg = ''

    if 'username' in session:
        if request.method == 'POST' and 'carpetaNueva' in request.form  and 'carpetaDescNueva' in request.form:
            nombre = request.form['carpetaNueva']
            descripcion = request.form['carpetaDescNueva']

            nombreCarpeta = nombre_carpeta(session['username'], session['password'], nombre)

            if nombreCarpeta:
                msg = 'Ya existe una carpeta con ese nombre en el sistema'
                flash(msg, "danger")

            else:
                connectionOS = nueva_carpetaOS(session['username'], session['password'], nombre)

                if connectionOS == True:
                    nueva_carpetaBDD(session['username'], session['password'], nombre, descripcion)
                    msg = 'Carpeta creada correctamente'
                    flash(msg, "success")
                    return redirect(url_for('folder'))
                else:
                    msg = 'Ocurrio un error durante el registro'
                    flash(msg, "danger")
                    return redirect(url_for('folder'))

    return redirect(url_for('login'))

@app.route("/files", methods=['POST'])
def file():
    if 'username' in session:
        comprobar_archivos(session['username'], session['password'], request.form["nombre"])
        archivos = mostrar_archivos(session['username'], session['password'], request.form["nombre"])
        carpetas = mostrar_carpetas(session['username'], session['password'])
        investigadores = info_investigadores(session['username'], session['password'])

        return render_template('file.html', carpeta=request.form["nombre"], archivos=archivos, carpetas=carpetas, investigadores=investigadores)
        
    return redirect(url_for('login'))

@app.route("/update_file", methods=['POST'])
def update_info_file():
    if 'username' in session:
        if request.method == 'POST' and 'descripcion-archivo' in request.form:
            nombre = request.form['nombreArchivo']
            descripcion = request.form['descripcion-archivo']
            publicable = 'S' if 'publicable' in request.form else 'N'
            descarga = 'S' if 'op-descarga' in request.form else 'N'

            actualizar_info_archivo(session['username'], session['password'], descripcion, publicable, descarga, nombre)
            return redirect(url_for('folder'))

    return redirect(url_for('login'))

@app.route("/download_file", methods=['POST'])
def download_file():
    if 'username' in session:
        if request.method == 'POST':
            nombre = request.form['nameArchivo']
            resp = descargar_archivo(session['username'], session['password'], nombre)

            if resp == False:
                msg = 'El propietario desabilito las descargas del archivo'
                flash(msg, "warning")

            elif resp == True:
                msg = 'Archivo descargado, revisa la carpeta de descargas'
                flash(msg, "success")
            return redirect(url_for('folder'))

    return redirect(url_for('login'))

@app.route("/upload_file", methods=['GET', 'POST'])
def upload_file():
    if 'username' in session:
        if request.method == 'POST':
            archivoNuevo = request.files['archivo']
            carpetaUsuario = request.form['carpetasUser']
            nombreArchivo = nombre_archivo(session['username'], session['password'], archivoNuevo.filename)

            if nombreArchivo:
                msg = 'Ya existe un archivo con ese nombre en el sistema'
                flash(msg, "danger")

            else:
                archivoNuevo.save(os.path.join("temp", secure_filename(archivoNuevo.filename)))
                temp = os.getcwd()
                os.chdir(temp + '\\temp') #Windows
                #os.chdir(temp + '/temp') #Linux
                temp = os.getcwd()
                temp = temp + '\\' + archivoNuevo.filename #Windows
                #temp = temp + '/' + archivoNuevo.filename #Linux
                subir_archivos(session['username'], session['password'], carpetaUsuario, temp, archivoNuevo.filename)
                os.remove(temp)
                os.chdir('..')
                msg = 'Archivo subido correctamente'
                flash(msg, "success")

                return redirect(url_for('folder'))

    return redirect(url_for('login'))

@app.route("/share", methods=['POST'])
def share():
    if 'username' in session:
        if request.method == 'POST':
            usuarioCI = request.form['investigadoresId']
            nombreArchivo = request.form['nombreArchivoC']

            compartir = info_grupos(session['username'], session['password'], usuarioCI)
            
            if compartir == True:
                archivoC = nombre_archivo_compartido(session['username'], session['password'], nombreArchivo)

                if archivoC:
                    msg = 'Este archivo ya fue compartido con el investigador'
                    flash(msg, "warning")

                else:
                    compartir_archivo(session['username'], session['password'], usuarioCI, nombreArchivo)
                    msg = 'Archivo compartido correctamente'
                    flash(msg, "success")
                    return redirect(url_for('folder'))

            elif compartir == False:
                msg = 'El investigador no pertence a su grupo de trabajo, motivo por el cual no se puede compartir el archivo'
                flash(msg, "danger")
                return redirect(url_for('folder'))

    return redirect(url_for('login'))

@app.route("/share_files")
def share_files():
    if 'username' in session:
        archivos = archivos_compartidos(session['username'], session['password'])

        return render_template('share.html', archivos=archivos)
        
    return redirect(url_for('login'))

@app.route("/profile")
def profile():
    if 'username' in session:
        infoPerfil = perfil_investigador(session['username'], session['password'])

        return render_template('profile.html', infoPerfil=infoPerfil)

    return redirect(url_for('login'))

@app.route("/update_profile", methods=['POST'])
def update_profile():
    if 'username' in session:
        url = request.form['urlSearch']
        bio = request.form['biografia']
        actualizar_perfil(session['username'], session['password'], url, bio)
        msg = 'Información actualizada'
        flash(msg, "success")

        return redirect(url_for('profile'))

    return redirect(url_for('login'))

@app.route("/users")
def users():
    if 'username' in session and session['usertype'] == 'A':
        investigadores = info_usuarios(session['username'], session['password'])
        return render_template('user.html', investigadores=investigadores)
        
    return redirect(url_for('login'))

@app.route("/add_user")
def add_user():
    if 'username' in session and session['usertype'] == 'A':
        return render_template('add-user.html')

    return redirect(url_for('login'))

@app.route("/register_user", methods=['POST'])
def register_user():
    if 'username' in session and session['usertype'] == 'A':
        if request.method == 'POST':
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            ci = request.form['ci']
            instituto = request.form['instituto']
            correo = request.form['correo']
            user = request.form['user']
            contrasena = request.form['contrasena']

            investigador = comprobar_usuario(session['username'], session['password'], ci)

            if investigador:
                msg = 'Ya existe un usuario con esas credenciales en el sistema'
                flash(msg, "danger")
                return redirect(url_for('users'))

            else:            
                conexion = ingresar_usuarioBDD(session['username'], session['password'], user, contrasena)

                if conexion == True:
                    registrar_usuarioBDD(session['username'], session['password'], ci, instituto, user, nombre, apellido, correo)
                    msg = 'Usuario creado en el sistema'
                    flash(msg, "success")
                    return redirect(url_for('users'))

                elif conexion == False:
                    msg = 'Ocurrio un error al ingresar un nuevo usuario'
                    flash(msg, "danger")
                    return redirect(url_for('users'))

    return redirect(url_for('login'))

if __name__=='__main__':
    csrf.init_app(app)
    app.run(port='5000')