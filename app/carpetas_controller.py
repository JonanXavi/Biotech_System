import mysql.connector
from mysql.connector import Error
import paramiko
import time

HOST='192.168.100.150'

def comprobar_carpetas(usuario, contrasena):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=HOST, port=22, username=usuario, password=contrasena)
        entrada, salida, error = ssh_client.exec_command('ls -d */')
        time.sleep(1)
        lista = salida.read().decode().replace('/\n', ',')
        carpetasLinux = lista.split(',')
        carpetasLinux.pop()
        ssh_client.close()
        
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
                    path = infoInvestigador[1] + '/' + item
                    cursor.execute('INSERT INTO CARPETA VALUES (%s, %s, %s, %s, %s, DEFAULT)', (item, ci, grupoPrincipal, '', path))              
            else:
                print('No existen carpetas nuevas')

            cursor.close()
            connection.commit()
            
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

        cursor.execute("SELECT CARNOMBRE, CARDESCRIPCION FROM CARPETA WHERE INVCEDULA = %s", (ci[0],))
        carpetas = cursor.fetchall()
        cursor.close()
        connection.close()

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))
    
    return carpetas

'''
def obtener_carpeta_id(usuario, contrasena, id):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            port=3306,
            user=usuario,
            password=contrasena,
            db='biologia'
        )
        
        carpeta = None

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM CARPETA WHERE CARCODIGO = %s", (id,))
        carpeta = cursor.fetchone()
        cursor.close()
        connection.close()
        print("La conexión ha finalizado.")
        print(carpeta)  

    except Error as ex:
        print("Error durante la conexión: {}".format(ex))
    
    return carpeta   
'''

def cambiar_permisos_carpeta():
    pass