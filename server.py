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

# Configuracion del logging
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-s) %(message)s')

logging.info('Inicio del server')

# Declaracion de variables
NUM_VISORES = 100  # TODO: Poner infinito vs parametro
SERVER_IP = 'localhost'
VISOR_PORT = 5000
LOGGER_PORT = 5003
CLOCK_PORT = 5001
movimiento_controller = MovimientoController()


"""
Recibe un objeto json de movimiento
Lo decodifica y envia al controller para su almacenamiento
Envia notificacion del resultado al lector
"""

def sendLog(nivel, accion):
    # Generacion del mensaje
    msg = (os.getppid(), 'Server', nivel, accion)
    msg = pickle.dumps(msg)

    # Envio
    loggerConnection = socket.socket(
        family=socket.AF_INET, type=socket.SOCK_STREAM)
    loggerConnection.connect((SERVER_IP, LOGGER_PORT))
    loggerConnection.send(msg)
    loggerConnection.close()

def processMovimiento(newdesc):
    leido = newdesc.recv(2048)
    # TODO: Validacion del objeto recibido

    oLeido = pickle.loads(leido)
    # Llamada al controller
    response = movimiento_controller.agregarMovimiento(
        oLeido[0], oLeido[1], oLeido[2], oLeido[3])

    # Envio de respuesta
    newdesc.send(response)


def main():
    # Inicio del logger
    logger = Logger()
    loggerProcess = multiprocessing.Process(target=logger.connect, args=())
    loggerProcess.start()

    # Nuevo Socket
    desc = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    # para que no diga address already in use ...
    desc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    desc.bind((SERVER_IP, VISOR_PORT))
    desc.listen(NUM_VISORES)

    # Espera infinita de nuevos lectores
    while True:
        newdesc, cli = desc.accept()
        logging.info(cli)

        # Nuevo hilo
        thread = threading.Thread(
            target=processMovimiento, args=(newdesc,))
        thread.start()


if __name__ == "__main__":
    main()
