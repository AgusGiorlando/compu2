#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import socket
import pickle
import settings


class ClockHelper:
    def getHora(self, ):
        try:
            clockConnection = socket.socket(
                family=socket.AF_INET, type=socket.SOCK_STREAM)
        except socket.error as e:
            raise Exception('Error al crear socket: ' + str(e))

        try:
            clockConnection.connect(
                (os.getenv("SERVER_IP"), int(os.getenv("CLOCK_PORT"))))
        except socket.gaierror as e:
            raise Exception('Error de ruta: ' + str(e))
        except socket.error as e:
            raise Exception('Error de conexion: ' + str(e))

        try:
            clockConnection.send(str(1))
        except socket.error as e:
            raise Exception('Error de envio: ' + str(e))

        try:
            response = clockConnection.recv(2048)
        except socket.error as e:
            raise Exception('Error de recepcion: ' + str(e))
        if not len(response):
            raise Exception('Objeto vacio')

        time = pickle.loads(response)
        clockConnection.close()
        return time
