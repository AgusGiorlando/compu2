#!/usr/bin/python3

import os
import socket
import pickle
import settings
from utils.loggerHelper import LoggerHelper
from tabulate import tabulate

# Declaracion de variables
showTable = False
headers = []
logger_helper = LoggerHelper()

def main():
    while True:
        try:
            # Menu y generacion de la peticion
            peticion = menu()

            # Si viene false (salir) termina el bucle
            if not peticion:
                break

            # Conexion con el server
            try:
                desc = socket.socket(family=socket.AF_INET,
                                     type=socket.SOCK_STREAM)
            except socket.error as err:
                logger_helper.sendLog(
                    'dashboard', 'error', 'Error al crear socket: ' + str(err))
                raise Exception("Error al iniciar la conexion")

            try:
                desc.connect(
                    (os.getenv("SERVER_IP"), int(os.getenv("SERVER_PORT"))))
            except socket.gaierror as err:
                logger_helper.sendLog('dashboard', 'error',
                                      'Error de ruta: ' + str(err))
                raise Exception("Error de ruta")

            # Formatea y envia la Peticion
            response = pickle.dumps(peticion)
            try:
                desc.send(response)
            except socket.error as err:
                logger_helper.sendLog(
                    'Dashboard', 'error',  'Error de envio: ' + str(err))
                raise Exception("Error de envio")

            try:
                leido = desc.recv(2048)
            except socket.error as err:
                logger_helper.sendLog(
                    'Dashboard', 'error',  'Error de recepcion: ' + str(err))
                raise Exception("Error de recepcion")
            if not len(leido):
                logger_helper.sendLog(
                    'dashboard', 'warning', 'No se recibio ningun objeto')
                return

            # Termina la conexion
            desc.close()

            # Muestra la respuesta recibida
            oLeido = pickle.loads(leido)
            showRespuesta(oLeido)

        except Exception as ex:
            logger_helper.sendLog('dashboard', 'error', 'Error: ' + str(ex))
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
