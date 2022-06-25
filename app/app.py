from flask import Flask, render_template, redirect, request, url_for, session, flash, abort
from flask_wtf import CSRFProtect
from werkzeug.utils import secure_filename
from config import DevelopmentConfig
import os

from bdd_controller import inicio_sesion
from contenido_controller import mostrar_contenido_home, mostrar_contenido_subcarpeta
from investigador_controller import tipo_usuario, info_investigadores, info_grupos, perfil_investigador, actualizar_perfil, actualizar_foto
from carpetas_controller import comprobar_carpetas_home, comprobar_subcarpetas, actualizar_info_carpeta, nombre_carpeta, nueva_carpetaOS, nueva_carpetaBDD, carpeta_descargas
from archivos_controller import comprobar_archivos_home, comprobar_archivos_subcarpeta, actualizar_info_archivo, nombre_archivo, descargar_archivo, subir_archivos, nombre_archivo_compartido, compartir_archivo, archivos_compartidos, verificar_foto
from usuarios_controller import info_ciudades, info_usuarios, comprobar_usuario, ingresar_usuarioOS, ingresar_usuarioBDD, registrar_usuarioBDD, info_grupos_sistema, info_instituciones, comprobar_grupo, ingresar_grupoOS, ingresar_grupoBDD, comprobar_institucion, ingresar_institucionBDD, configurar_pass, grupos_os, comprobar_grupos_investigador, nuevo_grupo_investigadorOS, nuevo_grupo_investigadorBDD

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)

@app.route("/")
@app.route("/home")
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(err):
    return render_template("404.html"), 404

@app.errorhandler(401)
def forbidden(err):
    return render_template("401.html"), 401

@app.errorhandler(500)
def internal_error(err):
    return render_template("500.html"), 500

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
                carpeta_descargas(username, password)
                comprobar_carpetas_home(username, password)
                comprobar_archivos_home(username, password)
                return redirect(url_for('folder'))

            elif session['usertype'] == 'A':
                return redirect(url_for('users'))

            else:
                abort(401)

        elif conexion == False:
            msg = 'Usuario o contraseña incorrecto'
            
    elif 'username' in session and session['usertype'] == 'I':
        return redirect(url_for('folder'))
        
    elif 'username' in session and session['usertype'] == 'A':
        return redirect(url_for('users'))

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
        home = tipo_usuario(session['username'], session['password'])
        comprobar_archivos_home(session['username'], session['password'])
        contenidos = mostrar_contenido_home(session['username'], session['password'])
        investigadores = info_investigadores(session['username'], session['password'])
        return render_template('folder.html', home=home, contenidos=contenidos, investigadores=investigadores)
        
    return redirect(url_for('login'))

@app.route("/subfolders", methods=['POST'])
def subfolder():
    if 'username' in session:
        path = request.form["path"]
        comprobar_archivos_subcarpeta(session['username'], session['password'], path)
        comprobar_subcarpetas(session['username'], session['password'], path)
        contenidos = mostrar_contenido_subcarpeta(session['username'], session['password'], path)
        investigadores = info_investigadores(session['username'], session['password'])
        return render_template('subfolder.html', path=path, contenidos=contenidos, investigadores=investigadores)

    return redirect(url_for('login'))        

@app.route("/update_folder", methods=['POST'])
def update_info_folder():
    if 'username' in session:
        if request.method == 'POST' and 'descripcion' in request.form:
            nombre = request.form['nombreCarpeta']
            descripcion = request.form['descripcion']
            opcion = 'S' if 'opcion' in request.form else 'N'

            actualizar = actualizar_info_carpeta(session['username'], session['password'], descripcion, opcion, nombre)

            if actualizar == True:
                msg = 'La información de la carpeta fue actualizada'
                flash(msg, "success")
                return redirect(url_for('folder'))

            elif actualizar == False:
                msg = 'No se pudo actualizar la información de la carpeta'
                flash(msg, "danger")
                return redirect(url_for('folder'))

    return redirect(url_for('login'))

@app.route("/create_folder", methods=['POST'])
def create_folder():
    if 'username' in session:
        if request.method == 'POST' and 'carpetaNueva' in request.form  and 'carpetaDescNueva' in request.form:
            path = request.form['newFolder']
            nombre = request.form['carpetaNueva']
            descripcion = request.form['carpetaDescNueva']

            nombreCarpeta = nombre_carpeta(session['username'], session['password'], nombre)

            if nombreCarpeta:
                msg = 'Ya existe una carpeta con ese nombre en el sistema'
                flash(msg, "danger")
                return redirect(url_for('folder'))

            else:
                connectionOS = nueva_carpetaOS(session['username'], session['password'], path, nombre)

                if connectionOS == True:
                    nueva_carpetaBDD(session['username'], session['password'], path, nombre, descripcion)
                    msg = 'Carpeta creada en: ' + path
                    flash(msg, "success")
                    return redirect(url_for('folder'))
                else:
                    msg = 'Ocurrio un error durante el registro'
                    flash(msg, "danger")
                    return redirect(url_for('folder'))

    return redirect(url_for('login'))

