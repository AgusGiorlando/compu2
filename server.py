#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import threading
import logging
import pickle
import multiprocessing
import os

from logger import Logger
from movimientoController import MovimientoController
from empleadoController import EmpleadoController

# Configuracion del logging
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-s) %(message)s')

logging.info('Inicio del server')

# Declaracion de variables
SERVER_IP = 'localhost'
SERVER_PORT = 5000
LOGGER_PORT = 5003
CLOCK_PORT = 5001
movimiento_controller = MovimientoController()
empleado_controller = EmpleadoController()


def logout():
    print('Bye')


def sendLog(nivel, accion):
    """
    Registra un log
    """
    # Generacion del mensaje
    msg = (os.getppid(), 'Server', nivel, accion)
    msg = pickle.dumps(msg)

    # Envio
    loggerConnection = socket.socket(
        family=socket.AF_INET, type=socket.SOCK_STREAM)
    loggerConnection.connect((SERVER_IP, LOGGER_PORT))
    loggerConnection.send(msg)
    loggerConnection.close()


def processPeticion(oLeido, newdesc):
    """
    Recibe una peticion
    Identifica a que controller debe llamar y devuelve una respuesta
    """
    try:
        # Peticion de un Lector
        if oLeido[0] == 0:
            # Llamada al controller
            response = movimiento_controller.agregarMovimiento(
                oLeido[1], oLeido[2], oLeido[3], oLeido[4])
        # Peticion de un Dashboard
        elif oLeido[0] == 1:
            if oLeido[1] == "getEmpleados":
                response = empleado_controller.getEmpleados()
            elif oLeido[1] == "getMovimientos":
                response = movimiento_controller.getMovimientos()
            elif oLeido[1] == "addEmpleado":
                response = empleado_controller.createEmpleado(
                    oLeido[2], oLeido[3], oLeido[4], oLeido[5])
            elif oLeido[1] == "deleteEmpleado":
                response = empleado_controller.deleteEmpleadoByDni(
                    oLeido[2])
            else:
                print('No se reconoce la operacion solicitada')
                print(oLeido)
        # Envio de respuesta
        oResponse = pickle.dumps(response)
        newdesc.send(oResponse)
    except Exception as ex:
        print(ex)


def service():
    # Nuevo Socket
    desc = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    # para que no diga address already in use ...
    desc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    desc.bind((SERVER_IP, SERVER_PORT))
    desc.listen(100)

    # Espera infinita de nuevos lectores
    # sendLog('info', 'Server activo')
    while True:
        try:
            newdesc, cli = desc.accept()
            logging.info(cli)

            leido = newdesc.recv(2048)
            # TODO: Validacion del objeto recibido
            oLeido = pickle.loads(leido)
            # Nuevo hilo
            thread = threading.Thread(
                target=processPeticion, args=(oLeido, newdesc))
            thread.start()
        except EOFError:
            pass


def client():
    while True:
        try:
            # Menu y generacion de la peticion
            peticion = menu()

            # Si viene false (salir) termina el bucle
            if not peticion:
                break

        except Exception as ex:
            print(ex)
            try:
                input("Presiona enter para volver a intentar")
            except SyntaxError:
                pass
    logout()


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
    salir = False
    opcion = 0
    while not salir:
        print("1. Consultar Hora")
        print("0. Salir")
        opcion = pedirOpcion()
        if opcion == 1:
            return getHora()
        elif opcion == 0:
            salir = True
            return False
        else:
            print("Ingrese un numero entre 1 y 3")


def getHora():
    clockConnection = socket.socket(
        family=socket.AF_INET, type=socket.SOCK_STREAM)
    clockConnection.connect((SERVER_IP, CLOCK_PORT))
    clockConnection.send(str(1))
    response = clockConnection.recv(2048)
    time = pickle.loads(response)
    clockConnection.close()

    print(str(time[0]) + '/' + str(time[1]) +
          ' - ' + str(time[2]) + ':' + str(time[3]))


def main():
    print('Iniciando servidor...')
    # Inicio del logger
    logger = Logger()
    loggerProcess = multiprocessing.Process(target=logger.connect, args=())
    loggerProcess.start()

    try:
        serviceThread = threading.Thread(name='service', target=service)
        clientThread = threading.Thread(name='client', target=client)

        serviceThread.start()
        clientThread.start()
    except Exception as ex:
        print(str(ex))


if __name__ == "__main__":
    main()
