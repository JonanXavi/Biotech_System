import mysql.connector
from mysql.connector import Error

def insertar_archivos():
    pass

def mostrar_archivos():
    pass

def mostrar_archivo_nombre():
    pass

def compartir_archivo():
    pass

def descargar_archivo():
    pass

def subir_archivos():
    pass

def conectar_bdd(usuario, contrasena):

    try:
        connection = mysql.connector.connect(
            host='192.168.100.150',
            port=3306,
            user=usuario,
            password=contrasena,
            db='biologia'
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM INVESTIGADOR")
        row = cursor.fetchall()
        cursor.close()
        connection.close()
        print("La conexión ha finalizado.")
        print(row)           

    except Error as ex:
        connection = None
        print("Error durante la conexión: {}".format(ex))

    return connection