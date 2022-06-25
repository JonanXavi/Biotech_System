import mysql.connector
from mysql.connector import Error
import paramiko
import time
from flask import current_app as app

def comprobar_carpetas_home(usuario, contrasena):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=app.config['HOST'], port=22, username=usuario, password=contrasena)
        entrada, salida, error = ssh_client.exec_command('ls -d */')
        time.sleep(1)
        lista = salida.read().decode().replace('/\n', ',')
        ssh_client.close()
        carpetasLinux = lista.split(',')
        carpetasLinux.pop() 

        connection = mysql.connector.connect(
            host=app.config['HOST'],
            port=app.config['PORT'],
            user=usuario,
            password=contrasena,
            db=app.config['BD']
        )

        cursor = connection.cursor()
        cursor.execute("SELECT INVIDENTIFICACION, INVPATHHOME, INVTIPO FROM INVESTIGADOR WHERE INVUSUARIO = %s", (usuario,))
        infoInvestigador = cursor.fetchone()

        if infoInvestigador[2] == 'I':
            cursor.execute("SELECT GRPNOMBRE FROM GRUPO_INVESTIGADOR WHERE INVIDENTIFICACION = %s AND GRPITIPO = %s", (infoInvestigador[0], 'P',))
            grupo = cursor.fetchone()

            cursor.execute("SELECT CONTNOMBRE FROM CONTENIDO WHERE INVIDENTIFICACION = %s AND CONTTIPO = %s AND CONTDIRECTORIO = %s", (infoInvestigador[0], 'C', infoInvestigador[1],))
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
                    path = infoInvestigador[1] + '/' + item
                    cursor.execute('INSERT INTO CONTENIDO VALUES (%s, %s, %s, %s, %s, DEFAULT, DEFAULT, DEFAULT, %s, %s)', (item, infoInvestigador[0], grupo[0], '', path, 'C', infoInvestigador[1],)) 
            else:
                print('No existen carpetas nuevas')

            cursor.close()
            connection.commit()
            connection.close()
            
        elif infoInvestigador[2] == 'A':
            cursor.close()
            connection.close()

    except paramiko.ssh_exception.AuthenticationException as e:
        print('Autenticación Fallida')

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

def comprobar_subcarpetas(usuario, contrasena, path):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(app.config['HOST'], port=22, username=usuario, password=contrasena)
        comando = 'cd ' + path + '/ ' + '\n ls -d */'
        entrada, salida, error = ssh_client.exec_command(comando)
        time.sleep(1)
        lista = salida.read().decode().replace('/\n', ',')
        ssh_client.close()
        carpetasLinux = lista.split(',')
        carpetasLinux.pop()

        connection = mysql.connector.connect(
            host=app.config['HOST'],
            port=app.config['PORT'],
            user=usuario,
            password=contrasena,
            db=app.config['BD']
        )

        cursor = connection.cursor()
        cursor.execute("SELECT INVIDENTIFICACION FROM INVESTIGADOR WHERE INVUSUARIO = %s", (usuario,))
        infoInvestigador = cursor.fetchone()

        cursor.execute("SELECT GRPNOMBRE FROM GRUPO_INVESTIGADOR WHERE INVIDENTIFICACION = %s AND GRPITIPO = %s", (infoInvestigador[0], 'P',))
        grupo = cursor.fetchone()

        cursor.execute("SELECT CONTNOMBRE FROM CONTENIDO WHERE INVIDENTIFICACION = %s AND CONTTIPO = %s AND CONTDIRECTORIO = %s", (infoInvestigador[0], 'C', path,))
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
                pathS = path + '/' + item
                cursor.execute('INSERT INTO CONTENIDO VALUES (%s, %s, %s, %s, %s, DEFAULT, DEFAULT, DEFAULT, %s, %s)', (item, infoInvestigador[0], grupo[0], '', pathS, 'C', path,)) 

        else:
            print('No existen carpetas nuevas')

        cursor.close()
        connection.commit()
        connection.close()

    except paramiko.ssh_exception.AuthenticationException as e:
        print('Autenticación Fallida')

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

def actualizar_info_carpeta(usuario, contrasena, descripcion, opcion, nombre):
    try:
        connection = mysql.connector.connect(
            host=app.config['HOST'],
            port=app.config['PORT'],
            user=usuario,
            password=contrasena,
            db=app.config['BD']
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("UPDATE CONTENIDO SET CONTDESCRIPCION = %s, CONTPRIVADO = %s WHERE CONTNOMBRE = %s", (descripcion, opcion, nombre,))
            cursor.close()

    except Error as ex:
        actualizar = False
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.commit()
            connection.close()
            actualizar = True
            print("La conexión ha finalizado.")

    return actualizar

def nombre_carpeta(usuario, contrasena, nombre):
    try:
        connection = mysql.connector.connect(
            host=app.config['HOST'],
            port=app.config['PORT'],
            user=usuario,
            password=contrasena,
            db=app.config['BD']
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT CONTNOMBRE FROM CONTENIDO WHERE CONTNOMBRE = %s", (nombre,))
            carpeta = cursor.fetchone()
            cursor.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.close()
            print("La conexión ha finalizado.")

    return carpeta

def nueva_carpetaOS(usuario, contrasena, path, nombre):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=app.config['HOST'], port=22, username=usuario, password=contrasena)
        permisos = 'chmod 770 ' + path + '/' + nombre
        entrada, salida, error = ssh_client.exec_command('mkdir ' + path + '/' + nombre + '\n' + permisos)
        time.sleep(1)
        ssh_client.close()

        connectionOS = True

    except paramiko.ssh_exception.AuthenticationException as e:
        connectionOS = False
        print('Autenticación Fallida')

    return connectionOS

def nueva_carpetaBDD(usuario, contrasena, path, nombre, descripcion):
    try:
        connection = mysql.connector.connect(
            host=app.config['HOST'],
            port=app.config['PORT'],
            user=usuario,
            password=contrasena,
            db=app.config['BD']
        )

        cursor = connection.cursor()
        cursor.execute("SELECT INVIDENTIFICACION FROM INVESTIGADOR WHERE INVUSUARIO = %s", (usuario,))
        info = cursor.fetchone()

        cursor.execute("SELECT GRPNOMBRE FROM GRUPO_INVESTIGADOR WHERE INVIDENTIFICACION = %s AND GRPITIPO = %s", (info[0], 'P',))
        grupo = cursor.fetchone()

        pathCarpeta = path + '/' + nombre

        cursor.execute('INSERT INTO CONTENIDO VALUES (%s, %s, %s, %s, %s, DEFAULT, DEFAULT, DEFAULT, %s, %s)', (nombre, info[0], grupo[0], descripcion, pathCarpeta, 'C', path,))
        cursor.close()
        connection.commit()
        connection.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

def carpeta_descargas(usuario, contrasena):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=app.config['HOST'], port=22, username=usuario, password=contrasena)
        permisos = 'chmod 770 /Descargas_' + usuario
        entrada, salida, error = ssh_client.exec_command('mkdir Descargas_' + usuario + '\n' + permisos)
        time.sleep(1)
        ssh_client.close()

    except paramiko.ssh_exception.AuthenticationException as e:
        print('Autenticación Fallida')