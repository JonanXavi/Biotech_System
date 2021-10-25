import mysql.connector
from mysql.connector import Error

HOST='192.168.100.150'

def mostrar_archivos(usuario, contrasena, nombre):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            port=3306,
            user=usuario,
            password=contrasena,
            db='biologia'
        )
        
        archivos = []

        cursor = connection.cursor()
        cursor.execute("SELECT ARCHNOMBRE, ARCHDESCRIPCION FROM ARCHIVO WHERE CARNOMBRE = %s", (nombre,))
        archivos = cursor.fetchall()
        cursor.close()
        connection.close()
        print("La conexión ha finalizado.")
        print(archivos)          

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))
    
    return archivos

def obtener_archivo_id():
    pass

def cambiar_permisos_archivo():
    pass

def compartir_archivo():
    pass

def descargar_archivo():
    pass

def subir_archivos():
    pass