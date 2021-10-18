import mysql.connector
from mysql.connector import Error

def mostrar_carpetas(usuario, contrasena):
    try:
        connection = mysql.connector.connect(
            host='192.168.100.153',
            port=3306,
            user=usuario,
            password=contrasena,
            db='biologia'
        )
        
        carpetas = []

        cursor = connection.cursor()
        cursor.execute("SELECT CARNOMBRE, CARDESCRIPCION FROM CARPETA")
        carpetas = cursor.fetchall()
        cursor.close()
        connection.close()
        print("La conexión ha finalizado.")
        print(carpetas)           

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))
    
    return carpetas

def mostrar_archivos(usuario, contrasena):
    try:
        connection = mysql.connector.connect(
            host='192.168.100.153',
            port=3306,
            user=usuario,
            password=contrasena,
            db='biologia'
        )
        
        archivos = []

        cursor = connection.cursor()
        cursor.execute("SELECT ARCHNOMBRE, ARCHDESCRIPCION FROM ARCHIVO")
        archivos = cursor.fetchall()
        cursor.close()
        connection.close()
        print("La conexión ha finalizado.")
        print(archivos)           

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))
    
    return archivos

def mostrar_archivo_nombre():
    pass

def compartir_archivo():
    pass

def descargar_archivo():
    pass

def subir_archivos():
    pass

def inicio_sesion(usuario, contrasena):

    try:
        connection = mysql.connector.connect(
            host='192.168.100.153',
            port=3306,
            user=usuario,
            password=contrasena,
            db='biologia'
        )
        
        connection.close()
        print("La conexión ha finalizado.")      

    except Error as ex:
        connection = None
        print("Error durante la conexión: {}".format(ex))

    return connection