import mysql.connector
from mysql.connector import Error
import paramiko
import time

HOST='192.168.100.150'

def comprobar_archivos(usuario, contrasena, nombre):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            port=3306,
            user=usuario,
            password=contrasena,
            db='biologia'
        )

        cursor = connection.cursor()
        cursor.execute("SELECT INVPATHHOME FROM INVESTIGADOR WHERE INVUSUARIO = %s", (usuario,))
        infoPath = cursor.fetchone()

        path = infoPath[0]

        cursor.execute("SELECT ARCHNOMBRE FROM ARCHIVO WHERE CARNOMBRE = %s", (nombre,))
        archivosbd = cursor.fetchall()

        archivos = set().union(*archivosbd)

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=HOST, port=22, username=usuario, password=contrasena)
        entrada, salida, error = ssh_client.exec_command('cd ' + path + '/' + nombre + '/' + ' \n ls -p | grep -v /')
        time.sleep(1)
        lista = salida.read().decode().replace('\n', ',')
        archivosLinux = lista.split(',')
        archivosLinux.pop()
        ssh_client.close()

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
                pathArchivo = path + '/' + nombre + '/' + item
                cursor.execute('INSERT INTO ARCHIVO VALUES (%s, %s, %s, %s, DEFAULT, DEFAULT, DEFAULT, DEFAULT)', (item, nombre, '', pathArchivo))              
        else:
            print('No existen archivos nuevos')

        cursor.close()
        connection.commit()
        connection.close()

    except paramiko.ssh_exception.AuthenticationException as e:
        print('Autenticación Fallida')

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

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