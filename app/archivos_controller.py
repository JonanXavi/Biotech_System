import mysql.connector
from mysql.connector import Error
from pathlib import Path
from flask import current_app as app

import paramiko
import time
import os

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpge"])

def comprobar_archivos_home(usuario, contrasena):
    try:
        connection = mysql.connector.connect(
            host=app.config['HOST'],
            port=app.config['PORT'],
            user=usuario,
            password=contrasena,
            db=app.config['BD']
        )

        cursor = connection.cursor()
        cursor.execute("SELECT INVIDENTIFICACION, INVPATHHOME FROM INVESTIGADOR WHERE INVUSUARIO = %s", (usuario,))
        infoInvestigador = cursor.fetchone()

        cursor.execute("SELECT GRPNOMBRE FROM GRUPO_INVESTIGADOR WHERE INVIDENTIFICACION = %s AND GRPITIPO = %s", (infoInvestigador[0], 'P',))
        grupo = cursor.fetchone()

        cursor.execute("SELECT CONTNOMBRE FROM CONTENIDO WHERE INVIDENTIFICACION = %s AND CONTTIPO = %s AND CONTDIRECTORIO = %s", (infoInvestigador[0], 'A', infoInvestigador[1],))
        archivosbd = cursor.fetchall()

        archivos = set().union(*archivosbd)

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=app.config['HOST'], port=22, username=usuario, password=contrasena)
        entrada, salida, error = ssh_client.exec_command('cd ' + infoInvestigador[1] + '/' + ' \n ls -p | grep -v /')
        time.sleep(1)
        lista = salida.read().decode().replace('\n', ',')
        archivosLinux = lista.split(',')
        archivosLinux.pop()
        sftp = ssh_client.open_sftp()

        nuevosArchivos = []

        for item1 in archivosLinux:
            x = True
            for item2 in archivos:
                if item2 in item1:
                    x = False
                    break
            if x:
                nuevosArchivos.append(item1)

        if len(nuevosArchivos) != 0:
            for item in nuevosArchivos:
                pathArchivo = infoInvestigador[1] + '/' + item
                sftp.chmod(pathArchivo, 0o770)
                cursor.execute('INSERT INTO CONTENIDO VALUES (%s, %s, %s, %s, %s, DEFAULT, DEFAULT, DEFAULT, %s, %s)', (item, infoInvestigador[0], grupo[0], '', pathArchivo, 'A', infoInvestigador[1],))              
        else:
            print('No existen archivos nuevos')

        sftp.close()
        ssh_client.close()
        cursor.close()
        connection.commit()
        connection.close()

    except paramiko.ssh_exception.AuthenticationException as e:
        print('Autenticación Fallida')

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

def comprobar_archivos_subcarpeta(usuario, contrasena, path):
    try:
        connection = mysql.connector.connect(
            host=app.config['HOST'],
            port=app.config['PORT'],
            user=usuario,
            password=contrasena,
            db=app.config['BD']
        )

        cursor = connection.cursor()
        cursor.execute("SELECT INVIDENTIFICACION, INVPATHHOME FROM INVESTIGADOR WHERE INVUSUARIO = %s", (usuario,))
        infoInvestigador = cursor.fetchone()

        cursor.execute("SELECT GRPNOMBRE FROM GRUPO_INVESTIGADOR WHERE INVIDENTIFICACION = %s AND GRPITIPO = %s", (infoInvestigador[0], 'P',))
        grupo = cursor.fetchone()

        cursor.execute("SELECT CONTNOMBRE FROM CONTENIDO WHERE INVIDENTIFICACION = %s AND CONTTIPO = %s AND CONTDIRECTORIO = %s", (infoInvestigador[0], 'A', path,))
        archivosbd = cursor.fetchall()

        archivos = set().union(*archivosbd)

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=app.config['HOST'], port=22, username=usuario, password=contrasena)
        entrada, salida, error = ssh_client.exec_command('cd ' + path + '/' + ' \n ls -p | grep -v /')
        time.sleep(1)
        lista = salida.read().decode().replace('\n', ',')
        archivosLinux = lista.split(',')
        archivosLinux.pop()
        sftp = ssh_client.open_sftp()

        nuevosArchivos = []

        for item1 in archivosLinux:
            x = True
            for item2 in archivos:
                if item2 in item1:
                    x = False
                    break
            if x:
                nuevosArchivos.append(item1)

        if len(nuevosArchivos) != 0:
            for item in nuevosArchivos:
                if path == infoInvestigador[1] + '/Descargas_' + usuario:
                    nombre = usuario + '_' + item
                    pathArchivo = path + '/' + item
                    sftp.chmod(pathArchivo, 0o770)
                    cursor.execute('INSERT INTO CONTENIDO VALUES (%s, %s, %s, %s, %s, DEFAULT, DEFAULT, DEFAULT, %s, %s)', (nombre, infoInvestigador[0], grupo[0], '', pathArchivo, 'A', path,))

                else:
                    pathArchivo = path + '/' + item
                    sftp.chmod(pathArchivo, 0o770)
                    cursor.execute('INSERT INTO CONTENIDO VALUES (%s, %s, %s, %s, %s, DEFAULT, DEFAULT, DEFAULT, %s, %s)', (item, infoInvestigador[0], grupo[0], '', pathArchivo, 'A', path,))              
        else:
            print('No existen archivos nuevos')

        sftp.close()
        ssh_client.close()
        cursor.close()
        connection.commit()
        connection.close()

    except paramiko.ssh_exception.AuthenticationException as e:
        print('Autenticación Fallida')

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

