import mysql.connector
from mysql.connector import Error

HOST='192.168.100.161'
#HOST='172.16.0.63'

def mostrar_contenido_home(usuario, contrasena):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            port=3306,
            user=usuario,
            password=contrasena,
            db='biologia'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT INVIDENTIFICACION, INVPATHHOME FROM INVESTIGADOR WHERE INVUSUARIO = %s", (usuario,))
            idt = cursor.fetchone()

            cursor.execute("SELECT CONTNOMBRE, GRPNOMBRE, CONTDESCRIPCION, CONTPATH, CONTPRIVADO, CONTDESCARGA, CONTNUMERODESCARGAS, CONTTIPO FROM CONTENIDO WHERE INVIDENTIFICACION = %s AND CONTDIRECTORIO = %s", (idt[0], idt[1],))
            contenido = cursor.fetchall()
            cursor.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.close()
            print("La conexión ha finalizado.")

    return contenido

def mostrar_contenido_subcarpeta(usuario, contrasena, path):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            port=3306,
            user=usuario,
            password=contrasena,
            db='biologia'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT INVIDENTIFICACION FROM INVESTIGADOR WHERE INVUSUARIO = %s", (usuario,))
            idt = cursor.fetchone()

            cursor.execute("SELECT CONTNOMBRE, GRPNOMBRE, CONTDESCRIPCION, CONTPATH, CONTPRIVADO, CONTDESCARGA, CONTNUMERODESCARGAS, CONTTIPO FROM CONTENIDO WHERE INVIDENTIFICACION = %s AND CONTDIRECTORIO = %s", (idt[0], path,))
            contenido = cursor.fetchall()
            cursor.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.close()
            print("La conexión ha finalizado.")

    return contenido