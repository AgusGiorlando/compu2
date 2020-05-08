#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import os
import logging
import socket
import threading
import pickle
import multiprocessing

# Configuracion del logging
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-s) %(message)s')

# Declaracion de variables
NUM_VISORES = 100  # TODO: Poner infinito vs parametro
SERVER_IP = 'localhost'
LOGGER_PORT = 5003
CLOCK_PORT = 5001
queue = multiprocessing.Queue()


class Logger:
    def connect(self,):
        # Writer
        writer = multiprocessing.Process(target=self.writerProc, args=())
        writer.start()
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
            msg = clientSocket.recv(2048)
            msg = pickle.loads(msg)

            time = self.getTime()
            #self.writeLog(msg, time)
            queue.put([msg, time])

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
            
    def writerProc(self,):
        while True:
            newLog = queue.get()
            msg = newLog[0]
            time = newLog[1]
            fecha = str(time[0]) + '/' + str(time[1])
            hora = str(time[2]) + ':' + str(time[3])
            log = str.format('[{0}] ({1} - {2}) - {3}-{4} - {5}\n',
                             str.upper(msg[2]),
                             msg[1],
                             msg[0],
                             fecha,
                             hora,
                             msg[3]
                             )
            file = open('logs/log.txt', 'a')
            file.write(log)
            file.close()
