import mysql.connector
from mysql.connector import Error
import paramiko
import time

HOST='192.168.100.150'
#HOST='172.16.0.63'

def comprobar_carpetas(usuario, contrasena):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=HOST, port=22, username=usuario, password=contrasena)
        entrada, salida, error = ssh_client.exec_command('ls -I Documentos -I Escritorio -I Imágenes -I Plantillas -I Público -I Música -I Vídeos')
        time.sleep(1)
        lista = salida.read().decode().replace('\n', ',')
        ssh_client.close()
        carpetasLinux = lista.split(',')
        carpetasLinux.pop()

        for x in range(len(carpetasLinux)):
            if carpetasLinux[x] == 'Descargas':
                carpetasLinux[x] = 'Descargas_' + usuario        

        connection = mysql.connector.connect(
            host=HOST,
            port=3306,
            user=usuario,
            password=contrasena,
            db='biologia'
        )

        cursor = connection.cursor()
        cursor.execute("SELECT INVCEDULA, INVPATHHOME, INVTIPO FROM INVESTIGADOR WHERE INVUSUARIO = %s", (usuario,))
        infoInvestigador = cursor.fetchone()

        ci = infoInvestigador[0]
        tipo = infoInvestigador[2]

        if tipo == 'I':
            cursor.execute("SELECT GRPNOMBRE FROM GRUPO_INVESTIGADOR WHERE INVCEDULA = %s AND GRPITIPO = 'P'", (ci,))
            grupo = cursor.fetchone()

            grupoPrincipal = grupo[0]
            carpetasbd = []

            cursor.execute("SELECT CARNOMBRE FROM CARPETA WHERE INVCEDULA = %s", (ci,))
            carpetasbd = cursor.fetchall()

            carpetas = set().union(*carpetasbd)
            nuevasCarpetas = []

            for item1 in carpetasLinux:
                x = True
                for item2 in carpetas:
                    if item2 in item1:
                        x = False
                        break
                if x:
                    nuevasCarpetas.append(item1)

            if len(nuevasCarpetas) != 0:
                for item in nuevasCarpetas:
                    if item == 'Descargas_' + usuario:
                        path = infoInvestigador[1] + '/' + 'Descargas'
                        cursor.execute('INSERT INTO CARPETA VALUES (%s, %s, %s, %s, %s, DEFAULT)', (item, ci, grupoPrincipal, '', path))

                    else:
                        path = infoInvestigador[1] + '/' + item
                        cursor.execute('INSERT INTO CARPETA VALUES (%s, %s, %s, %s, %s, DEFAULT)', (item, ci, grupoPrincipal, '', path))              
            else:
                print('No existen carpetas nuevas')

            cursor.close()
            connection.commit()
            connection.close()
            
        elif tipo == 'A':
            cursor.close()
            connection.close()

    except paramiko.ssh_exception.AuthenticationException as e:
        print('Autenticación Fallida')

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

def mostrar_carpetas(usuario, contrasena):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            port=3306,
            user=usuario,
            password=contrasena,
            db='biologia'
        )
        
        carpetas = []

        cursor = connection.cursor()
        cursor.execute("SELECT INVCEDULA FROM INVESTIGADOR WHERE INVUSUARIO = %s", (usuario,))
        ci = cursor.fetchone()

        cursor.execute("SELECT CARNOMBRE, GRPNOMBRE, CARDESCRIPCION, CARPRIVADO FROM CARPETA WHERE INVCEDULA = %s", (ci[0],))
        carpetas = cursor.fetchall()
        cursor.close()
        connection.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))
    
    return carpetas

def actualizar_info_carpeta(usuario, contrasena, descripcion, opcion, nombre):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            port=3306,
            user=usuario,
            password=contrasena,
            db='biologia'
        )

        cursor = connection.cursor()
        cursor.execute("UPDATE CARPETA SET CARDESCRIPCION = %s, CARPRIVADO = %s WHERE CARNOMBRE = %s", (descripcion, opcion, nombre,))
        cursor.close()
        connection.commit()
        connection.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

def nombre_carpeta(usuario, contrasena, nombre):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            port=3306,
            user=usuario,
            password=contrasena,
            db='biologia'
        )

        cursor = connection.cursor()
        cursor.execute("SELECT CARNOMBRE FROM CARPETA WHERE CARNOMBRE = %s", (nombre,))
        carpeta = cursor.fetchone()
        cursor.close()
        connection.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    return carpeta

def nueva_carpetaOS(usuario, contrasena, nombre):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=HOST, port=22, username=usuario, password=contrasena)
        permisos = 'chmod 770 ' + nombre
        entrada, salida, error = ssh_client.exec_command('mkdir ' + nombre + '\n' + permisos)
        time.sleep(1)
        ssh_client.close()

        connectionOS = True

    except paramiko.ssh_exception.AuthenticationException as e:
        connectionOS = False
        print('Autenticación Fallida')

    return connectionOS

def nueva_carpetaBDD(usuario, contrasena, nombre, descripcion):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            port=3306,
            user=usuario,
            password=contrasena,
            db='biologia'
        )

        cursor = connection.cursor()
        cursor.execute("SELECT INVCEDULA, INVPATHHOME FROM INVESTIGADOR WHERE INVUSUARIO = %s", (usuario,))
        info = cursor.fetchone()

        ci = info[0]
        path = info[1]

        cursor.execute("SELECT GRPNOMBRE FROM GRUPO_INVESTIGADOR WHERE INVCEDULA = %s AND GRPITIPO = %s", (ci, 'P',))
        grupo = cursor.fetchone()

        grupoPrincipal = grupo[0]
        pathCarpeta = path + '/' + nombre

        cursor.execute('INSERT INTO CARPETA VALUES (%s, %s, %s, %s, %s, DEFAULT)', (nombre, ci, grupoPrincipal, descripcion, pathCarpeta))
        cursor.close()
        connection.commit()
        connection.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))