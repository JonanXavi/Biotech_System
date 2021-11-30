import mysql.connector
from mysql.connector import Error
import paramiko

HOST='192.168.100.161'
#HOST='172.16.0.63'

def info_ciudades(usuario, contrasena):
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
            cursor.execute("SELECT CIUCODIGO, CIUNOMBRE FROM CIUDAD")
            ciudades = cursor.fetchall()
            cursor.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.close()
            print("La conexión ha finalizado.")

    return ciudades

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
            cursor.execute("SELECT INVESTIGADOR.INVIDENTIFICACION, INVESTIGADOR.INVUSUARIO, INVESTIGADOR.INSNOMBRE, INVESTIGADOR.INVNOMBRES, INVESTIGADOR.INVAPELLIDOS, INVESTIGADOR.INVCORREOINSTITUCIONAL, GRUPO_INVESTIGADOR.GRPNOMBRE FROM INVESTIGADOR INNER JOIN GRUPO_INVESTIGADOR ON INVESTIGADOR.INVIDENTIFICACION = GRUPO_INVESTIGADOR.INVIDENTIFICACION WHERE INVESTIGADOR.INVTIPO = %s AND GRUPO_INVESTIGADOR.GRPITIPO = %s", ('I', 'P',))
            investigadores = cursor.fetchall()
            cursor.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.close()
            print("La conexión ha finalizado.")   

    return investigadores

def info_grupos_sistema(usuario, contrasena):
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
            cursor.execute("SELECT GRPNOMBRE, GRPDESCRIPCION FROM GRUPO")
            grupos = cursor.fetchall()
            cursor.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.close()
            print("La conexión ha finalizado.")

    return grupos

def info_instituciones(usuario, contrasena):
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
            cursor.execute("SELECT INSTITUCION.INSNOMBRE, CIUDAD.CIUNOMBRE, INSTITUCION.INSDESCRIPCION FROM INSTITUCION INNER JOIN CIUDAD ON INSTITUCION.CIUCODIGO = CIUDAD.CIUCODIGO")
            instituciones = cursor.fetchall()
            cursor.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.close()
            print("La conexión ha finalizado.")

    return instituciones

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
            cursor.execute("SELECT * FROM INVESTIGADOR WHERE INVIDENTIFICACION = %s", (ci,))
            investigador = cursor.fetchone()
            cursor.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.close()
            print("La conexión ha finalizado.")

    return investigador  

def ingresar_usuarioOS(usuario, contrasena, user, grupo):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=HOST, port=22, username=usuario, password=contrasena)
 
        ssh_client.get_transport()
 
        command = "sudo useradd " + user + " -g " + grupo
        entrada, salida, error = ssh_client.exec_command(command=command, get_pty=True)
        entrada.write(contrasena + "\n")
 
        entrada.flush()
 
        if error.channel.recv_exit_status() != 0:
            print(f"Ocurrió el siguiente error: {error.readlines()}")
            connectionOS = False
 
        else:
            print(f"Se creo correctamente el usuario")
            connectionOS = True
 
        ssh_client.close()
 
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
            sql = 'grant select, insert, update on biologia.CONTENIDO to ' + '\'' + user + '\'' + '@\'%\''
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

def registrar_usuarioBDD(usuario, contrasena, ci, instituto, user, grupo, nombre, apellido, correo):
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
            cursor.execute('INSERT INTO GRUPO_INVESTIGADOR VALUES (%s, %s, %s)', (grupo, ci, 'P'))
            cursor.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.commit()
            connection.close()
            print("La conexión ha finalizado.")

def comprobar_grupo(usuario, contrasena, nombre):
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
            cursor.execute("SELECT * FROM GRUPO WHERE GRPNOMBRE = %s", (nombre,))
            grupo = cursor.fetchone()
            cursor.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.close()
            print("La conexión ha finalizado.")

    return grupo

