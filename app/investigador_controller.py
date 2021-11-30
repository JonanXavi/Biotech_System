import mysql.connector
from mysql.connector import Error

HOST='192.168.100.161'
#HOST='172.16.0.63'

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
        cursor.execute("SELECT INVTIPO, INVPATHHOME FROM INVESTIGADOR WHERE INVUSUARIO = %s", (usuario,))
        tipoUsuario = cursor.fetchone()
        cursor.close()
        connection.close()
        print("La conexión ha finalizado.")   

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    return tipoUsuario

def info_investigadores(usuario, contrasena):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            port=3306,
            user=usuario,
            password=contrasena,
            db='biologia'
        )

        cursor = connection.cursor()
        cursor.execute("SELECT INVIDENTIFICACION, INVNOMBRES, INVAPELLIDOS FROM INVESTIGADOR WHERE INVTIPO = %s EXCEPT SELECT INVIDENTIFICACION, INVNOMBRES, INVAPELLIDOS FROM INVESTIGADOR WHERE INVUSUARIO = %s", ('I', usuario,))
        investigadores = cursor.fetchall()
        cursor.close()
        connection.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    return investigadores

def info_grupos(usuario, contrasena, idt):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            port=3306,
            user=usuario,
            password=contrasena,
            db='biologia'
        )

        cursor = connection.cursor()
        cursor.execute("SELECT INVIDENTIFICACION FROM INVESTIGADOR WHERE INVUSUARIO = %s", (usuario,))
        propietario = cursor.fetchone()

        cursor.execute("SELECT GRPNOMBRE FROM GRUPO_INVESTIGADOR WHERE INVIDENTIFICACION = %s AND GRPITIPO = %s", (propietario[0], 'P',))
        propietarioGrupo = cursor.fetchone()

        cursor.execute("SELECT GRPNOMBRE FROM GRUPO_INVESTIGADOR WHERE INVIDENTIFICACION = %s", (idt,))
        personaGrupos = cursor.fetchall()
        grupos = set().union(*personaGrupos)

        if propietarioGrupo[0] in grupos:
            compartir = True
            
        else:
            compartir = False

        cursor.close()
        connection.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    return compartir

def perfil_investigador(usuario, contrasena):
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
            cursor.execute("SELECT INSNOMBRE, INVNOMBRES, INVAPELLIDOS, INVCORREOINSTITUCIONAL, INVURLRESEARCH, INVFOTO, INVBIOGRAFIA, INVTIPO FROM INVESTIGADOR WHERE INVUSUARIO = %s", (usuario,))
            infoPerfil = cursor.fetchone()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.close()
            print("La conexión ha finalizado.")   

    return infoPerfil

def actualizar_perfil(usuario, contrasena, url, bio):
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
            cursor.execute("UPDATE INVESTIGADOR SET INVURLRESEARCH = %s, INVBIOGRAFIA = %s WHERE INVUSUARIO = %s", (url, bio, usuario,))
            cursor.close()
            connection.commit()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.close()
            print("La conexión ha finalizado.")

def actualizar_foto(usuario, contrasena, foto):
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

            cursor.execute("UPDATE INVESTIGADOR SET INVFOTO = %s WHERE INVUSUARIO = %s", (foto, usuario,))
            cursor.close()
            connection.commit()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.close()
            print("La conexión ha finalizado.")