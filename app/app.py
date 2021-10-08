from flask import Flask, render_template, redirect, request, url_for, session
from flask_wtf import CSRFProtect
from config import DevelopmentConfig

import cx_Oracle
from controlador_archivos import conectar_bdd 

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
        return render_template('panel.html')
    elif request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        connection = conectar_bdd(username, password)

        if connection is not None:
            session['username'] = username
            session['password'] = password

            return redirect(url_for('panel'))
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

@app.route("/panel")
def panel():
    if 'username' in session:
        return render_template('panel.html')
        
    return redirect(url_for('login'))

if __name__=='__main__':
    csrf.init_app(app)
    app.run(port='5000')