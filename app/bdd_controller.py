import mysql.connector
from mysql.connector import Error
from flask import current_app as app

def inicio_sesion(usuario, contrasena):
    try:
        connection = mysql.connector.connect(
            host=app.config['HOST'],
            port=app.config['PORT'],
            user=usuario,
            password=contrasena,
            db=app.config['BD']
        )
        conexion = True
        connection.close() 
        
    except Error as ex:
        conexion = False
        print("Error durante la conexión: {}".format(ex))

    return conexion