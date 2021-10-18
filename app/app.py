from flask import Flask, render_template, redirect, request, url_for, session
from flask_wtf import CSRFProtect
from config import DevelopmentConfig

from controlador_archivos import inicio_sesion, mostrar_carpetas, mostrar_archivos 

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)

@app.route("/")
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

@app.route("/folder")
def folder():
    if 'username' in session:
        carpetas = mostrar_carpetas(session['username'], session['password'])

        return render_template('folder.html', username=session['username'], carpetas=carpetas)
        
    return redirect(url_for('login'))

@app.route("/file")
def archivos():
    if 'username' in session:
        archivos = mostrar_archivos(session['username'], session['password'])

        return render_template('file.html', username=session['username'], archivos=archivos)
        
    return redirect(url_for('login'))

if __name__=='__main__':
    csrf.init_app(app)
    app.run(port='5000')