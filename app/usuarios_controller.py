import mysql.connector
from mysql.connector import Error
import paramiko
import time

HOST='192.168.100.156'
#HOST='172.16.0.63'

def info_usuarios(usuario, contrasena):
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
            cursor.execute("SELECT INSNOMBRE, INVNOMBRES, INVAPELLIDOS, INVCORREOINSTITUCIONAL FROM INVESTIGADOR WHERE INVTIPO = %s", ('I',))
            investigadores = cursor.fetchall()
            cursor.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.close()
            print("La conexión ha finalizado.")   

    return investigadores

def comprobar_usuario(usuario, contrasena, ci):
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
            cursor.execute("SELECT * FROM INVESTIGADOR WHERE INVCEDULA = %s", (ci,))
            investigador = cursor.fetchone()
            cursor.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.close()
            print("La conexión ha finalizado.")

    return investigador  

def ingresar_usuarioOS(usuario, contrasena):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=HOST, port=22, username=usuario, password=contrasena)
        #comando = 
        comando = 'echo %s | sudo -Siptables -nL' % contrasena
        entrada, salida, error = ssh_client.exec_command(comando)
        print(entrada.read())
        print(salida.read())
        print(error.read())

        #permisos = 'chmod 770 ' + nombre
        #entrada, salida, error = ssh_client.exec_command('mkdir ' + nombre + '\n' + permisos)
        #time.sleep(1)
        ssh_client.close()

        connectionOS = True

    except paramiko.ssh_exception.AuthenticationException as e:
        connectionOS = False
        print('Autenticación Fallida')

    return connectionOS

def ingresar_usuarioBDD(usuario, contrasena, user, passw):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            port=3306,
            user=usuario,
            password=contrasena,
            db='mysql'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            sql = 'create user ' + '\'' + user + '\'' + '@\'%\' identified by ' + '\'' + passw + '\''
            cursor.execute(sql)
            sql = 'grant select, insert, update on biologia.CARPETA to ' + '\'' + user + '\'' + '@\'%\''
            cursor.execute(sql)
            sql = 'grant select, insert, update on biologia.ARCHIVO to ' + '\'' + user + '\'' + '@\'%\''
            cursor.execute(sql)
            sql = 'grant select, update on biologia.INVESTIGADOR to ' + '\'' + user + '\'' + '@\'%\''
            cursor.execute(sql)
            sql = 'grant select on biologia.GRUPO_INVESTIGADOR to ' + '\'' + user + '\'' + '@\'%\''
            cursor.execute(sql)
            sql = 'grant select, insert on biologia.ARCHIVOS_COMPARTIDOS to ' + '\'' + user + '\'' + '@\'%\''
            cursor.execute(sql)
            sql = 'flush privileges'
            cursor.execute(sql)
            cursor.close()

    except Error as ex:
        conexion = False
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.commit()
            connection.close()
            conexion = True
            print("La conexión ha finalizado.")

    return conexion

def registrar_usuarioBDD(usuario, contrasena, ci, instituto, user, nombre, apellido, correo):
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
            path = '/home/' + user
            cursor.execute('INSERT INTO INVESTIGADOR VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, DEFAULT)', (ci, instituto, user, nombre, apellido, correo, '', '', '', path))
            cursor.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.commit()
            connection.close()
            print("La conexión ha finalizado.") 