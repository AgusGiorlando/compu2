#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import os
import logging
import socket
import threading
import pickle

# Configuracion del logging
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-s) %(message)s')

# Declaracion de variables
NUM_VISORES = 100  # TODO: Poner infinito vs parametro
SERVER_IP = 'localhost'
LOGGER_PORT = 5003
CLOCK_PORT = 5001


class Logger:
    def connect(self,):
        # Nuevo Socket
        desc = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        # para que no diga address already in use ...
        desc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        desc.bind((SERVER_IP, LOGGER_PORT))
        desc.listen(NUM_VISORES + 1)

        # Espera infinita de nuevos lectores
        while True:
            clientSocket, cli = desc.accept()
            logging.info(cli)
            leido = clientSocket.recv(2048)
            leido = pickle.loads(leido)
            
            time = self.getTime()
            fecha = str(time[0]) + '/' + str(time[1])
            hora = str(time[2]) + ':' + str(time[3])
            log = str.format('[{0}] ({1} - {2}) - {3}-{4} - {5}\n',
                             str.upper(leido[2]),
                             leido[1],
                             leido[0],
                             fecha,
                             hora,
                             leido[3]
                             )
            file = open('logs/log.txt', 'a')
            file.write(log)
            file.close()

    def getTime(self, ):
        # Solicitud al clock de horario
        clockConnection = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM)
        clockConnection.connect((SERVER_IP, CLOCK_PORT))
        clockConnection.send(str(1))
        response = clockConnection.recv(2048)
        time = pickle.loads(response)
        clockConnection.close()
        return time