def ingresar_grupoOS(usuario, contrasena, nombre):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=HOST, port=22, username=usuario, password=contrasena)

        ssh_client.get_transport()

        command = "sudo groupadd " + nombre
        entrada, salida, error = ssh_client.exec_command(command=command, get_pty=True)
        entrada.write(contrasena + "\n")

        entrada.flush()

        if error.channel.recv_exit_status() != 0:
            print(f"Ocurrió el siguiente error: {error.readlines()}")
            connectionOS = False

        else:
            print(f"Se produjo el siguiente resultado: \n{salida.readlines()}")
            connectionOS = True

        ssh_client.close()

    except paramiko.ssh_exception.AuthenticationException as e:
        connectionOS = False
        print('Autenticación Fallida')

    return connectionOS

def ingresar_grupoBDD(usuario, contrasena, nombre, descripcion):
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
            cursor.execute('INSERT INTO GRUPO VALUES (%s, %s)', (nombre, descripcion))
            cursor.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.commit()
            connection.close()
            print("La conexión ha finalizado.")

def comprobar_institucion(usuario, contrasena, nombre):
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
            cursor.execute("SELECT * FROM INSTITUCION WHERE INSNOMBRE = %s", (nombre,))
            institucion = cursor.fetchone()
            cursor.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.close()
            print("La conexión ha finalizado.")

    return institucion

def ingresar_institucionBDD(usuario, contrasena, nombre, ciudad, descripcion):
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
            cursor.execute('INSERT INTO INSTITUCION VALUES (%s, %s, %s)', (nombre, ciudad, descripcion))
            cursor.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.commit()
            connection.close()
            print("La conexión ha finalizado.")

def configurar_pass(usuario, contrasena, user, passw):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=HOST, port=22, username=usuario, password=contrasena)

        ssh_client.get_transport()

        command = 'echo ' + '\"' + user + ':' + passw +'\" | sudo chpasswd'
        entrada, salida, error = ssh_client.exec_command(command=command, get_pty=True)
        entrada.write(contrasena + "\n")
        entrada.flush()

        if error.channel.recv_exit_status() != 0:
            print(f"Ocurrió el siguiente error: {error.readlines()}")

        else:
            print(f"Contraseña configurada correctamente")

        ssh_client.close()

    except paramiko.ssh_exception.AuthenticationException as e:
        connectionOS = False
        print('Autenticación Fallida')

def comprobar_grupos_investigador(usuario, contrasena, nombre, ci):
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
            cursor.execute("SELECT * FROM GRUPO_INVESTIGADOR WHERE GRPNOMBRE = %s AND INVIDENTIFICACION =%s", (nombre, ci,))
            grupo_inv = cursor.fetchone()
            cursor.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.close()
            print("La conexión ha finalizado.")

    return grupo_inv

def nuevo_grupo_investigadorOS(usuario, contrasena, grupo, user):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=HOST, port=22, username=usuario, password=contrasena)

        ssh_client.get_transport()

        command = "sudo usermod -aG " + grupo + " " + user
        print(command)
        entrada, salida, error = ssh_client.exec_command(command=command, get_pty=True)
        entrada.write(contrasena + "\n")
        entrada.flush()

        if error.channel.recv_exit_status() != 0:
            print(f"Ocurrió el siguiente error: {error.readlines()}")
            connectionOS = False

        else:
            print(f"Se produjo el siguiente resultado: \n{salida.readlines()}")
            connectionOS = True

        ssh_client.close()

    except paramiko.ssh_exception.AuthenticationException as e:
        connectionOS = False
        print('Autenticación Fallida')

    return connectionOS

def nuevo_grupo_investigadorBDD(usuario, contrasena, grupo, id):
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
            cursor.execute('INSERT INTO GRUPO_INVESTIGADOR VALUES (%s, %s, %s)', (grupo, id, 'S'))
            cursor.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.commit()
            connection.close()
            print("La conexión ha finalizado.")

def grupos_os(usuario, contrasena):
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
            cursor.execute("SELECT GRPNOMBRE FROM GRUPO")
            gruposS = cursor.fetchall()
            cursor.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))

    finally:
        if connection.is_connected():
            connection.close()
            print("La conexión ha finalizado.")

    return gruposS