@app.route("/update_file", methods=['POST'])
def update_info_file():
    if 'username' in session:
        if request.method == 'POST' and 'descripcion-archivo' in request.form:
            nombre = request.form['nombreArchivo']
            descripcion = request.form['descripcion-archivo']
            publicable = 'S' if 'publicable' in request.form else 'N'
            descarga = 'S' if 'op-descarga' in request.form else 'N'

            actualizar = actualizar_info_archivo(session['username'], session['password'], descripcion, publicable, descarga, nombre)

            if actualizar == True:
                msg = 'La información y permisos del archivo fueron actualizados'
                flash(msg, "success")
                return redirect(url_for('folder'))

            elif actualizar == False:
                msg = 'No se pudo actualizar la información y permisos del archivo'
                flash(msg, "danger")
                return redirect(url_for('folder'))

    return redirect(url_for('login'))

@app.route("/download_file", methods=['POST'])
def download_file():
    if 'username' in session:
        if request.method == 'POST':
            nombre = request.form['nameArchivo']
            resp = descargar_archivo(session['username'], session['password'], nombre)

            if resp == False:
                msg = 'Las descargas del archivo están desabilitadas'
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
            path = request.form['newFile']
            archivoNuevo = request.files['archivo']
            nombreArchivo = nombre_archivo(session['username'], session['password'], archivoNuevo.filename)

            if nombreArchivo:
                msg = 'Ya existe un archivo con ese nombre en el sistema'
                flash(msg, "danger")

            else:
                nuevoNombre = archivoNuevo.filename.replace(" ", "_")
                if os.name == 'nt':
                    archivoNuevo.save(os.path.join("temp", secure_filename(nuevoNombre)))
                    temp = os.getcwd()
                    os.chdir(temp + '\\temp')
                    temp = os.getcwd()
                    temp = temp + '\\' + nuevoNombre
                    subir_archivos(session['username'], session['password'], path, temp, archivoNuevo.filename)
                    os.remove(temp)
                    os.chdir('..')
                    msg = 'Archivo subido a: ' + path
                    flash(msg, "success")
                    return redirect(url_for('folder'))

                elif os.name == 'posix':
                    archivoNuevo.save(os.path.join("temp", secure_filename(archivoNuevo.filename)))
                    temp = os.getcwd()
                    os.chdir(temp + '/temp')
                    temp = os.getcwd()
                    temp = temp + '/' + archivoNuevo.filename
                    subir_archivos(session['username'], session['password'], path, temp, archivoNuevo.filename)
                    os.remove(temp)
                    os.chdir('..')
                    msg = 'Archivo subido a: ' + path
                    flash(msg, "success")
                    return redirect(url_for('folder'))

    return redirect(url_for('login'))

@app.route("/share", methods=['POST'])
def share():
    if 'username' in session:
        if request.method == 'POST':
            usuarioId = request.form['investigadoresId']
            nombreArchivo = request.form['nombreArchivoC']

            compartir = info_grupos(session['username'], session['password'], usuarioId)
            
            if compartir == True:
                archivoC = nombre_archivo_compartido(session['username'], session['password'], nombreArchivo)

                if archivoC:
                    msg = 'Este archivo ya fue compartido con el investigador'
                    flash(msg, "warning")

                else:
                    compartir_archivo(session['username'], session['password'], usuarioId, nombreArchivo)
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
        foto = request.files['foto']

        if not foto.filename:
            actualizar_perfil(session['username'], session['password'], url, bio)
            msg = 'Información actualizada'
            flash(msg, "success")
            return redirect(url_for('profile'))

        else:
            tipoArchivo = verificar_foto(foto.filename)

            if foto.filename and tipoArchivo:
                if os.name == 'nt':
                    foto.save(os.path.join("app/static/img/admin/pictures", secure_filename(foto.filename)))
                    actualizar_perfil(session['username'], session['password'], url, bio)
                    actualizar_foto(session['username'], session['password'], foto.filename)

                    msg = 'Información actualizada'
                    flash(msg, "success")
                    return redirect(url_for('profile'))

                elif os.name == 'posix':
                    foto.save(os.path.join("app/static/img/admin/pictures", secure_filename(foto.filename)))
                    actualizar_perfil(session['username'], session['password'], url, bio)
                    actualizar_foto(session['username'], session['password'], foto.filename)

                    msg = 'Información actualizada'
                    flash(msg, "success")
                    return redirect(url_for('profile'))

            else:
                msg = 'Formato de foto incorrecto, usar formato PNG o JPG'
                flash(msg, "danger")
                return redirect(url_for('profile'))

    return redirect(url_for('login'))

