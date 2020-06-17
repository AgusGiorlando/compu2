#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import os
import logging
import socket
import threading
import multiprocessing
import pickle
import reporter

# Configuracion del logging
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-s) %(message)s')

# Declaracion de variables
NUM_VISORES = 100  # TODO: Poner infinito vs parametro
SERVER_IP = 'localhost'
VISOR_PORT = 5001
hora = 0
minuto = 0
mes = 0
dia = 0


def clock():
    # Informa que se refiere a las variables globales
    global hora, minuto, mes, dia
    meses = dict()
    meses = {
        1: 31,
        2: 27,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }

    # Reloj
    while True:
        for mes, limitDia in meses.items():
            for dia in range(limitDia):
                dia += 1
                while hora < 24:
                    while minuto < 60:
                        print(str(dia) + '/' + str(mes) + ' - ' +
                              str(hora).zfill(2) + ':' + str(minuto).zfill(2))
                        checkHourAndStartReporter()
                        time.sleep(1)
                        minuto += 30
                    hora += 1
                    minuto = 0
                hora = 0


def getFecha():
    # Informa que se refiere a las variables globales
    global hora, minuto, mes, dia
    return (mes, dia, hora, minuto)


def connect():
    # Nuevo Socket
    desc = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    # para que no diga address already in use ...
    desc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    desc.bind((SERVER_IP, VISOR_PORT))
    desc.listen(NUM_VISORES + 1)

    # Espera infinita de nuevos lectores
    while True:
        clientSocket, cli = desc.accept()
        logging.info(cli)
        leido = clientSocket.recv(2048)
        if leido == '1':
            fecha = getFecha()
            msg = pickle.dumps(fecha)
            clientSocket.send(msg)


def checkHourAndStartReporter():
    global hora, minuto, mes, dia
    if hora == 23 and minuto == 30 :
        print('Inicia reporter')
        reporterProcess = multiprocessing.Process(target=reporter.createReport, args=(mes, dia))
        reporterProcess.start()

def main():
    logging.info('Inicio del clock')
    clockThread = threading.Thread(name='clock', target=clock)
    connectThread = threading.Thread(name='connect', target=connect)

    connectThread.start()
    clockThread.start()


if __name__ == "__main__":
    main()
