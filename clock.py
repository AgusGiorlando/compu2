#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import os
import socket
import threading
import multiprocessing
import pickle
import reporter
import settings
import argparse

# Declaracion de variables
hora = 0
minuto = 0
mes = 0
dia = 0
terminate = False
port = os.getenv("VISOR_PORT")
args = []


def clock():
    # Informa que se refiere a las variables globales
    global hora, minuto, mes, dia, terminate
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
                    if terminate:
                        break
                hora = 0


def getFecha():
    global hora, minuto, mes, dia, port  # Informa que se refiere a las variables globales
    return (dia, mes, str(hora).zfill(2), str(minuto).zfill(2))


def connect():
    # Nuevo Socket
    desc = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    # para que no diga address already in use ...
    desc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    desc.bind((os.getenv("SERVER_IP"), int(port)))
    desc.listen(100 + 1)

    # Espera infinita de nuevos lectores
    while True:
        clientSocket, cli = desc.accept()
        leido = clientSocket.recv(2048)
        try:
            if leido != '1':
                raise Exception(
                    "El objeto recibido no es valido" + str(leido))
            fecha = getFecha()
            msg = pickle.dumps(fecha)
            clientSocket.send(msg)
        except Exception as ex:
            print(str(ex))


def checkHourAndStartReporter():
    global hora, minuto, mes, dia
    if hora == 23 and minuto == 30:
        reporterProcess = multiprocessing.Process(
            target=reporter.createReport, args=(mes, dia))
        reporterProcess.start()


def main():
    global terminate, args, port
    print(os.getpid())
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-cp', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator', default=0)

    args = parser.parse_args()
    print(args.cp)

    if args.cp != 0:
        port = args.cp[0]


    clockThread = threading.Thread(name='clock', target=clock)
    connectThread = threading.Thread(name='connect', target=connect)

    connectThread.start()
    clockThread.start()


if __name__ == "__main__":
    main()
