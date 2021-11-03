import mysql.connector
from mysql.connector import Error

HOST='192.168.100.150'

def inicio_sesion(usuario, contrasena):

    try:
        connection = mysql.connector.connect(
            host=HOST,
            port=3306,
            user=usuario,
            password=contrasena,
            db='biologia'
        )
        
        connection.close() 

    except Error as ex:
        connection = None
        print("Error durante la conexión: {}".format(ex))

    return connection

def tipo_usuario(usuario, contrasena):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            port=3306,
            user=usuario,
            password=contrasena,
            db='biologia'
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT INVTIPO FROM INVESTIGADOR WHERE INVUSUARIO = %s", (usuario,))
        tipoUsuario = cursor.fetchone()
        cursor.close()
        connection.close()
        print("La conexión ha finalizado.")   

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    return tipoUsuario