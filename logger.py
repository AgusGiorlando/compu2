#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import os
import logging
import socket
import threading
import pickle
import multiprocessing
import settings

# Configuracion del logging
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-s) %(message)s')

# Declaracion de variables
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
        desc.bind((os.getenv("SERVER_IP"), int(os.getenv("LOGGER_PORT"))))
        desc.listen(100 + 1)

        # Espera infinita de nuevos lectores
        while True:
            clientSocket, cli = desc.accept()

            msg = clientSocket.recv(2048)
            msg = pickle.loads(msg)
            if msg[2] == 'terminate':
                writer.terminate()
                writer.join()
                break

            time = self.getTime()
            queue.put([msg, time])

        print("Fin bucle")

    def getTime(self, ):
        try:
            # Solicitud al clock de horario
            clockConnection = socket.socket(
                family=socket.AF_INET, type=socket.SOCK_STREAM)
            clockConnection.connect(
                (os.getenv("SERVER_IP"), int(os.getenv("CLOCK_PORT"))))
            clockConnection.send(str(1))
            response = clockConnection.recv(2048)
            time = pickle.loads(response)
            clockConnection.close()
            return time
        except:
            return (0,0,0,0)

    def writerProc(self,):
        """
        Lee los logs de la queue, los formatea y escribe en el archivo log.txt
        """
        while True:
            newLog = queue.get()
            try:
                # Chequeo del objeto recibido
                if len(newLog) != 2:
                    raise Exception(
                        "El objeto recibido no es valido" + str(newLog))

                msg = newLog[0]
                if len(msg) != 3:
                    raise Exception(
                        "El mensaje recibido no es valido" + str(newLog))

                time = newLog[1]
                if len(time) != 4:
                    raise Exception(
                        "El tiempo recibido no es valido" + str(newLog))


                # Formateo del log                        
                fecha = str(time[0]) + '/' + str(time[1])
                hora = str(time[2]) + ':' + str(time[3])
                log = str.format('[{0}] ({1}) - {2}-{3} - {4}\n',
                                 str.upper(msg[1]),
                                 msg[0],
                                 fecha,
                                 hora,
                                 msg[2]
                                 )
                
                # Abre y escribe en el archivo
                file = open('logs/log.txt', 'a')
                file.write(log)

                # Aviso de conexion al Clock
                if time == (0,0,0,0):
                    file.write('[ERROR] - No hay conexion con el Clock')
                    raise Exception(
                        "[ERROR] - No hay conexion con el Clock")

                file.close()
            except Exception as ex:
                print(str(ex))
