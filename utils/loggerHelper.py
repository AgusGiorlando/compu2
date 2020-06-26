#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import socket
import pickle
import settings

class LoggerHelper:
    def sendLog(self, author, level, action):
        """
        Registra un log
        """
        # Generacion del mensaje
        msg = (author, level, action)
        msg = pickle.dumps(msg)
        # Envio
        loggerConnection = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM)
        loggerConnection.connect(
            (os.getenv("SERVER_IP"), int(os.getenv("LOGGER_PORT"))))
        loggerConnection.send(msg)
        loggerConnection.close()
