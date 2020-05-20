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
NUM_VISORES = 100  # TODO: Poner infinito vs parametro
SERVER_IP = 'localhost'
SERVER_PORT = 5000
LOGGER_PORT = 5003
CLOCK_PORT = 5001
movimiento_controller = MovimientoController()
empleado_controller = EmpleadoController()


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


def main():
    # Inicio del logger
    logger = Logger()
    loggerProcess = multiprocessing.Process(target=logger.connect, args=())
    loggerProcess.start()

    # Nuevo Socket
    desc = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    # para que no diga address already in use ...
    desc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    desc.bind((SERVER_IP, SERVER_PORT))
    desc.listen(NUM_VISORES)

    # Espera infinita de nuevos lectores
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
        except Exception as ex:
            print(ex)


if __name__ == "__main__":
    main()
