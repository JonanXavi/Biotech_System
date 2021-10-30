from flask import Flask, render_template, redirect, request, url_for, session, current_app
from flask_wtf import CSRFProtect
from config import DevelopmentConfig

from bdd_controller import inicio_sesion
from carpetas_controller import comprobar_carpetas, mostrar_carpetas, actualizar_info_carpeta
from archivos_controller import comprobar_archivos, mostrar_archivos, actualizar_info_archivo

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)

@app.route("/")
@app.route("/inicio")
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():

    msg = ''

    if 'username' in session:
        return redirect(url_for('folder'))
    elif request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        connection = inicio_sesion(username, password)

        if connection is not None:
            session['username'] = username
            session['password'] = password

            comprobar_carpetas(username, password)

            return redirect(url_for('folder'))
        else:
            msg = 'Usuario o contraseña incorrecto'

    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
        session.pop('password', None)
    return redirect(url_for('index'))

@app.route("/recover")
def recover():
    return render_template('password.html')

@app.route("/folders")
def folder():
    if 'username' in session:
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

@app.route("/files", methods=['POST'])
def file():
    if 'username' in session:
        comprobar_archivos(session['username'], session['password'], request.form["nombre"])
        archivos = mostrar_archivos(session['username'], session['password'], request.form["nombre"])

        return render_template('file.html', carpeta=request.form["nombre"], archivos=archivos)
        
    return redirect(url_for('login'))

@app.route("/update_file", methods=['POST'])
def update_info_file():
    if 'username' in session:
        if request.method == 'POST' and 'descripcion-archivo' in request.form:
            nombre = request.form['nombreArchivo']
            descripcion = request.form['descripcion-archivo']
            publicable = 'S' if 'publicable' in request.form else 'N'
            compartir = 'S' if 'compartir' in request.form else 'N'
            descarga = 'S' if 'op-descarga' in request.form else 'N'

            actualizar_info_archivo(session['username'], session['password'], descripcion, publicable, compartir, descarga, nombre)
            return redirect(url_for('folder'))

    return redirect(url_for('login'))

if __name__=='__main__':
    csrf.init_app(app)
    app.run(port='5000')