@app.route("/users")
def users():
    if 'username' in session and session['usertype'] == 'A':
        investigadores = info_usuarios(session['username'], session['password'])
        instituciones = info_instituciones(session['username'], session['password'])
        grupos = info_grupos_sistema(session['username'], session['password'])
        gruposS = grupos_os(session['username'], session['password'])
        return render_template('user.html', investigadores=investigadores, instituciones=instituciones, grupos=grupos, gruposS=gruposS)
    else:
        abort(401)

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
            grupo = request.form['grupo']
            contrasena = request.form['contrasena']

            investigador = comprobar_usuario(session['username'], session['password'], ci)

            if investigador:
                msg = 'Ya existe un usuario con esas credenciales en el sistema'
                flash(msg, "danger")
                return redirect(url_for('users'))

            else:
                connectionOS = ingresar_usuarioOS(session['username'], session['password'], user, grupo)

                if connectionOS == True:
                    configurar_pass(session['username'], session['password'], user, contrasena)
                    conexion = ingresar_usuarioBDD(session['username'], session['password'], user, contrasena)

                    if conexion == True:
                        registrar_usuarioBDD(session['username'], session['password'], ci, instituto, user, grupo, nombre, apellido, correo)
                        msg = 'Usuario creado en el sistema'
                        flash(msg, "success")
                        return redirect(url_for('users'))

                    elif conexion == False:
                        msg = 'Ocurrio un error al ingresar un nuevo usuario'
                        flash(msg, "danger")
                        return redirect(url_for('users'))

                else:
                    msg = 'Ocurrio un error durante el registro'
                    flash(msg, "danger")
                    return redirect(url_for('users'))

    else:
        abort(401)

@app.route("/groups")
def groups():
    if 'username' in session and session['usertype'] == 'A':
        grupos = info_grupos_sistema(session['username'], session['password'])
        return render_template('group.html', grupos=grupos)

    else:
        abort(401)

@app.route("/create_group", methods=['POST'])
def create_group():
    if 'username' in session and session['usertype'] == 'A':
        if request.method == 'POST' and 'grupoNuevo' in request.form  and 'grupoDescNueva' in request.form:
            nombre = request.form['grupoNuevo']
            descripcion = request.form['grupoDescNueva']

            nombreGrupo = comprobar_grupo(session['username'], session['password'], nombre)

            if nombreGrupo:
                msg = 'Ya existe un grupo con ese nombre en el sistema'
                flash(msg, "danger")
                return redirect(url_for('groups'))

            else:
                connectionOS = ingresar_grupoOS(session['username'], session['password'], nombre)

                if connectionOS == True:
                    ingresar_grupoBDD(session['username'], session['password'], nombre, descripcion)
                    msg = 'Grupo creado correctamente'
                    flash(msg, "success")
                    return redirect(url_for('groups'))
                else:
                    msg = 'Ocurrio un error durante el registro'
                    flash(msg, "danger")
                    return redirect(url_for('folder'))
    else:
        abort(401)

@app.route("/institutes")
def institutes():
    if 'username' in session and session['usertype'] == 'A':
        instituciones = info_instituciones(session['username'], session['password'])
        ciudades = info_ciudades(session['username'], session['password'])
        return render_template('institute.html', instituciones=instituciones, ciudades=ciudades)
    
    else:
        abort(401)

@app.route("/create_institute", methods=['POST'])
def create_institute():
    if 'username' in session and session['usertype'] == 'A':
        if request.method == 'POST' and 'institucionNueva' in request.form  and 'institucionDescNueva' in request.form:
            nombre = request.form['institucionNueva']
            ciudad = request.form['institucionCiudad']
            descripcion = request.form['institucionDescNueva']

            institucion = comprobar_institucion(session['username'], session['password'], nombre)

            if institucion:
                msg = 'Ya existe una institución con ese nombre en el sistema'
                flash(msg, "danger")
                return redirect(url_for('institutes'))

            else:
                ingresar_institucionBDD(session['username'], session['password'], nombre, ciudad, descripcion)
                msg = 'Institución ingresada correctamente'
                flash(msg, "success")
                return redirect(url_for('institutes'))
    else:
        abort(401)

@app.route("/add_group_to_user", methods=['POST'])
def add_group_to_user():
    if 'username' in session and session['usertype'] == 'A':
        if request.method == 'POST':
            idt = request.form['usuarioID']
            user = request.form['userInvest']
            grupo = request.form['grupoSecundario']

            grupo_inv = comprobar_grupos_investigador(session['username'], session['password'], grupo, idt)

            if grupo_inv:
                msg = 'El investigador ya pertenece al grupo seleccionado'
                flash(msg, "danger")
                return redirect(url_for('users'))

            else:
                connectionOS = nuevo_grupo_investigadorOS(session['username'], session['password'], grupo, user)

                if connectionOS == True:
                    nuevo_grupo_investigadorBDD(session['username'], session['password'], grupo, idt)
                    msg = 'El grupo: ' + grupo + ' ' + 'fue asignado a ' + user
                    flash(msg, "success")
                    return redirect(url_for('users'))

                elif connectionOS == False:
                    msg = 'Ocurrio un error durante la asignacion de grupo'
                    flash(msg, "danger")
                    return redirect(url_for('users'))
    else:
        abort(401)

if __name__=='__main__':
    csrf.init_app(app)
    app.run(port='5000')