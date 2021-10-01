from flask import Flask, render_template, redirect, request, url_for, session
from flask_wtf import CSRFProtect 
import cx_Oracle

import config

from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
csrf = CSRFProtect(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():

    msg = ''
    connection = None

    if 'username' in session:
        return render_template('panel.html')
    elif request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        try:
            connection = cx_Oracle.connect(username, password, config.dsn, encoding=config.encoding)           
            cursor = connection.cursor()
            '''cursor.execute("select * from tab")
            rows = cursor.fetchall()
            for row in rows:
                print(row)'''
            cursor.close()
            connection.close()
            
        except Exception as ex:
            print("Error durante la conexión: {}".format(ex))

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