def actualizar_info_archivo(usuario, contrasena, descripcion, publicable, descarga, nombre):
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
            cursor.execute("UPDATE CONTENIDO SET CONTDESCRIPCION = %s, CONTPRIVADO = %s, CONTDESCARGA = %s WHERE CONTNOMBRE = %s", (descripcion, publicable, descarga, nombre,))
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

def descargar_archivo(usuario, contrasena, nombre):
    try:
        connection = mysql.connector.connect(
            host=app.config['HOST'],
            port=app.config['PORT'],
            user=usuario,
            password=contrasena,
            db=app.config['BD']
        )

        cursor = connection.cursor()
        cursor.execute("SELECT CONTNOMBRE, CONTPATH, CONTNUMERODESCARGAS, CONTDESCARGA FROM CONTENIDO WHERE CONTNOMBRE = %s", (nombre,))
        infoArchivo = cursor.fetchone()

        if infoArchivo[3] == 'N':
            resp = False

        elif infoArchivo[3] == 'S':
            try:
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=app.config['HOST'], port=22, username=usuario, password=contrasena)
                sftp = ssh_client.open_sftp()

                if os.name == 'nt':
                    pathDescarga = str(Path.home()) + '\\' + 'Downloads' + '\\' + infoArchivo[0]
                    sftp.get(infoArchivo[1], pathDescarga)

                elif os.name == 'posix':
                    pathDescarga = str(Path.home()) + '/' + 'Descargas_' + usuario + '/' + infoArchivo[0]
                    sftp.get(infoArchivo[1], pathDescarga)

                contador = int(infoArchivo[2]) + 1
                cursor.execute("UPDATE CONTENIDO SET CONTNUMERODESCARGAS = %s WHERE CONTNOMBRE = %s", (contador, infoArchivo[0],))
                sftp.close()
                ssh_client.close()
                resp = True

            except paramiko.ssh_exception.AuthenticationException as e:
                print('Autenticación Fallida')

        cursor.close()
        connection.commit()
        connection.close()

        return resp

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

def nombre_archivo(usuario, contrasena, nombre):
    try:
        connection = mysql.connector.connect(
            host=app.config['HOST'],
            port=app.config['PORT'],
            user=usuario,
            password=contrasena,
            db=app.config['BD']
        )

        cursor = connection.cursor()
        cursor.execute("SELECT CONTNOMBRE FROM CONTENIDO WHERE CONTNOMBRE = %s", (nombre,))
        archivo = cursor.fetchone()
        cursor.close()
        connection.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    return archivo

def subir_archivos(usuario, contrasena, path, archivo, nombreArchivo):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=app.config['HOST'], port=22, username=usuario, password=contrasena)
        sftp = ssh_client.open_sftp()
        sftp.chdir(path)
        sftp.put(archivo, nombreArchivo)
        sftp.close()
        ssh_client.close()

    except paramiko.ssh_exception.AuthenticationException as e:
        print('Autenticación Fallida')

def nombre_archivo_compartido(usuario, contrasena, nombre):
    try:
        connection = mysql.connector.connect(
            host=app.config['HOST'],
            port=app.config['PORT'],
            user=usuario,
            password=contrasena,
            db=app.config['BD']
        )

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM ARCHIVOS_COMPARTIDOS WHERE CONTNOMBRE = %s", (nombre,))
        archivoC = cursor.fetchone()
        cursor.close()
        connection.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    return archivoC

def compartir_archivo(usuario, contrasena, idt, nombre):
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
            cursor.execute('INSERT INTO ARCHIVOS_COMPARTIDOS VALUES (%s, %s)', (idt, nombre))
            cursor.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.commit()
            connection.close()
            print("La conexión ha finalizado.")

def archivos_compartidos(usuario, contrasena):
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
        idt = cursor.fetchone()

        cursor.execute("SELECT ARCHIVOS_COMPARTIDOS.CONTNOMBRE, CONTENIDO.CONTDESCRIPCION FROM ARCHIVOS_COMPARTIDOS INNER JOIN CONTENIDO ON ARCHIVOS_COMPARTIDOS.CONTNOMBRE = CONTENIDO.CONTNOMBRE WHERE ARCHIVOS_COMPARTIDOS.INVIDENTIFICACION = %s", (idt[0],))
        archivos = cursor.fetchall()

        cursor.close()
        connection.close()
        print("La conexión ha finalizado.")     

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))
    
    return archivos

def verificar_foto(archivo):
    return '.' in archivo and archivo.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS