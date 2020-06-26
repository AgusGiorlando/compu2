#!/usr/bin/python3

import logging
import os
import socket
import pickle
import settings
from tabulate import tabulate

# Configuracion del login
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-s) %(message)s')

# Declaracion de variables
showTable = False
headers = []


def sendLog(nivel, accion):
    # Generacion del mensaje
    msg = (os.getppid(), 'Dashboard', nivel, accion)
    msg = pickle.dumps(msg)

    # Envio
    loggerConnection = socket.socket(
        family=socket.AF_INET, type=socket.SOCK_STREAM)
    loggerConnection.connect(
        (os.getenv("SERVER_IP"), int(os.getenv("LOGGER_PORT"))))
    loggerConnection.send(msg)
    loggerConnection.close()


def main():
    while True:
        try:
            # Menu y generacion de la peticion
            peticion = menu()

            # Si viene false (salir) termina el bucle
            if not peticion:
                break
            
            # Conexion con el server
            desc = socket.socket(family=socket.AF_INET,
                                 type=socket.SOCK_STREAM)
            desc.connect(
                (os.getenv("SERVER_IP"), int(os.getenv("SERVER_PORT"))))

            # Formatea y envia la Peticion
            response = pickle.dumps(peticion)
            desc.send(response)
            leido = desc.recv(2048)

            # Termina la conexion
            desc.close()

            # Muestra la respuesta recibida
            oLeido = pickle.loads(leido)
            showRespuesta(oLeido)

        except Exception as ex:
            sendLog('error', 'Error: ' + str(ex))
            try:
                input("Presiona enter para volver a intentar")
            except SyntaxError:
                pass
    # Termina la conexion
    desc.close()
    print("Hasta luego")


def showRespuesta(oLeido):
    global headers, showTable
    if showTable:
        print('\n')
        print(tabulate(oLeido, headers=headers, tablefmt="orgtbl"))
        print('\n')
    else:
        print(oLeido)


def pedirOpcion():
    correcto = False
    num = 0
    while(not correcto):
        try:
            num = input("Elige una opcion: ")
            correcto = True
        except ValueError:
            print('Error, la opcion ingresada no es valida')
    return int(num)


def menu():
    global headers, showTable
    salir = False
    opcion = 0
    while not salir:
        print("1. Ver empleados")
        print("2. Ver movimientos")
        print("3. Agregar empleado")
        print("4. Eliminar empleado")
        print("0. Salir")
        opcion = pedirOpcion()
        if opcion == 1:
            showTable = True
            headers = ['ID', 'DNI', 'Nombre', 'Apellido']
            return (1, "getEmpleados")
        elif opcion == 2:
            showTable = True
            headers = ['ID', 'ID Empleado', 'Tipo', 'Fecha', 'Hora']
            return (1, "getMovimientos")
        elif opcion == 3:
            showTable = False
            headers = ['Nuevo empleado']
            return createEmpleado()
        elif opcion == 4:
            showTable = False
            headers = ['Eliminar empleado']
            return deleteEmpleado()
        elif opcion == 0:
            salir = True
            return False
        else:
            print("Ingrese un numero")


def createEmpleado():
    try:
        print("Ingrese su nombre: ")
        nombre = raw_input()
        print("Ingrese su apellido: ")
        apellido = raw_input()
        print("Ingrese su DNI: ")
        dni = input()
        print("Ingrese su clave: ")
        clave = input()
        return (1, 'addEmpleado', dni, nombre, apellido, clave)
    except Exception as ex:
        print(ex)


def deleteEmpleado():
    try:
        print("Ingrese su DNI: ")
        dni = input()
        return (1, 'deleteEmpleado', dni)
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
