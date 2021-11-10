import mysql.connector
from mysql.connector import Error

#HOST='192.168.100.150'
HOST='172.16.0.63'

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

def info_investigadores(usuario, contrasena):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            port=3306,
            user=usuario,
            password=contrasena,
            db='biologia'
        )

        investigadores = []

        cursor = connection.cursor()
        cursor.execute("SELECT INVCEDULA, INVNOMBRES, INVAPELLIDOS FROM INVESTIGADOR WHERE INVTIPO = %s EXCEPT SELECT INVCEDULA, INVNOMBRES, INVAPELLIDOS FROM INVESTIGADOR WHERE INVUSUARIO = %s", ('I', usuario,))
        investigadores = cursor.fetchall()
        cursor.close()
        connection.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    return investigadores

def info_grupos(usuario, contrasena, ci):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            port=3306,
            user=usuario,
            password=contrasena,
            db='biologia'
        )

        cursor = connection.cursor()
        cursor.execute("SELECT INVCEDULA FROM INVESTIGADOR WHERE INVUSUARIO = %s", (usuario,))
        propietario = cursor.fetchone()

        cursor.execute("SELECT GRPNOMBRE FROM GRUPO_INVESTIGADOR WHERE INVCEDULA = %s AND GRPITIPO = %s", (propietario[0], 'P',))
        propietarioGrupo = cursor.fetchone()

        cursor.execute("SELECT GRPNOMBRE FROM GRUPO_INVESTIGADOR WHERE INVCEDULA = %s", (ci,))
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